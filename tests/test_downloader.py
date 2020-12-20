import dataclasses
import pickle
from typing import List

import pytest

import ilmsdump


@dataclasses.dataclass
class Item(ilmsdump.Downloadable):
    STATS_NAME = 'Item'

    id: int
    children: List[ilmsdump.Downloadable]
    downloaded: int = 0

    async def download(self, client):
        self.downloaded += 1
        for child in self.children:
            yield child


class ItemFails(Item):
    async def download(self, client):
        async for child in super().download(client):
            yield
        raise Exception


@pytest.mark.asyncio
async def test_download(client: ilmsdump.Client):
    d3 = Item(3, [])
    d2 = Item(2, [d3])
    d1 = Item(1, [d2])

    downloader = ilmsdump.Downloader(client=client)

    await downloader.run([d1])

    assert d1.downloaded == 1
    assert d2.downloaded == 1
    assert d3.downloaded == 1


@pytest.mark.asyncio
async def test_ignore(client: ilmsdump.Client):
    d3 = Item(3, [])
    d2 = Item(2, [d3])
    d1 = Item(1, [d2])

    downloader = ilmsdump.Downloader(client=client)

    await downloader.run([d1], {'Item'})

    assert d1.downloaded == 0
    assert d2.downloaded == 0
    assert d3.downloaded == 0


@pytest.mark.asyncio
async def test_generates_resume(client: ilmsdump.Client):
    d3 = Item(3, [])
    d2 = ItemFails(2, [d3])
    d1 = Item(1, [d2])

    downloader = ilmsdump.Downloader(client=client)

    with pytest.raises(ilmsdump.DownloadFailed) as exc:
        await downloader.run([d1], {'GarbageString'})

    assert d1.downloaded == 1
    assert d2.downloaded == 1
    assert d3.downloaded == 0

    (resume_file,) = client.data_dir.glob('resume-*.pickle')

    assert resume_file.name in exc.value.args[0]

    with resume_file.open('rb') as file:
        resume_data = pickle.load(file)

    assert [*resume_data['items']] == [d2]
    assert resume_data['ignore'] == {'GarbageString'}
