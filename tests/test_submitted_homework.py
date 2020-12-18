import pytest

import ilmsdump
from tests import data


@pytest.mark.asyncio
async def test_download(client: ilmsdump.Client):
    assert [a async for a in data.SUBMITTED_2474481.download(client)] == [data.ATTACHMENT_2406879]

    assert (client.get_dir_for(data.SUBMITTED_2474481) / 'index.html').exists()


@pytest.mark.asyncio
async def test_group_download(client: ilmsdump.Client):
    assert [a async for a in data.SUBMITTED_59376.download(client)] == [data.ATTACHMENT_49113]

    assert (client.get_dir_for(data.SUBMITTED_59376) / 'index.html').exists()
