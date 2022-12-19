from __future__ import annotations

import os

import nox


nox.options.sessions = ["pre_commit", "docs", "typecheck", "tests"]
nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = True


@nox.session
def pre_commit(session: nox.Session) -> None:
    session.install("pre-commit")

    session.run("pre-commit", "run", "--all-files", "--show-diff-on-failure")


@nox.session(python=["pypy3.7", "pypy3.8", "3.7", "3.8", "3.9", "3.10", "3.11"])
def tests(session: nox.Session) -> None:
    session.install("Twisted", "coverage[toml]")
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

    if os.environ.get("CI") != "true":
        session.notify("coverage_report")
    else:
        session.run("coverage", "combine")


@nox.session
def coverage_report(session: nox.Session) -> None:
    session.install("coverage[toml]")

    session.run("coverage", "combine")
    session.run("coverage", "report")


@nox.session
def check_newsfragment(session: nox.Session) -> None:
    session.install(".")
    session.run("python", "-m", "towncrier.check", "--compare-with", "origin/trunk")


@nox.session
def check_manifest(session: nox.Session) -> None:
    session.install("check-manifest")
    session.run("check-manifest")


@nox.session
def typecheck(session: nox.Session) -> None:
    session.install(".", "mypy", "types-setuptools")
    session.run("mypy", "src")


@nox.session
def docs(session: nox.Session) -> None:
    session.install(".[dev]")

    session.run(
        # fmt: off
        "python", "-m", "sphinx",
        "-T", "-E",
        "-W", "--keep-going",
        "-b", "html",
        "-d", "docs/_build/doctrees",
        "-D", "language=en",
        "docs",
        "docs/_build/html",
        # fmt: on
    )


@nox.session
def build(session: nox.Session) -> None:
    session.install("build", "check-manifest>=0.44", "twine")

    session.run("check-manifest", "--verbose")
    # If no argument is passed, build builds an sdist and then a wheel from
    # that sdist.
    session.run("python", "-m", "build")

    session.run("twine", "check", "dist/*")
