import pytest
import tempfile

import ilmsdump


@pytest.mark.asyncio
async def test_anonymous():
    with tempfile.TemporaryDirectory() as tmpd:
        async with ilmsdump.Client(data_dir=tmpd) as client:
            course = await client.get_course(46274)
            assert course.id == 46274
            assert course.name == '平行程式Parallel Programming'
            assert course.is_admin is False
