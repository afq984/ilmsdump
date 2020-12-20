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
