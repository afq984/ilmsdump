import os
import pathlib

import pytest

import ilmsdump
from tests import data


@pytest.mark.asyncio
async def test_get_course_anonymous(client):
    assert await client.get_course(46274) == data.COURSE_46274
    assert await client.get_course(74) == data.COURSE_74
    assert await client.get_course(40596) == data.COURSE_40596
    assert await client.get_course(1808) == data.COURSE_1808


@pytest.mark.asyncio
async def test_get_course_anonymous_doesnt_exist(client):
    with pytest.raises(ilmsdump.UserError):
        await client.get_course(0)


@pytest.mark.asyncio
async def test_get_courses_anonymous(client):
    with pytest.raises(ilmsdump.UserError):
        async for course in client.get_enrolled_courses():
            pass


@pytest.mark.asyncio
async def test_get_course_authentication_required(client):
    with pytest.raises(ilmsdump.UserError):
        await client.get_course(43477)


@pytest.mark.asyncio
async def test_clear_credentials(client):
    pathlib.Path(client.cred_path).touch()
    assert client.clear_credentials() is True
    assert not os.path.exists(client.cred_path)

    assert client.clear_credentials() is False


@pytest.mark.asyncio
async def test_get_login_state_anonymous(client):
    assert await client.get_login_state() is None


@pytest.mark.asyncio
async def test_login_with_username_and_password_invalid(client: ilmsdump.Client):
    with pytest.raises(ilmsdump.LoginFailed) as exc:
        await client.login_with_username_and_password('username', 'badpassword')

    exc_message = exc.value.args[0]
    print(exc_message)
    # make sure our captcha is correct
    assert exc_message['focus'] != 'loginSecCode'
    assert exc_message['msg'] != '您輸入的安全校驗碼不正確'
    assert exc_message['msg'] != 'You entered an incorrect number'


@pytest.mark.asyncio
async def test_login_with_phpsessid_invalid(client: ilmsdump.Client):
    with pytest.raises(ilmsdump.LoginFailed):
        await client.login_with_phpsessid('badsessid')


@pytest.mark.asyncio
async def test_get_dir_for(client):
    course = data.COURSE_74
    dir_ = client.get_dir_for(course)
    assert dir_.exists()


@pytest.mark.asyncio
async def test_get_open_courses(client: ilmsdump.Client):
    courses = [c async for c in client.get_open_courses(semester_id=38)]

    assert data.COURSE_40596 in courses
    assert len(courses) > 20
    assert all(isinstance(c, ilmsdump.Course) for c in courses)
