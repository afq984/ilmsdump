import pytest

import ilmsdump
from tests import data


@pytest.mark.asyncio
async def test_download(client: ilmsdump.Client):
    # XXX: Not actually downloading a score table
    assert [a async for a in ilmsdump.Score(data.COURSE_74).download(client)] == []

    assert (client.get_dir_for(ilmsdump.Score(data.COURSE_74)) / 'index.html').exists()
