import pytest

import ilmsdump
from tests import data


@pytest.mark.asyncio
async def test_download(client: ilmsdump.Client):
    attachments = [a async for a in data.HOMEWORK_201015.download(client)]

    assert (client.get_dir_for(data.HOMEWORK_201015) / 'index.html').exists()

    assert attachments == [
        data.ATTACHMENT_2038513,
        data.ATTACHMENT_2047732,
    ]


@pytest.mark.asyncio
async def test_download_invalid(client: ilmsdump.Client):
    invalid_homework = ilmsdump.Homework(
        id=0,
        title='invalid homework',
        course=data.COURSE_74,
    )

    with pytest.raises(ilmsdump.Unavailable):
        [a async for a in invalid_homework.download(client)]


@pytest.mark.asyncio
async def test_download_with_submissions(client: ilmsdump.Client):
    attachments = [a async for a in data.HOMEWORK_182409.download(client)]

    assert (client.get_dir_for(data.HOMEWORK_182409) / 'index.html').exists()

    assert len(attachments) >= 50
    assert all(isinstance(a, ilmsdump.SubmittedHomework) for a in attachments)


@pytest.mark.asyncio
async def test_download_multiple_div_id_main(client: ilmsdump.Client):
    # just make sure it runs
    [a async for a in data.HOMEWORK_183084.download(client)]

    assert (client.get_dir_for(data.HOMEWORK_183084) / 'index.html').exists()


@pytest.mark.asyncio
async def test_download_open_submission(client: ilmsdump.Client):
    children = [c async for c in data.HOMEWORK_220144.download(client)]

    assert data.SUBMITTED_2474481 in children


@pytest.mark.asyncio
async def test_download_open_group_submission(client: ilmsdump.Client):
    assert [c async for c in data.HOMEWORK_18264.download(client)] == [data.SUBMITTED_59376]


@pytest.mark.asyncio
async def test_donload_a_without_content(client: ilmsdump.Client):
    assert [c async for c in data.HOMEWORK_32460.download(client)] == [data.ATTACHMENT_133807]
