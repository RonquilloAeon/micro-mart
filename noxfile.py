import nox
from nox_poetry import session

nox.options.sessions = ["format", "lint", "test_iam", "test_retail"]


@nox.session(python="3.11", reuse_venv=True)
def format(session):
    session.install("black")
    session.run("black", "iam/src", "retail/src", "noxfile.py", *session.posargs)


@nox.session(python="3.11", reuse_venv=True)
def lint(session):
    session.install("flake8")
    session.run("flake8", "iam/src", "retail/src")


@session(python="3.11", reuse_venv=True)
def test_iam(local_session):
    local_session.run_always("poetry", "install", external=True)

    # IAM
    local_session.run(
        "python",
        "iam/src/manage.py",
        "test",
        "--keepdb",
        *local_session.posargs,
        env={
            "DB_HOST": "localhost",
            "DB_PASSWORD": "pgpass",
            "DB_PORT": "5432",
            "DB_NAME": "test_iam",
            "DB_USER": "mmadmin",
        },
    )


@session(python="3.11", reuse_venv=True)
def test_retail(local_session):
    local_session.run_always("poetry", "install", external=True)

    # IAM
    local_session.run(
        "python",
        "retail/src/manage.py",
        "test",
        "--keepdb",
        *local_session.posargs,
        env={
            "DB_HOST": "localhost",
            "DB_PASSWORD": "pgpass",
            "DB_PORT": "5432",
            "DB_NAME": "test_retail",
            "DB_USER": "mmadmin",
        },
    )
