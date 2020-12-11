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
