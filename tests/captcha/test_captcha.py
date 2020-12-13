import pathlib

import pytest
from PIL import Image

from ilmsdump import captcha

HERE = pathlib.Path(__file__).parent.resolve()


def test_hamming_weight():
    """
    Test case from:
    https://github.com/python/cpython/pull/20518/files#diff-687f4a736f1f6ad4b6cd4ff65c8e0113408304e8d65530dbd41b3f59a081a126R92-R98
    """
    assert captcha.hamming_weight(0) == 0
    assert captcha.hamming_weight(1) == 1
    assert captcha.hamming_weight(0x08080808) == 4
    assert captcha.hamming_weight(0x10101010) == 4
    assert captcha.hamming_weight(0x10204080) == 4
    assert captcha.hamming_weight(0xDEADCAFE) == 22
    assert captcha.hamming_weight(0xFFFFFFFF) == 32
    assert captcha.hamming_weight(0xFFFFFFFFDEADCAFE1020408010101010) == 62


def test_match():
    for digit in '123456789':
        filename = HERE / f'{digit}.jpg'
        im = Image.open(filename)
        assert captcha.match(im) == digit


@pytest.mark.asyncio
async def test_test():
    """
    make sure it works
    """
    await captcha.test()
