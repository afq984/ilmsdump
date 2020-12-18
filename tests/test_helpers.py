import os
import signal

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

    # malformed link
    html = lxml.html.fromstring(
        '<a href="/sys/read_attach.php?id=109077" target="_blank" style="color: rgb(68, 68, 255); '
        'text-decoration: none; "></a>'
    )
    assert list(ilmsdump.get_attachments(data.HOMEWORK_32460, html)) == []


def test_generate_table():
    table = ''.join(
        ilmsdump.generate_table(
            [data.COURSE_74, data.COURSE_1808, data.COURSE_359],
        )
    )
    expected = '''\
id    serial           is_admin  name
----  ---------------  --------  -----------------------------------
74    0001             False     iLMS平台線上客服專區
1808  09810BMES525100  False     藥物控制釋放Drug Controlled Release
359   09810CL492400    False     敦煌學Dunhuang Studies
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


@pytest.mark.skip()
@pytest.mark.asyncio
async def test_capture_keyboard_interrupt():
    with ilmsdump.capture_keyboard_interrupt() as interrupted:
        assert not interrupted.is_set()
        os.kill(0, getattr(signal, 'CTRL_C_EVENT', signal.SIGINT))
        assert interrupted.is_set()
