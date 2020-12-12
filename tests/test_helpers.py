import lxml.html
import pytest
import yarl

import ilmsdump

from tests import data


def test_qs_get():
    assert ilmsdump.qs_get('http://example.com/?a=b', 'a') == 'b'
    with pytest.raises(KeyError):
        ilmsdump.qs_get('http://example.com', 'a')


def test_flatten_attribute():
    assert ilmsdump.flatten_attribute(3) == 3
    assert ilmsdump.flatten_attribute(yarl.URL('http://example.org')) == 'http://example.org'
    assert ilmsdump.flatten_attribute(data.COURSE_74) == data.COURSE_74.as_id_string()


def test_get_attachments():
    html = lxml.html.fromstring(
        '''
        <a href="example.com/a">one</a>
        <a href="/sys/read_attach.php?id=12345" title="attachment.txt">two</a>
        <a href="/sys/read_attach.php?id=12345" title="attachment.txt">three</a>
        '''
    )

    assert list(ilmsdump.get_attachments(data.COURSE_74, html)) == [
        ilmsdump.Attachment(id=12345, title='attachment.txt', parent=data.COURSE_74),
    ]


def test_generate_table():
    table = ''.join(
        ilmsdump.generate_table(
            [data.COURSE_74, data.COURSE_1808, data.COURSE_359],
        )
    )
    expected = '''\
id    serial           name                                 is_admin
----  ---------------  -----------------------------------  --------
74    0001             iLMS平台線上客服專區                 False\x20\x20\x20
1808  09810BMES525100  藥物控制釋放Drug Controlled Release  False\x20\x20\x20
359   09810CL492400    敦煌學Dunhuang Studies               False\x20\x20\x20
'''
    assert expected == table


@pytest.mark.asyncio
async def test_empty_async_generator():
    called = 0

    @ilmsdump.as_empty_async_generator
    async def agen():
        nonlocal called
        called += True

    assert [_ async for _ in agen()] == []
    assert called == 1
