import pytest

import ilmsdump

from tests import data


@pytest.mark.asyncio
async def test_get_announcements(client):
    announcements = [a async for a in data.COURSE_40596.get_announcements(client)]

    assert data.ANNOUNCEMENT_2008652 in announcements
    assert data.ANNOUNCEMENT_2218728 in announcements


@pytest.mark.asyncio
async def test_get_announcements_empty(client):
    assert [a async for a in data.COURSE_1808.get_announcements(client)] == []


@pytest.mark.asyncio
async def test_get_discussions(client):
    discussions = [d async for d in data.COURSE_40596.get_discussions(client)]

    assert data.DISCUSSION_236608 in discussions
    assert data.DISCUSSION_258543 in discussions


@pytest.mark.asyncio
async def test_get_discussions_empty(client):
    assert [d async for d in data.COURSE_1808.get_discussions(client)] == []


@pytest.mark.asyncio
async def test_get_materials(client):
    materials = [m async for m in data.COURSE_40596.get_materials(client)]
    assert data.MATERIAL_2004666 in materials
    assert data.MATERIAL_2173495 in materials

    materials = [m async for m in data.COURSE_74.get_materials(client)]
    assert data.MATERIAL_1518 in materials


@pytest.mark.asyncio
async def test_get_materials_empty(client):
    assert [m async for m in data.COURSE_359.get_materials(client)] == []


@pytest.mark.asyncio
async def test_get_homework(client):
    homeworks = [h async for h in data.COURSE_40596.get_homeworks(client)]

    assert data.HOMEWORK_198377 in homeworks
    assert data.HOMEWORK_200355 in homeworks


@pytest.mark.asyncio
async def test_get_homework_empty(client):
    assert [h async for h in data.COURSE_1808.get_homeworks(client)] == []


@pytest.mark.asyncio
async def test_get_score_empty(client):
    assert [s async for s in data.COURSE_74.get_scores(client)] == []


@pytest.mark.asyncio
async def test_get_grouplist(client):
    assert [g async for g in data.COURSE_40596.get_grouplists(client)] == [data.GROUPLIST_40596]


@pytest.mark.asyncio
async def test_get_grouplist_empty(client):
    assert [g async for g in data.COURSE_1808.get_grouplists(client)] == []


@pytest.mark.asyncio
async def test_download(client: ilmsdump.Client):
    items = [i async for i in data.COURSE_40596.download(client)]

    assert (client.get_dir_for(data.COURSE_40596) / 'index.html').exists()

    assert data.ANNOUNCEMENT_2008652 in items
    assert data.ANNOUNCEMENT_2218728 in items
    assert data.DISCUSSION_258543 in items
    assert data.DISCUSSION_236608 in items
    assert data.MATERIAL_2173495 in items
    assert data.MATERIAL_2004666 in items
    assert data.HOMEWORK_198377 in items
    assert data.HOMEWORK_200355 in items
    assert data.GROUPLIST_40596 in items
