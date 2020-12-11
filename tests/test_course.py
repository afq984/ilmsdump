import pytest

from tests import data


@pytest.mark.asyncio
async def test_get_announcements(client):
    announcements = [a async for a in data.COURSE_40596.get_announcements(client)]

    assert data.ANNOUNCEMENT_2008652 in announcements
    assert data.ANNOUNCEMENT_2218728 in announcements


@pytest.mark.asyncio
async def test_get_discussions(client):
    discussions = [d async for d in data.COURSE_40596.get_discussions(client)]

    assert data.DISCUSSION_236608 in discussions
    assert data.DISCUSSION_258543 in discussions


@pytest.mark.asyncio
async def test_get_materials(client):
    materials = [m async for m in data.COURSE_40596.get_materials(client)]
    assert data.MATERIAL_2004666 in materials
    assert data.MATERIAL_2173495 in materials

    materials = [m async for m in data.COURSE_74.get_materials(client)]
    assert data.MATERIAL_258234 in materials


@pytest.mark.asyncio
async def test_get_homework(client):
    homeworks = [h async for h in data.COURSE_40596.get_homeworks(client)]

    assert data.HOMEWORK_198377 in homeworks
    assert data.HOMEWORK_200355 in homeworks
