import ilmsdump

import pytest

from tests import data


@pytest.mark.asyncio
async def test_download(client: ilmsdump.Client):
    assert [a async for a in ilmsdump.GroupList(data.COURSE_46274).download(client)] == []

    assert (client.get_dir_for(ilmsdump.GroupList(data.COURSE_46274)) / 'index.html').exists()
