import os
from dotenv import load_dotenv

import nox


load_dotenv()

nox.options.reuse_existing_virtualenvs = False
#nox.options.sessions = ['build']


@nox.session(
    python=['3.8', '3.9', '3.10', '3.11', '3.12', '3.13'],
)
def tests(session):
    session.install("-e", ".")  # Install the package in the virtualenv
    session.install('-r', 'requirements.txt')
    session.install('-r', 'requirements-dev.txt')
    session.run('pytest')


@nox.session(python=['3.13'], requires=["tests-{python}"])
def coverage(session):
    session.install("-e", ".")  # Install the package in the virtualenv
    session.install('-r', 'requirements.txt')
    session.install('-r', 'requirements-dev.txt')
    session.install("coverage")
    session.run("coverage", 'run', '-m', 'pytest')
    session.run("coverage", 'report')
    session.run("coverage", 'xml')
    session.run("coverage", 'html')


@nox.session
def lint(session):
    session.install("-e", ".")  # Install the package in the virtualenv
    session.install('flake8')
    session.install('black')
    session.install('isort')
    session.install('pylint')
    session.run('flake8', 'src', 'tests')
    session.run('black', 'src', 'tests')
    session.run("isort", "--profile", "black", "src")
    session.run("pylint", "src")


@nox.session
def type_check(session):
    session.install("-e", ".")  # Install the package in the virtualenv
    session.install('mypy')
    session.run('mypy', '--install-types', '--non-interactive')
    session.run('mypy', 'src', 'tests')


@nox.session
def docs(session):
    session.install("-e", ".")  # Install the package in the virtualenv
    session.install('sphinx')
    session.run('sphinx-build', '-b', 'html', 'docs/', 'build/docs')


@nox.session
def build(session):
    session.install("-e", ".")  # Install the package in the virtualenv
    session.install('build')
    session.run('python', '-m', 'build')


@nox.session(requires=["build"], default=False)
def publish(session):
    pypi_user: str = os.environ.get("PYPI_USER")
    pypi_pass: str = os.environ.get("PYPI_PASS")
    if not pypi_user or not pypi_pass:
        session.error(
            "Environment variables for release: PYPI_USER, PYPI_PASS are missing!",
        )

    session.install("twine")
    session.run("twine", "upload", '-u', pypi_user, '-p', pypi_pass, "dist/*")


