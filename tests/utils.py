import tempfile
import contextlib

from typing import AsyncGenerator

import ilmsdump


COURSE_74 = ilmsdump.Course(
    id=74,
    serial='0001',
    name='iLMS平台線上客服專區',
    is_admin=False,
)

COURSE_46274 = ilmsdump.Course(
    id=46274, serial='10910CS542200', name='平行程式Parallel Programming', is_admin=False
)


@contextlib.asynccontextmanager
async def get_client() -> AsyncGenerator[ilmsdump.Client, None]:
    with tempfile.TemporaryDirectory() as tmpd:
        async with ilmsdump.Client(data_dir=tmpd) as client:
            yield client
