import pytest

import ilmsdump

from tests import data


@pytest.mark.asyncio
async def test_downlaod(client: ilmsdump.Client):
    attachments = [a async for a in data.ANNOUNCEMENT_2218728.download(client)]

    assert (client.get_dir_for(data.ANNOUNCEMENT_2218728) / 'index.json').exists()

    assert attachments == [data.ATTACHMENT_2616319, data.ATTACHMENT_2616320]


@pytest.mark.asyncio
async def test_download_invalid(client: ilmsdump.Client):
    invalid_announcement = ilmsdump.Announcement(
        id=0,
        title='invalid announcement',
        course=data.COURSE_74,
    )

    with pytest.raises(ilmsdump.Unavailable):
        [a async for a in invalid_announcement.download(client)]
