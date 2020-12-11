import tempfile
import os

import pytest
import click.testing

import ilmsdump


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
    open(cred_file, 'w').close()

    runner = click.testing.CliRunner(mix_stderr=False)
    result = runner.invoke(ilmsdump.main, ['--output-dir', tempdir, '--logout'])

    assert not os.path.exists(cred_file)
    assert 'Removed' in result.stdout
