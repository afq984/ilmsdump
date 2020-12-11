import pytest

import ilmsdump

from tests import data


ATTACHMENT_2616319_CONTENT = '''\
HW3 成績已公佈
請到 iLMS 查看

各項得分在 iLMS 的評語內
說明：
[C]orrectness, w: 錯的測資數量
[P]erformance, t: 執行總時間
[T]estcase, t: 除了自己以外的執行總時間
[D]emo
[R]eport
[L]inearAdjustment

如有疑問請與助教聯絡
'''


@pytest.mark.asyncio
async def test_download(client: ilmsdump.Client):
    assert [c async for c in data.ATTACHMENT_2616319.download(client)] == []

    file = client.get_dir_for(data.ATTACHMENT_2616319) / 'data'
    assert file.read_text(encoding='utf8') == ATTACHMENT_2616319_CONTENT

    assert client.bytes_downloaded == file.stat().st_size
