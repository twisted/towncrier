from __future__ import annotations

import nox


nox.options.sessions = ["pre_commit", "docs", "typecheck", "tests"]
nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = True
nox.needs_version = ">=2026.08.10"  # for allow_parallel
nox.options.default_venv_backend = "uv|virtualenv"


@nox.session(allow_parallel=True)
def pre_commit(session: nox.Session) -> None:
    session.install("pre-commit")

    session.run("pre-commit", "run", "--all-files", "--show-diff-on-failure")


# Keep list in-sync with ci.yml/test-linux & pyproject.toml
@nox.session(
    python=["pypy3.11", "3.11", "3.12", "3.13", "3.14", "3.15"], allow_parallel=True
)
def tests(session: nox.Session) -> None:
    session.env["PYTHONWARNDEFAULTENCODING"] = "1"
    session.install("Twisted", "coverage")
    posargs = list(session.posargs)

    try:
        # Allow `--use-wheel path/to/wheel.whl` to be passed.
        i = session.posargs.index("--use-wheel")
        session.install(session.posargs[i + 1])
        del posargs[i : i + 2]
    except ValueError:
        session.install(".")

    if not posargs:
        posargs = ["towncrier"]

    session.run("coverage", "run", "--module", "twisted.trial", *posargs)


@nox.session(requires=["tests"])
def coverage_report(session: nox.Session) -> None:
    session.install("coverage")

    session.run("coverage", "combine")
    session.run("coverage", "report")


@nox.session(allow_parallel=True)
def check_newsfragment(session: nox.Session) -> None:
    session.install(".")
    session.run("python", "-m", "towncrier.check", "--compare-with", "origin/trunk")


@nox.session
def draft_newsfragment(session: nox.Session) -> None:
    session.install(".")
    session.run("python", "-m", "towncrier.build", "--draft")


@nox.session(allow_parallel=True)
def typecheck(session: nox.Session) -> None:
    # Click 8.1.4 is bad type hints -- lets not complicate packaging and only
    # pin here.
    session.install(".", "mypy", "click!=8.1.4")
    session.run("mypy", "src")


@nox.session(allow_parallel=True)
def codespell(session: nox.Session) -> None:
    session.install(".", "codespell")
    session.run("codespell")


@nox.session(allow_parallel=True)
def docs(session: nox.Session) -> None:
    session.install(".[dev]")

    session.run(
        "python", "-m", "sphinx",
        "-T", "-E",
        "-W", "--keep-going",
        "-b", "html",
        "-d", "docs/_build/doctrees",
        "-D", "language=en",
        "docs",
        "docs/_build/html",
    )  # fmt: skip


@nox.session
def build(session: nox.Session) -> None:
    session.install("build", "twine", "pkginfo>=1.12.0")

    # If no argument is passed, build builds an sdist and then a wheel from
    # that sdist.
    session.run("python", "-m", "build")

    session.run("twine", "check", "--strict", "dist/*")
