# Copyright (c) Amber Brown, 2018
# See LICENSE for details.


from __future__ import annotations

import os
import sys

from subprocess import CalledProcessError
from typing import Container
from warnings import warn

import click

from ._builder import find_fragments
from ._git import get_remote_branches, list_changed_files_compared_to_branch
from ._settings import config_option_help, load_config_from_options


def _get_default_compare_branch(branches: Container[str]) -> str | None:
    if "origin/main" in branches:
        return "origin/main"
    if "origin/master" in branches:
        warn(
            'Using "origin/master" as default compare branch is deprecated '
            "and will be removed in a future version.",
            DeprecationWarning,
            stacklevel=2,
        )
        return "origin/master"
    return None


@click.command(name="check")
@click.option(
    "--compare-with",
    default=None,
    metavar="BRANCH",
    help=(
        "Checks files changed running git diff --name-only BRANCH... "
        "BRANCH is the branch to be compared with. "
        "Default to origin/main"
    ),
)
@click.option(
    "--dir",
    "directory",
    default=None,
    metavar="PATH",
    help="Check fragment in directory. Default to current directory.",
)
@click.option(
    "--config",
    "config",
    default=None,
    metavar="FILE_PATH",
    help=config_option_help,
)
def _main(compare_with: str | None, directory: str | None, config: str | None) -> None:
    """
    Check for new fragments on a branch.
    """
    __main(compare_with, directory, config)


def __main(
    comparewith: str | None, directory: str | None, config_path: str | None
) -> None:
    base_directory, config = load_config_from_options(directory, config_path)

    if comparewith is None:
        comparewith = _get_default_compare_branch(
            get_remote_branches(base_directory=base_directory)
        )

    if comparewith is None:
        click.echo("Could not detect default branch. Aborting.")
        sys.exit(1)

    try:
        files_changed = list_changed_files_compared_to_branch(
            base_directory, comparewith
        )
    except CalledProcessError as e:
        click.echo("git produced output while failing:")
        click.echo(e.output)
        raise

    if not files_changed:
        click.echo(
            f"On {comparewith} branch, or no diffs, so no newsfragment required."
        )
        sys.exit(0)

    files = {os.path.abspath(path) for path in files_changed}

    click.echo("Looking at these files:")
    click.echo("----")
    for n, change in enumerate(files, start=1):
        click.echo(f"{n}. {change}")
    click.echo("----")

    news_file = os.path.normpath(os.path.join(base_directory, config.filename))
    if news_file in files:
        click.echo("Checks SKIPPED: news file changes detected.")
        sys.exit(0)

    if config.directory:
        fragment_base_directory = os.path.abspath(
            os.path.join(base_directory, config.directory)
        )
        fragment_directory = None
    else:
        fragment_base_directory = os.path.abspath(
            os.path.join(base_directory, config.package_dir, config.package)
        )
        fragment_directory = "newsfragments"

    fragments = {
        os.path.abspath(path)
        for path in find_fragments(
            fragment_base_directory,
            config.sections,
            fragment_directory,
            config.types.keys(),
        )[1]
    }
    fragments_in_branch = fragments & files

    if not fragments_in_branch:
        click.echo("No new newsfragments found on this branch.")
        sys.exit(1)
    else:
        click.echo("Found:")
        for n, fragment in enumerate(fragments_in_branch, start=1):
            click.echo(f"{n}. {fragment}")
        sys.exit(0)


if __name__ == "__main__":  # pragma: no cover
    _main()
