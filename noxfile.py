import nox
from nox_poetry import session

nox.options.sessions = ["format", "lint", "test"]


@nox.session(python="3.11", reuse_venv=True)
def format(session):
    session.install("black")
    session.run("black", "src", "noxfile.py", *session.posargs)


@nox.session(python="3.11", reuse_venv=True)
def lint(session):
    session.install("flake8")
    session.run("flake8", "src")


@session(python="3.11", reuse_venv=True)
def test(local_session):
    local_session.run_always("poetry", "install", external=True)

    # IAM
    local_session.run(
        "python",
        "iam/manage.py",
        "test",
        "src",
        "-v 2",
        "--keepdb",
        *local_session.posargs,
        env={

        },
    )
