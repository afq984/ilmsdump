import pytest

import ilmsdump
from tests import data


@pytest.mark.asyncio
async def test_downlaod(client: ilmsdump.Client):
    attachments = [a async for a in data.MATERIAL_2173495.download(client)]

    assert (client.get_dir_for(data.MATERIAL_2173495) / 'index.html').exists()

    assert attachments == [data.ATTACHMENT_2107249]


@pytest.mark.asyncio
async def test_downlaod_powercam(client: ilmsdump.Client):
    attachments = [a async for a in data.MATERIAL_1518.download(client)]

    assert (client.get_dir_for(data.MATERIAL_1518) / 'index.html').exists()

    assert attachments == [data.VIDEO_1518]


@pytest.mark.asyncio
async def test_download_invalid(client: ilmsdump.Client):
    invalid_material = ilmsdump.Material(
        id=0,
        title='invalid material',
        type='Econtent',
        course=data.COURSE_74,
    )

    with pytest.raises(ilmsdump.Unavailable):
        [a async for a in invalid_material.download(client)]
