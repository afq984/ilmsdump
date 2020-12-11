import os
import contextlib
import tempfile

from typing import AsyncGenerator

import pytest
import yarl

import ilmsdump


COURSE_74 = ilmsdump.Course(
    id=74,
    serial='0001',
    name='iLMS平台線上客服專區',
    is_admin=False,
)

COURSE_46274 = ilmsdump.Course(
    id=46274, serial='10910CS542200', name='平行程式Parallel Programming', is_admin=False
)


def test_qs_get():
    assert ilmsdump.qs_get('http://example.com/?a=b', 'a') == 'b'
    with pytest.raises(KeyError):
        ilmsdump.qs_get('http://example.com', 'a')


@contextlib.asynccontextmanager
async def get_client() -> AsyncGenerator[ilmsdump.Client, None]:
    with tempfile.TemporaryDirectory() as tmpd:
        async with ilmsdump.Client(data_dir=tmpd) as client:
            yield client


@pytest.mark.asyncio
async def test_get_course_anonymous():
    async with get_client() as client:
        course = await client.get_course(46274)
        assert course == COURSE_46274

        course = await client.get_course(74)
        assert course == COURSE_74


@pytest.mark.asyncio
async def test_get_course_anonymous_doesnt_exist():
    async with get_client() as client:
        with pytest.raises(ilmsdump.UserError):
            await client.get_course(0)


@pytest.mark.asyncio
async def test_get_courses_anonymous():
    async with get_client() as client:
        with pytest.raises(ilmsdump.UserError):
            async for course in client.get_courses():
                pass


@pytest.mark.asyncio
async def test_get_course_authentication_required():
    async with get_client() as client:
        with pytest.raises(ilmsdump.UserError):
            await client.get_course(43477)


@pytest.mark.asyncio
async def test_clear_credentials():
    async with get_client() as client:
        open(client.cred_path, 'w').close()
        assert client.clear_credentials() is True
        assert not os.path.exists(client.cred_path)

        assert client.clear_credentials() is False


@pytest.mark.asyncio
async def test_get_login_state_anonymous():
    async with get_client() as client:
        assert await client.get_login_state() is None


@pytest.mark.asyncio
async def test_get_dir_for():
    async with get_client() as client:
        course = COURSE_74
        dir_ = client.get_dir_for(course)
        assert dir_.exists()


def test_as_id_string():
    assert COURSE_74.as_id_string() == 'Course-74'


def test_flatten_attribute():
    assert ilmsdump.flatten_attribute(3) == 3
    assert ilmsdump.flatten_attribute(yarl.URL('http://example.org')) == 'http://example.org'
    assert ilmsdump.flatten_attribute(COURSE_74) == COURSE_74.as_id_string()
