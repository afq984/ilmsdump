from __future__ import annotations

import dataclasses
import functools
import json
import pathlib
from typing import Optional, Union

import aiohttp_jinja2
import click
import jinja2
import lxml.html
import yarl
from aiohttp import web

here = pathlib.Path(__file__).parent.resolve()


@dataclasses.dataclass
class Object:
    ctx: ApplicationContext
    typename: str
    id: int

    @classmethod
    def from_name(cls, ctx: ApplicationContext, name: str):
        typename, _, id = name.partition('-')
        return cls(ctx, typename.lower(), int(id))

    @functools.cached_property
    def meta(self):
        with self.ctx.open_base(self.typename, self.id) as file:
            return json.load(file)

    def beta(self):
        return self.meta

    def open(self, filename):
        return self.ctx.open_base(self.typename, self.id, filename)

    def embed(self, filename):
        with self.open(filename) as file:
            return jinja2.Markup(file.read())

    @functools.cached_property
    def children(self):
        children = {}
        for name in self.meta['children']:
            child = self.ctx.get_name(name)
            children.setdefault(child.typename, []).append(child)
        return children

    def get_url(self):
        return yarl.URL('/') / self.typename / str(self.id)

    @property
    def dir(self):
        return self.ctx.data_dir / self.typename / str(self.id)

    @functools.cached_property
    def course(self):
        return self.from_name(self.ctx, self.meta['course'])

    @functools.cached_property
    def json(self):
        with self.open('index.json') as file:
            return json.load(file)

    def to_path_frag(self, by):
        return PathFrag(str(self.get_url()), self.meta[by])

    def __repr__(self):
        return f'<Object {self.typename} {self.id}>'


class ApplicationContext:
    def __init__(self, data_dir):
        self.data_dir = pathlib.Path(data_dir)

    def open_base(self, typename, id, filename='meta.json'):
        return (self.data_dir / typename / str(id) / filename).open()

    def get_name(self, name):
        return Object.from_name(self, name)

    def get(self, typename, id):
        return Object(self, typename, id)

    def get_all(self, typename):
        for path in (self.data_dir / typename).glob('*/meta.json'):
            yield Object(self, typename, path.parent.name)


APP_CTX_KEY = 'ilmsserve.WbDgTQZTofTlfR0o'


@dataclasses.dataclass
class MenuItem:
    typename: Optional[str]
    name: str
    countable: bool

    def href(self, obj: Object):
        if self.typename is None:
            return obj.get_url()
        return obj.get_url() / self.typename

    def is_active(self, obj: Object, request):
        return str(self.href(obj)) == str(request.url.path)

    def text(self, children):
        if not self.countable:
            return self.name
        return '{} ({})'.format(self.name, len(children.get(self.typename, ())))


MENU_ANNOUNCEMENT = MenuItem('announcement', '公告', True)
MENU_MATERIAL = MenuItem('material', '上課教材', True)
MENU_DISCUSSION = MenuItem('discussion', '討論區', True)
MENU_HOMEWORK = MenuItem('homework', '作業', True)
MENU_SCORE = MenuItem('score', '成績計算', False)
MENU_GROUPLIST = MenuItem('grouplist', '小組專區', False)
COURSE_MENU_ITEMS = [
    MenuItem(None, '課程說明', False),
    MENU_ANNOUNCEMENT,
    MENU_MATERIAL,
    MENU_DISCUSSION,
    MENU_HOMEWORK,
    MENU_SCORE,
    MENU_GROUPLIST,
]


@object.__new__
class fa:
    def __getitem__(self, name):
        return jinja2.Markup('<span class="icon"><i class="fas fa-{}"></i></span>').format(name)


@dataclasses.dataclass
class PathFrag:
    url: str
    text: Union[str, jinja2.Markup]


PATH_FRAG_HOME = PathFrag('/', fa['home'])


class View(web.View):
    @property
    def ctx(self) -> ApplicationContext:
        return self.request.app[APP_CTX_KEY]

    @property
    def id(self):
        return int(self.request.match_info['id'])


class IndexView(View):
    @aiohttp_jinja2.template('index.html.j2')
    def get(self):
        return {
            'courses': [course for course in self.ctx.get_all('course')],
            'path': [PathFrag('/', fa['home'] + ' ilmsserve')],
        }


class CourseView(View):
    item_class = 'course'
    template_name = 'course.html.j2'

    def get_path(self, item):
        return [PATH_FRAG_HOME, item.to_path_frag('name')]

    def prepare(self):
        item = self.ctx.get(self.item_class, self.id)
        if self.item_class == 'course':
            course = item
        else:
            course = item.course
        return {
            'item': item,
            'course': course,
            'path': self.get_path(item=item),
        }

    async def get(self):
        return aiohttp_jinja2.render_template(
            self.template_name,
            self.request,
            self.prepare(),
        )


class ListView(CourseView):
    template_name = 'list.html.j2'

    menu_item: MenuItem

    def prepare(self):
        return {
            **super().prepare(),
            'list_class': self.menu_item.typename,
        }

    def get_path(self, item):
        return [
            PATH_FRAG_HOME,
            item.to_path_frag('name'),
            PathFrag(str(self.menu_item.href(item)), self.menu_item.name),
        ]


class AnnouncementListView(ListView):
    menu_item = MENU_ANNOUNCEMENT


class MaterialListView(ListView):
    menu_item = MENU_MATERIAL


class DiscussionListView(ListView):
    menu_item = MENU_DISCUSSION


class HomeworkListView(ListView):
    menu_item = MENU_HOMEWORK


class L2FlatView(CourseView):

    menu_item: MenuItem

    def get_path(self, item):
        return [
            PATH_FRAG_HOME,
            item.course.to_path_frag('name'),
            PathFrag(str(self.menu_item.href(item)), self.menu_item.name),
        ]


class ScoreView(L2FlatView):
    item_class = 'score'
    menu_item = MENU_SCORE


class GroupView(L2FlatView):
    item_class = 'grouplist'
    menu_item = MENU_GROUPLIST


class L2View(CourseView):

    menu_item: MenuItem

    @property
    def item_class(self):
        return self.menu_item.typename

    def get_path(self, item):
        return [
            PATH_FRAG_HOME,
            item.course.to_path_frag('name'),
            PathFrag(str(self.menu_item.href(item.course)), self.menu_item.name),
            item.to_path_frag('title'),
        ]


class AnnouncementView(L2View):
    menu_item = MENU_ANNOUNCEMENT
    template_name = 'announcement.html.j2'


class MaterialView(L2View):
    menu_item = MENU_MATERIAL


class DiscussionView(L2View):
    menu_item = MENU_DISCUSSION
    template_name = 'discussion.html.j2'


class HomeworkView(L2View):
    menu_item = MENU_HOMEWORK
    template_name = 'homework.html.j2'


class SubmissionListView(L2View):
    menu_item = MENU_HOMEWORK
    template_name = 'submissions.html.j2'

    def get_path(self, item):
        return super().get_path(item) + [
            PathFrag(
                item.get_url() / 'submissions',
                f'可下載 ({len(item.children.get("submittedhomework", ()))})',
            ),
        ]


class SubmissionRedirectView(View):
    def get(self):
        item = self.ctx.get('submittedhomework', self.request.match_info['id'])
        for homework in item.course.children['homework']:
            if f'SubmittedHomework-{self.id}' in homework.meta['children']:
                raise web.HTTPTemporaryRedirect(
                    f'/homework/{homework.meta["id"]}/submissions/{self.id}'
                )
        raise web.HTTPServerError


class SubmissionView(SubmissionListView):
    template_name = 'course.html.j2'
    item_class = 'submittedhomework'

    def prepare(self):
        item = self.ctx.get(self.item_class, self.id)
        course = item.course
        homework = self.ctx.get('homework', self.request.match_info['hid'])
        assert f'SubmittedHomework-{self.id}' in homework.meta['children']
        return {
            'item': item,
            'course': course,
            'path': self.get_path(item=homework) + [item.to_path_frag('by')],
        }


class AttachmentView(View):
    async def get(self):
        item = self.ctx.get('attachment', self.id)
        title = filename = item.meta['title']
        if filename == 'meta.json':
            filename = 'meta_.json'
        return web.FileResponse(
            item.dir / filename,
            headers={
                'Content-Disposition': "attachment; filename*=UTF-8''{}".format(
                    str(yarl.URL(title)),
                )
            },
        )


class VideoView(View):
    async def get(self):
        item = self.ctx.get('video', self.id)
        return web.FileResponse(
            item.dir / 'video.mp4',
        )


def read_attach_php(request: web.Request):
    try:
        id = request.url.query['id']
    except KeyError:
        raise web.HTTPBadRequest
    raise web.HTTPTemporaryRedirect(yarl.URL('/attachment') / id)


class CoursePHP(View):
    def param(self, name):
        try:
            return self.request.query[name]
        except KeyError:
            raise web.HTTPBadRequest(text=f'missing required query parameter: {name}')

    def redirect_url(self):
        courseID = self.param('courseID')
        f = self.request.query.get('f', 'syllabus')
        if f == 'syllabus':
            return f'/course/{courseID}'
        if f == 'activity' or f == 'news':
            return f'/course/{courseID}/announcement'
        if f == 'doclist':
            return f'/course/{courseID}/material'
        if f == 'forumlist':
            return f'/course/{courseID}/discussion'
        if f == 'hwlist':
            return f'/course/{courseID}/homework'
        if f == 'score':
            return f'/course/{courseID}/score'
        if f in {
            'group',
            'grouplist',
            'teamall',
            'team_forumlist',
            'team_memberlist',
            'team_homework',
        }:
            return f'/course/{courseID}/grouplist'
        if f == 'news_show':
            return f'/announcement/{self.param("newsID")}'
        if f == 'doc':
            cid = self.param("cid")
            if (self.ctx.data_dir / 'material' / cid / 'meta.json').exists():
                return f'/material/{cid}'
            if (self.ctx.data_dir / 'submittedhomework' / cid / 'meta.json').exists():
                return f'/submittedhomework/{self.param("cid")}'
        if f == 'forum':
            return f'/discussion/{self.param("tid")}'
        if f == 'hw':
            return f'/homework/{self.param("hw")}'
        if f == 'hw_doclist':
            return f'/homework/{self.param("hw")}/submissions'
        raise web.HTTPNotFound

    async def get(self):
        raise web.HTTPTemporaryRedirect(self.redirect_url())


ICON_MAPPING = {
    'check.gif': 'done',
    'web.gif': 'home',
    'item2.gif': 'attachment',
    'mail.png': 'email',
    'wait.gif': 'hourglass_top',
    'zoom.jpg': 'zoom_in',
    'lock.gif': 'lock',
    'cal_homework.gif': 'edit',
}


def icon_redirect(request):
    filename = request.match_info['filename']
    try:
        icon = ICON_MAPPING[filename]
    except KeyError:
        raise web.HTTPNotFound
    raise web.HTTPTemporaryRedirect(
        f'https://fonts.gstatic.com/s/i/materialicons/{icon}/v6/24px.svg'
    )


def fix_img_src(data: dict):
    for post in data['posts']['items']:
        if not post['note'].strip():
            continue
        element = lxml.html.fromstring(post['note'])
        fixes = {}
        for attachment in post['attach']:
            fixes[attachment['fileName']] = f'/attachment/{attachment["id"]}'
        for img in element.xpath('//img[starts-with(@src, "/sysdata")]'):
            filename = yarl.URL(img.attrib['src']).name
            img.attrib['src'] = fixes.get(filename, filename)
        post['note'] = lxml.html.tostring(element, encoding='unicode')
    return data


def sort_by_id(items):
    return sorted(items, key=lambda x: x.meta['id'], reverse=True)


def robots_txt(request):
    return web.Response(
        text='''User-agent: *
Disallow: /
'''
    )


def make_app(data_dir: str):
    app = web.Application()
    ctx = app[APP_CTX_KEY] = ApplicationContext(data_dir=data_dir)
    jinja2_env = aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(here / 'templates'),
        context_processors=[aiohttp_jinja2.request_processor],
    )
    jinja2_env.globals.update(
        {
            'ctx': ctx,
            'COURSE_MENU_ITEMS': COURSE_MENU_ITEMS,
            'fa': fa,
            'fix_img_src': fix_img_src,
            'sort_by_id': sort_by_id,
        }
    )
    app.add_routes(
        [
            # lists
            web.view('/', IndexView),
            web.view(r'/course/{id:\d+}', CourseView),
            web.view(r'/course/{id:\d+}/announcement', AnnouncementListView),
            web.view(r'/course/{id:\d+}/material', MaterialListView),
            web.view(r'/course/{id:\d+}/discussion', DiscussionListView),
            web.view(r'/course/{id:\d+}/homework', HomeworkListView),
            # single item list
            web.view(r'/course/{id:\d+}/score', ScoreView),
            web.view(r'/course/{id:\d+}/grouplist', GroupView),
            # single item
            web.view(r'/announcement/{id:\d+}', AnnouncementView),
            web.view(r'/material/{id:\d+}', MaterialView),
            web.view(r'/discussion/{id:\d+}', DiscussionView),
            web.view(r'/homework/{id:\d+}', HomeworkView),
            web.view(r'/homework/{id:\d+}/submissions', SubmissionListView),
            web.view(r'/submittedhomework/{id:\d+}', SubmissionRedirectView),
            web.view(r'/homework/{hid:\d+}/submissions/{id:\d+}', SubmissionView),
            # downloads
            web.view(r'/attachment/{id:\d+}', AttachmentView),
            web.view(r'/video/{id:\d+}', VideoView),
            # redirects
            web.get('/sys/read_attach.php', read_attach_php),
            web.view('/course.php', CoursePHP),
            web.get('/sys/res/icon/{filename}', icon_redirect),
            # misc
            web.get('/robots.txt', robots_txt),
        ]
    )
    return app


@click.command()
@click.option(
    '--data-dir',
    help='Data directory.',
    default='ilmsdump.out',
)
@click.option(
    '--port',
    type=int,
)
def main(data_dir: str, port: Optional[int]):
    app = make_app(data_dir=data_dir)
    web.run_app(app, port=port)
