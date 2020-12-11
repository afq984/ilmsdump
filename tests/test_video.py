import hashlib

import pytest

import ilmsdump

from tests import data


@pytest.mark.asyncio
async def test_download(client: ilmsdump.Client):
    assert [c async for c in data.VIDEO_1518.download(client)] == []

    file = client.get_dir_for(data.VIDEO_1518) / 'video.mp4'
    b = file.read_bytes()
    assert (
        hashlib.sha256(b).hexdigest()
        == 'c926d4375794d4a1b56cf5bc0f323dda10d45fbd3e93f2779b4f8af86f2d970d'
    )

    assert client.bytes_downloaded == len(b)
