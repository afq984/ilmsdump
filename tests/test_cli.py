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
