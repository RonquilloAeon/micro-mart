import nox
from nox_poetry import session

nox.options.sessions = ["format", "lint", "test"]


@nox.session(python="3.11", reuse_venv=True)
def format(session):
    session.install("black")
    session.run("black", "iam/src", "noxfile.py", *session.posargs)


@nox.session(python="3.11", reuse_venv=True)
def lint(session):
    session.install("flake8")
    session.run("flake8", "iam/src")


@session(python="3.11", reuse_venv=True)
def test(local_session):
    local_session.run_always("poetry", "install", external=True)

    # IAM
    local_session.run(
        "python",
        "iam/src/manage.py",
        "test",
        "--keepdb",
        *local_session.posargs,
        env={"DB_NAME": "test_mm"},
    )
