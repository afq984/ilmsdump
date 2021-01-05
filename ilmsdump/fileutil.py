"""
This module implemnts
"""

import unicodedata


def is_illegal_anywhere(c: str):
    """
    IllegalCharacters::IllegalCharacters()
    https://source.chromium.org/chromium/chromium/src/+/master:base/i18n/file_util_icu.cc;l=66;drc=e45616a746204e7405d3e2414675978597817414
    """
    i = ord(c)
    return (
        c in R'"~*/:<>??\|'
        or unicodedata.category(c) in {'Cc', 'Cf'}
        or 0xFDD0 <= i <= 0xFDEF
        or any(
            plane_base + 0xFFFE <= i <= plane_base + 0xFFFF
            for plane_base in range(0, 0x110000, 0x10000)
        )
    )


def is_illegal_at_ends(c: str):
    """
    IllegalCharacters::IllegalCharacters()
    https://source.chromium.org/chromium/chromium/src/+/master:base/i18n/file_util_icu.cc;l=66;drc=e45616a746204e7405d3e2414675978597817414
    """
    return c.isspace() or c == '.'


def replace_illegal_characters_in_path(file_name: str, replace_char: str):
    """
    ReplaceIllegalCharactersInPath()
    https://source.chromium.org/chromium/chromium/src/+/master:base/i18n/file_util_icu.cc;l=105;drc=e45616a746204e7405d3e2414675978597817414
    """
    return ''.join(
        replace_char
        if (
            is_illegal_anywhere(c)
            or ((i == 0 or i + 1 == len(file_name)) and is_illegal_at_ends(c))
        )
        else c
        for (i, c) in enumerate(file_name)
    )
