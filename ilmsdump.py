import os
import re
import sys
import json
import pathlib
import collections
import functools
import itertools
import urllib.parse
import asyncio
import getpass
import dataclasses

from typing import List, Union, AsyncGenerator

import aiohttp
import yarl
import lxml.html
import click
import wcwidth


DOMAIN = 'lms.nthu.edu.tw'
LOGIN_URL = 'https://lms.nthu.edu.tw/sys/lib/ajax/login_submit.php'
LOGIN_STATE_URL = 'http://lms.nthu.edu.tw/home.php'
COURSE_LIST_URL = 'http://lms.nthu.edu.tw/home.php?f=allcourse'


class LoginFailed(Exception):
    pass


class CannotUnderstand(Exception):
    pass


class UserError(Exception):
    pass


def as_sync(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))

    return wrapper


def qs_get(url: str, key: str) -> str:
    purl = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(purl.query)
    try:
        return query[key][0]
    except KeyError:
        raise KeyError(key, url) from None


class Client:
    def __init__(self, data_dir):
        self.session = aiohttp.ClientSession(
            raise_for_status=True,
        )

        self.data_dir = pathlib.Path(data_dir).absolute()
        os.makedirs(self.data_dir, exist_ok=True)

        self.cred_path = os.path.join(self.data_dir, 'credentials.txt')

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    log = staticmethod(print)

    async def ensure_authenticated(self, prompt: bool):
        try:
            cred_file = open(self.cred_path)
        except FileNotFoundError:
            if prompt:
                await self.interactive_login()
                with open(self.cred_path, 'w') as file:
                    print(
                        self.session.cookie_jar.filter_cookies(LOGIN_STATE_URL)['PHPSESSID'].value,
                        file=file,
                    )
                self.log('Saved credentials to', self.cred_path)
        else:
            with cred_file:
                self.log('Using existing credentials in', self.cred_path)
                phpsessid = cred_file.read().strip()
                await self.login_with_phpsessid(phpsessid)

    def clear_credentials(self):
        """
        Clear saved credentials. Returns true if something is actually removed. False otherwise.
        """
        try:
            os.remove(self.cred_path)
        except FileNotFoundError:
            self.log('No credentials saved in', self.cred_path)
            return False
        else:
            self.log('Removed saved credentials in', self.cred_path)
            return True

    async def interactive_login(self):
        username = input('iLMS username (leave empty to login with PHPSESSID): ')
        if username:
            password = getpass.getpass('iLMS password: ')
            await self.login_with_username_and_password(username, password)
        else:
            phpsessid = getpass.getpass('iLMS PHPSESSID: ')
            await self.login_with_phpsessid(phpsessid)

    async def login_with_username_and_password(self, username, password):
        login = self.session.get(
            LOGIN_URL,
            params={'account': username, 'password': password},
        )
        async with login as response:
            response.raise_for_status()
            json_body = await response.json(
                content_type=None,  # to bypass application/json check
            )
        json_ret = json_body['ret']
        if json_ret['status'] != 'true':
            raise LoginFailed(json_ret)
        self.log('Logged in as', json_ret['name'])

    async def login_with_phpsessid(self, phpsessid):
        self.session.cookie_jar.update_cookies(
            {'PHPSESSID': phpsessid},
            response_url=yarl.URL(DOMAIN),
        )
        name = await self.get_login_state()
        if name is not None:
            self.log('Logged in as', name)
            return
        raise LoginFailed('cannot login with provided PHPSESSID')

    async def get_login_state(self):
        async with self.session.get(LOGIN_STATE_URL) as response:
            html = lxml.html.fromstring(await response.read())

            if not html.xpath('//*[@id="login"]'):
                return None

            name_node = html.xpath('//*[@id="profile"]/div[2]/div[1]/text()')
            assert name_node
            return ''.join(name_node).strip()

    async def get_course(self, course_id: int) -> 'Course':
        async with self.session.get(
            'http://lms.nthu.edu.tw/course.php',
            params={
                'courseID': course_id,
                'f': 'hwlist',
            },
        ) as response:
            body = await response.read()
            if not body:
                raise UserError(
                    'Empty response returned for course, '
                    f"the course probably doesn't exist: course_id={course_id}"
                )

            html = lxml.html.fromstring(body)

            (name,) = html.xpath('//div[@class="infoPath"]/a/text()')

            if html.xpath('//a[@href="javascript:add()"]'):
                is_admin = True
            else:
                is_admin = False

            course = Course(
                id=course_id,
                name=name,
                is_admin=is_admin,
            )

            if response.url.path == '/course_login.php':
                raise UserError(f'No access to course: {course}')

            return course

    async def get_courses(self) -> AsyncGenerator['Course', None]:
        async with self.session.get(COURSE_LIST_URL) as response:
            body = await response.read()
            if b'\xe6\xac\x8a\xe9\x99\x90\xe4\xb8\x8d\xe8\xb6\xb3!' in body:
                # '權限不足!'
                raise UserError('Cannot get enrolled courses for user')
            html = lxml.html.fromstring(body)

            for a in html.xpath('//td[@class="listTD"]/a'):
                bs = a.xpath('b')
                if bs:
                    is_admin = True
                    (tag,) = bs
                else:
                    is_admin = False
                    tag = a

                name = tag.text

                m = re.match(r'/course/(\d+)', a.attrib['href'])
                if m is None:
                    raise CannotUnderstand('course URL', a.attrib['href'])
                yield Course(
                    id=int(m.group(1)),
                    name=name,
                    is_admin=is_admin,
                )

    def get_dir_for(self, item: 'Downloadable') -> pathlib.Path:
        d = self.data_dir / item.__class__.__name__.lower() / str(item.id)
        d.mkdir(parents=True, exist_ok=True)
        return d


class Downloadable:
    async def download(self, client) -> AsyncGenerator['Downloadable', None]:
        return
        yield


@dataclasses.dataclass
class Stat:
    total: int = 0
    completed: int = 0


class Downloader:
    def __init__(self, client: Client):
        self.client = client
        self.stats = collections.defaultdict(Stat)

    def report_progress(self):
        progress_str = ' '.join(
            f'{k[:3]}[{v.completed}/{v.total}]' for (k, v) in self.stats.items()
        )
        print('Progress:', progress_str, end='\r', file=sys.stderr)

    async def run(self, items):
        for item in items:
            self.stats[item.__class__.__name__].total += 1

        while items:
            item = items.pop()

            async for child in item.download(self.client):
                items.append(child)
                self.stats[child.__class__.__name__].total += 1

            self.stats[item.__class__.__name__].completed += 1
            self.report_progress()

        self.report_progress()
        print(file=sys.stderr)


def html_get_main(html: lxml.html.HtmlElement) -> lxml.html.HtmlElement:
    main, = html.xpath('//div[@id="main"]')
    for to_remove in itertools.chain(
        main.xpath('div[@class="infoPath"]'),
        main.xpath('//script'),
    ):
        to_remove.getparent().remove(to_remove)
    return main


@dataclasses.dataclass
class Course(Downloadable):
    """歷年課程檔案"""

    id: int
    name: str
    is_admin: bool

    async def download(self, client):
        generators = [
            self.get_announcements(client),
            self.get_materials(client),
            self.get_discussions(client),
            self.get_homeworks(client),
        ]
        for generator in generators:
            async for item in generator:
                yield item

        async with client.session.get(
            'http://lms.nthu.edu.tw/course.php',
            params={
                'courseID': self.id,
                'f': 'syllabus',
            },
        ) as response:
            html = lxml.html.fromstring(await response.read())

        if html.xpath('//input[@id="loginAccount"]'):
            raise UserError('Must login')
        main = html_get_main(html)
        with (client.get_dir_for(self) / 'index.html').open('wb') as file:
            file.write(lxml.html.tostring(main))

    async def _item_paginator(self, client, f, page=1):
        for page in itertools.count(page):
            async with client.session.get(
                'http://lms.nthu.edu.tw/course.php',
                params={
                    'courseID': self.id,
                    'f': f,
                    'page': page,
                },
            ) as response:
                html = lxml.html.fromstring(await response.read())

                if html.xpath('//td[text()="目前尚無資料"]'):  # XXX: might be in English
                    break

                yield html

                next_hrefs = html.xpath('//span[@class="page"]//a[text()="Next"]/@href')
                if not next_hrefs:
                    break
                next_page = int(qs_get(next_hrefs[0], 'page'))
                assert page + 1 == next_page

    async def get_announcements(self, client) -> AsyncGenerator['Announcement', None]:
        async for html in self._item_paginator(client, 'news'):
            for tr in html.xpath('//*[@id="main"]//tr[@class!="header"]'):
                (href,) = tr.xpath('td[1]/a/@href')
                (title,) = tr.xpath('td[2]//a/text()')
                yield Announcement(
                    id=int(qs_get(href, 'newsID')),
                    title=title,
                    course=self,
                )

    async def get_materials(self, client) -> AsyncGenerator['Material', None]:
        async for html in self._item_paginator(client, 'doclist'):
            for a in html.xpath('//*[@id="main"]//tr[@class!="header"]/td[2]/div/a'):
                yield Material(
                    id=int(qs_get(a.attrib['href'], 'cid')),
                    title=a.text,
                    type=a.getparent().attrib['class'],
                    course=self,
                )

    async def get_discussions(self, client) -> AsyncGenerator['Discussion', None]:
        async for html in self._item_paginator(client, 'forumlist'):
            for tr in html.xpath('//*[@id="main"]//tr[@class!="header"]'):
                (href,) = tr.xpath('td[1]/a/@href')
                (title,) = tr.xpath('td[2]//a/span/text()')
                yield Discussion(
                    id=int(qs_get(href, 'tid')),
                    title=title,
                    course=self,
                )

    async def get_homeworks(self, client) -> AsyncGenerator['Homework', None]:
        async for html in self._item_paginator(client, 'hwlist'):
            for a in html.xpath('//*[@id="main"]//tr[@class!="header"]/td[2]/a[1]'):
                yield Homework(
                    id=int(qs_get(a.attrib['href'], 'hw')),
                    title=a.text,
                    course=self,
                )


@dataclasses.dataclass
class Announcement(Downloadable):
    """課程活動(公告)"""

    id: int
    title: str
    course: Course


@dataclasses.dataclass
class Material(Downloadable):
    """上課教材"""

    id: int
    title: str
    type: str
    course: Course


@dataclasses.dataclass
class Discussion(Downloadable):
    """討論區"""

    id: int
    title: str
    course: Course

    async def download(self, client: Client):
        async with client.session.post(
            'http://lms.nthu.edu.tw/sys/lib/ajax/post.php',
            data={
                'id': self.id,
            },
        ) as response:
            body_json = await response.json(content_type=None)
            if not body_json['posts']['status']:
                raise CannotUnderstand(body_json)

            for post in body_json['posts']['items']:
                for attachment in post['attach']:
                    yield Attachment(
                        id=int(attachment['id']),
                        parent=self,
                    )

            with (client.get_dir_for(self) / 'index.json').open('w') as file:
                json.dump(body_json, file)


@dataclasses.dataclass
class Homework(Downloadable):
    """作業"""

    id: int
    title: str
    course: Course


@dataclasses.dataclass
class Attachment(Downloadable):
    id: int
    parent: Downloadable

    async def download(self, client):
        async with client.session.get(
            'http://lms.nthu.edu.tw/sys/read_attach.php',
            params={
                'id': self.id,
            },
        ) as response:
            content_disposition = response.headers['Content-Disposition']
            with (client.get_dir_for(self) / 'meta.json').open('w') as file:
                json.dump(
                    {
                        'Content-Disposition': content_disposition,
                    },
                    file,
                )

            with (client.get_dir_for(self) / 'data').open('wb') as file:
                async for chunk in response.content.iter_any():
                    file.write(chunk)
        return
        yield


def generate_table(items):
    fields = [field.name for field in dataclasses.fields(items[0])]
    rows = [fields]
    rows.extend(
        [str(getattr(x := getattr(item, field), 'id', x)) for field in fields] for item in items
    )
    widths = [max(map(wcwidth.wcswidth, col)) for col in zip(*rows)]
    for i, row in enumerate(rows):
        for j, (width, cell) in enumerate(zip(widths, row)):
            if j:
                yield '  '
            yield cell
            yield ' ' * (width - wcwidth.wcswidth(cell))
        yield '\n'
        if i == 0:
            for j, width in enumerate(widths):
                if j:
                    yield '  '
                yield '-' * width
            yield '\n'


def print_table(items):
    print(end=''.join(generate_table(items)))


async def foreach_course(
    client: Client, course_ids: List[Union[str, int]]
) -> AsyncGenerator[Course, None]:
    for course_id in course_ids:
        if course_id == 'enrolled':
            async for course in client.get_courses():
                yield course
        else:
            yield await client.get_course(int(course_id))


def validate_course_id(ctx, param, value: str):
    result: List[Union[str, int]] = []
    for course_id in value:
        if course_id == 'enrolled':
            result.append(course_id)
        elif not course_id.isdigit():
            raise click.BadParameter('must be a number or the string "enrolled"')
        else:
            result.append(int(course_id))
    return result


@click.command(
    help="""
        Dump the courses given by their ID.
        The string "enrolled" can be used as a special ID to dump all courses
        enrolled by the logged in user.
        """,
)
@click.option(
    '--logout',
    is_flag=True,
    help="""
        Clear iLMS credentials.
        If specified with --login, the credentials is cleared first, then login is performed
    """,
)
@click.option(
    '--login',
    is_flag=True,
    help='Login to iLMS interactively before accessing iLMS',
)
@click.option(
    '-o',
    '--output-dir',
    metavar='DIR',
    default='ilmsdump.d',
    show_default=True,
    help='Output directory to store login credentials and downloads',
)
@click.argument(
    'course_ids',
    nargs=-1,
    callback=validate_course_id,
)
@as_sync
async def main(course_ids, logout: bool, login: bool, output_dir: str):
    async with Client(data_dir=output_dir) as client:
        d = Downloader(client=client)
        changed = False
        if logout:
            changed |= client.clear_credentials()

        await client.ensure_authenticated(prompt=login)
        changed |= login

        if course_ids:
            courses = [course async for course in foreach_course(client, course_ids)]

            if courses:
                changed = True
                print(end=''.join(generate_table(courses)))
                await d.run(courses)
        if not changed:
            print('Nothing to do')


if __name__ == '__main__':
    main()
