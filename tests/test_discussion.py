import pytest

import ilmsdump
from tests import data


@pytest.mark.asyncio
async def test_downlaod(client: ilmsdump.Client):
    attachments = [a async for a in data.DISCUSSION_258543.download(client)]

    assert (client.get_dir_for(data.DISCUSSION_258543) / 'index.json').exists()

    assert data.ATTACHMENT_2134734 in attachments
    assert data.ATTACHMENT_2134738 in attachments


@pytest.mark.asyncio
async def test_download_invalid(client: ilmsdump.Client):
    discussion = ilmsdump.Discussion(id=0, title='invalid discussion', course=data.COURSE_74)

    with pytest.raises(ilmsdump.CannotUnderstand):
        [a async for a in discussion.download(client)]
