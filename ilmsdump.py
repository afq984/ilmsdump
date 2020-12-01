from dataclasses import dataclass
import os
import re
import functools
import itertools
import urllib.parse
import asyncio
import getpass
import dataclasses

from typing import AsyncGenerator

import aiohttp
import yarl
import lxml.html
import click


DOMAIN = 'lms.nthu.edu.tw'
LOGIN_URL = 'https://lms.nthu.edu.tw/sys/lib/ajax/login_submit.php'
LOGIN_STATE_URL = 'http://lms.nthu.edu.tw/home.php'
COURSE_LIST_URL = 'http://lms.nthu.edu.tw/home.php?f=allcourse'


class LoginFailed(Exception):
    pass


class CannotUnderstand(Exception):
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


async def response_ok_as_html(response: aiohttp.ClientResponse):
    response.raise_for_status()
    return lxml.html.fromstring(await response.read())


class ILMSClient:
    def __init__(self):
        self.session = aiohttp.ClientSession()

        self.data_dir = os.path.abspath('ilmsdump.d')
        os.makedirs(self.data_dir, exist_ok=True)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    log = staticmethod(print)

    async def ensure_authenticated(self):
        cred_path = os.path.join(self.data_dir, 'credentials.txt')
        try:
            cred_file = open(cred_path)
        except FileNotFoundError:
            await self.interactive_login()
            with open(cred_path, 'w') as file:
                print(
                    self.session.cookie_jar.filter_cookies(LOGIN_STATE_URL)['PHPSESSID'].value,
                    file=file,
                )
            self.log('Saved credentials to', cred_path)
        else:
            with cred_file:
                self.log('Using existing credentials in', cred_path)
                phpsessid = cred_file.read().strip()
                await self.login_with_phpsessid(phpsessid)

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
            html = await response_ok_as_html(response)

            if not html.xpath('//*[@id="login"]'):
                return None

            name_node = html.xpath('//*[@id="profile"]/div[2]/div[1]/text()')
            assert name_node
            return ''.join(name_node).strip()

    async def get_courses(self) -> AsyncGenerator['Course', None]:
        async with self.session.get(COURSE_LIST_URL) as response:
            html = await response_ok_as_html(response)

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

    async def _response_paginator(self, url, params, page=1):
        for page in itertools.count(page):
            params['page'] = page
            async with self.session.get(url, params=params) as response:
                html = await response_ok_as_html(response)
                yield html

                next_hrefs = html.xpath('//span[@class="page"]//a[text()="Next"]/@href')
                if not next_hrefs:
                    break
                next_page = int(qs_get(next_hrefs[0], 'page'))
                assert page + 1 == next_page


@dataclasses.dataclass
class Course:
    """歷年課程檔案"""

    id: int
    name: str
    is_admin: bool

    def _item_paginator(self, client, f):
        return client._response_paginator(
            'http://lms.nthu.edu.tw/course.php',
            params={
                'courseID': self.id,
                'f': f,
            },
        )

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
class Announcement:
    """課程活動(公告)"""

    id: int
    title: str
    course: Course


@dataclasses.dataclass
class Material:
    """上課教材"""

    id: int
    title: str
    type: str
    course: Course


@dataclasses.dataclass
class Discussion:
    """討論區"""

    id: int
    title: str
    course: Course


@dataclasses.dataclass
class Homework:
    """作業"""

    id: int
    title: str
    course: Course


@click.group()
def main():
    pass


@main.command()
@as_sync
async def test():
    """Testing command to be removed"""
    async with ILMSClient() as client:
        await client.ensure_authenticated()
        courses = [x async for x in client.get_courses()]
        print(courses)
        async for announcement in courses[5].get_announcements(client):
            print(announcement)
        async for discussion in courses[1].get_discussions(client):
            print(discussion)
        async for material in courses[5].get_materials(client):
            print(material)
        async for homework in courses[-2].get_homeworks(client):
            print(homework)


if __name__ == '__main__':
    main()
