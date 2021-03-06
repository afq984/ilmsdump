import os
import pathlib
import pickle
import tempfile

import click.testing
import pytest

import ilmsdump
from tests import data


@pytest.fixture(scope='function')
def tempdir():
    with tempfile.TemporaryDirectory() as tmpd:
        yield tmpd


def test_nothing_to_do(tempdir):
    runner = click.testing.CliRunner(mix_stderr=False)
    result = runner.invoke(ilmsdump.main, ['--output-dir', tempdir])
    assert result.stderr == 'Nothing to do\n'


def test_logout(tempdir):
    cred_file = os.path.join(tempdir, 'credentials.txt')
    pathlib.Path(cred_file).touch()

    runner = click.testing.CliRunner(mix_stderr=False)
    result = runner.invoke(ilmsdump.main, ['--output-dir', tempdir, '--logout'])

    assert not os.path.exists(cred_file)
    assert 'Removed' in result.stdout


def test_anonymous(tempdir):
    cred_file = os.path.join(tempdir, 'credentials.txt')
    pathlib.Path(cred_file).touch()

    runner = click.testing.CliRunner(mix_stderr=False)
    result = runner.invoke(ilmsdump.main, ['--output-dir', tempdir, '--anonymous'])
    assert result.stdout == ''
    assert result.stderr == 'Nothing to do\n'


def test_download(tempdir):
    """
    very basic download test
    """

    runner = click.testing.CliRunner(mix_stderr=False)
    runner.invoke(ilmsdump.main, ['--output-dir', tempdir, '399'])

    # https://lms.nthu.edu.tw/course/399
    # open course having no attachments

    for sub in [
        'course/399/index.html',
        'course/399/meta.json',
        'announcement/2714/index.json',
        'announcement/2714/meta.json',
    ]:
        assert os.path.exists(os.path.join(tempdir, sub))


def test_resume(tempdir):
    resume_file = os.path.join(tempdir, 'resmue.pickle')
    with open(resume_file, 'wb') as file:
        pickle.dump({'items': [data.COURSE_399], 'ignore': []}, file)

    runner = click.testing.CliRunner(mix_stderr=False)
    runner.invoke(ilmsdump.main, ['--output-dir', tempdir, '--resume', resume_file])

    for sub in [
        'course/399/index.html',
        'course/399/meta.json',
        'announcement/2714/index.json',
        'announcement/2714/meta.json',
    ]:
        assert os.path.exists(os.path.join(tempdir, sub))


def test_resume_check(tempdir):
    resume_file = os.path.join(tempdir, 'resmue.pickle')
    with open(resume_file, 'wb') as file:
        pickle.dump({'items': [data.COURSE_399], 'ignore': []}, file)

    runner = click.testing.CliRunner(mix_stderr=False)

    result = runner.invoke(ilmsdump.main, ['--output-dir', tempdir, '--resume', resume_file, '399'])
    assert isinstance(result.exception, ilmsdump.CLISystemExit)


def test_no_resume_check(tempdir):
    resume_file = os.path.join(tempdir, 'resmue.pickle')
    with open(resume_file, 'wb') as file:
        pickle.dump({'items': [data.COURSE_399], 'ignore': []}, file)

    runner = click.testing.CliRunner(mix_stderr=False)

    result = runner.invoke(
        ilmsdump.main,
        ['--output-dir', tempdir, '--resume', resume_file, '399', '--no-resume-check', '--dry'],
    )

    assert result.exception is None


def test_ignore(tempdir):
    runner = click.testing.CliRunner(mix_stderr=False)
    runner.invoke(ilmsdump.main, ['--output-dir', tempdir, '399', '--ignore', 'Announcement'])

    for sub in [
        'course/399/index.html',
        'course/399/meta.json',
    ]:
        assert os.path.exists(os.path.join(tempdir, sub))

    for sub in [
        'announcement/2714/index.json',
        'announcement/2714/meta.json',
    ]:
        assert not os.path.exists(os.path.join(tempdir, sub))


def test_ignore_item(tempdir):
    runner = click.testing.CliRunner(mix_stderr=False)
    runner.invoke(ilmsdump.main, ['--output-dir', tempdir, '399', '--ignore', 'Announcement-2714'])

    for sub in [
        'course/399/index.html',
        'course/399/meta.json',
    ]:
        assert os.path.exists(os.path.join(tempdir, sub))

    for sub in [
        'announcement/2714/index.json',
        'announcement/2714/meta.json',
    ]:
        assert not os.path.exists(os.path.join(tempdir, sub))


def test_dry(tempdir):
    runner = click.testing.CliRunner(mix_stderr=False)
    runner.invoke(ilmsdump.main, ['--output-dir', tempdir, '399', '--dry'])

    for sub in [
        'course/399/index.html',
        'course/399/meta.json',
        'announcement/2714/index.json',
        'announcement/2714/meta.json',
    ]:
        assert not os.path.exists(os.path.join(tempdir, sub))
