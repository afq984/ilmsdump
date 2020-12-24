import asyncio
import base64
import io
import logging
import random
from typing import Optional

import aiohttp
from PIL import Image

logger = logging.getLogger(__name__)

WIDTH = 16
HEIGHT = 26
SIZE = WIDTH * HEIGHT

MATCHERS = [
    ('1', 0x3800380038001800380038003800380038003800380038003B003E003E0030000000000000000000),
    ('2', 0x3FC03FC00F800380038007000E000E001C001C001800380038E038E01DC01FC00700000000000000),
    ('3', 0xF001F801DC038E038E03800380018000C000C0018003800380038C01DC01F800700000000000000),
    ('4', 0x1C001C001C001C003FE03FE03CE01C601C401C801CC01D801D001D001F001F001E00000000000000),
    ('5', 0x3000FC01FE018C03800380018001CA01DE00FE006E000E000E000E016E01FE01FE0000000000000),
    ('6', 0xF001F801DC018C038E038E038E018E03FC00FC0018003800300070006000E000E00000000000000),
    ('7', 0xC001C001C001800380030003000300060006000E000E000C000C001EA01FE01FE0000000000000),
    ('8', 0x7801F801FC038C038E038E038E03DC01FC00F801DC018C038E038E01DC01FC00F80000000000000),
    ('9', 0x1C001800300070006000E000C001F001FC01FE038E038E018E038C01DC01F800700000000000000),
]


def process(im):
    return sum((px < 80) << i for i, px in enumerate(im.convert('L').tobytes()))


def to_data_uri(bin: bytes, content_type: str):
    b64str = base64.b64encode(bin).decode('ascii')
    return f'data:{content_type};base64,{b64str}'


def hamming_weight(value: int) -> int:
    return f'{value:b}'.count('1')


def match(bin: bytes, content_type: Optional[str] = None):
    im = Image.open(io.BytesIO(bin))
    logger.info('Processing image:')
    if content_type is None:
        content_type = Image.MIME[im.format]
    logger.info(to_data_uri(bin, content_type))
    p = process(im)
    matches, digit = max(
        (
            SIZE - hamming_weight(p ^ matcher),
            digit,
        )
        for (digit, matcher) in MATCHERS
    )
    score = matches / SIZE
    logger.info(f'Matched as {digit}, score={score:.4f}')
    return digit


def request(session: aiohttp.ClientSession):
    return session.get(
        'https://lms.nthu.edu.tw/sys/lib/class/csecimg.php',
        params={
            'width': WIDTH,
            'height': HEIGHT,
            'characters': 1,
            'rk': str(random.random()),
        },
    )


async def test():
    logging.basicConfig(level=logging.INFO)
    async with aiohttp.ClientSession() as session:
        async with request(session) as response:
            b = await response.read()
    match(b, response.content_type)


if __name__ == '__main__':
    asyncio.run(test())
