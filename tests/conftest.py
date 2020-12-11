import tempfile

import pytest

import ilmsdump


@pytest.fixture(scope='function')
async def client():
    with tempfile.TemporaryDirectory() as tmpd:
        async with ilmsdump.Client(data_dir=tmpd) as client:
            yield client
