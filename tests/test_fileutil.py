import pytest

import ilmsdump.fileutil


@pytest.mark.parametrize(
    'bad_name,good_name',
    [
        ["bad*file:name?.jpg", "bad-file-name-.jpg"],
        ["**********::::.txt", "--------------.txt"],
        ["bad\u0003\u0091 file\u200E\u200Fname.png", "bad-- file--name.png"],
        ["bad*file\\?name.jpg", "bad-file--name.jpg"],
        ["\t  bad*file\\name/.jpg", "-  bad-file-name-.jpg"],
        ["this_file_name is okay!.mp3", "this_file_name is okay!.mp3"],
        ["\u4E00\uAC00.mp3", "\u4E00\uAC00.mp3"],
        ["\u0635\u200C\u0644.mp3", "\u0635-\u0644.mp3"],
        ["\U00010330\U00010331.mp3", "\U00010330\U00010331.mp3"],
        # Unassigned codepoints are ok.
        ["\u0378\U00040001.mp3", "\u0378\U00040001.mp3"],
        # Non-characters are not allowed.
        ["bad\uFFFFfile\U0010FFFEname.jpg", "bad-file-name.jpg"],
        ["bad\uFDD0file\uFDEFname.jpg", "bad-file-name.jpg"],
        # CVE-2014-9390
        [
            "(\u200C.\u200D.\u200E.\u200F.\u202A.\u202B.\u202C.\u202D.\u202E.\u206A."
            "\u206B.\u206C.\u206D.\u206F.\uFEFF)",
            "(-.-.-.-.-.-.-.-.-.-.-.-.-.-.-)",
        ],
        ["config~1", "config-1"],
        [" _ ", "-_-"],
        [" ", "-"],
        ["\u2008.(\u2007).\u3000", "-.(\u2007).-"],
        ["     ", "-   -"],
        [".    ", "-   -"],
    ],
)
def test_replace_illegal_characters_in_path(bad_name, good_name):
    """
    https://source.chromium.org/chromium/chromium/src/+/master:base/i18n/file_util_icu_unittest.cc;l=52-87;drc=000df18f71b5eddeafbb3e07648f5fb55e464e13
    """
    assert ilmsdump.fileutil.replace_illegal_characters_in_path(bad_name, '-') == good_name
