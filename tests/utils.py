import tempfile
import contextlib

from typing import AsyncGenerator

import ilmsdump


@contextlib.asynccontextmanager
async def get_client() -> AsyncGenerator[ilmsdump.Client, None]:
    with tempfile.TemporaryDirectory() as tmpd:
        async with ilmsdump.Client(data_dir=tmpd) as client:
            yield client
