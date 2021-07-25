import os
import subprocess

import nox

nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = ['format', 'lint', 'test']

FILES = ['ilmsdump', 'ilmsserve', 'tests', 'noxfile.py', 'setup.py']


@nox.session
@nox.parametrize('formatter', ['isort', 'black'])
def format_check(session, formatter):
    session.install(formatter)
    session.run(formatter, '--check', '--diff', *FILES)


@nox.session
@nox.parametrize('formatter', ['isort', 'black'])
def format(session, formatter):
    session.install(formatter)
    session.run(formatter, *FILES)


@nox.session
def lint(session):
    session.install('flake8')
    session.run('flake8', *FILES)


@nox.session
def test(session):
    session.install('-U', '.[dev]')
    session.run('python', '-m', 'pytest', 'tests')


@nox.session
def test_ilmsmock(session):
    session.install('-U', '.[dev]')
    session.run('go', 'install', 'github.com/afq984/ilmsmock/cmd/ilmsmock@latest', external=True)
    gopath = subprocess.check_output(['go', 'env', 'GOPATH']).decode('utf-8').strip()
    ilmsmock = os.path.join(gopath, 'bin', 'ilmsmock')
    if os.name == 'nt':
        ilmsmock += '.exe'
    session.run(
        ilmsmock,
        '--setenv=ILMSDUMP_TARGET_ORIGIN',
        '--',
        'python',
        '-m',
        'pytest',
        'tests',
        external=True,
    )
