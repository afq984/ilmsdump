import os
import contextlib
import pytest
import tempfile

from typing import AsyncGenerator

import ilmsdump


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
        assert course.id == 46274
        assert course.name == '平行程式Parallel Programming'
        assert course.is_admin is False


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
        course = ilmsdump.Course(id=74, name='example', is_admin=False)
        dir_ = client.get_dir_for(course)
        assert dir_.exists()
