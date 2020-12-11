import os

import pytest

import ilmsdump

from tests import utils
from tests import data


@pytest.mark.asyncio
async def test_get_course_anonymous():
    async with utils.get_client() as client:
        course = await client.get_course(46274)
        assert course == data.COURSE_46274

        course = await client.get_course(74)
        assert course == data.COURSE_74


@pytest.mark.asyncio
async def test_get_course_anonymous_doesnt_exist():
    async with utils.get_client() as client:
        with pytest.raises(ilmsdump.UserError):
            await client.get_course(0)


@pytest.mark.asyncio
async def test_get_courses_anonymous():
    async with utils.get_client() as client:
        with pytest.raises(ilmsdump.UserError):
            async for course in client.get_courses():
                pass


@pytest.mark.asyncio
async def test_get_course_authentication_required():
    async with utils.get_client() as client:
        with pytest.raises(ilmsdump.UserError):
            await client.get_course(43477)


@pytest.mark.asyncio
async def test_clear_credentials():
    async with utils.get_client() as client:
        open(client.cred_path, 'w').close()
        assert client.clear_credentials() is True
        assert not os.path.exists(client.cred_path)

        assert client.clear_credentials() is False


@pytest.mark.asyncio
async def test_get_login_state_anonymous():
    async with utils.get_client() as client:
        assert await client.get_login_state() is None


@pytest.mark.asyncio
async def test_get_dir_for():
    async with utils.get_client() as client:
        course = data.COURSE_74
        dir_ = client.get_dir_for(course)
        assert dir_.exists()
