# Copyright (c) Amber Brown, 2018
# See LICENSE for details.

from __future__ import absolute_import, division

import os
import sys

import click

from subprocess import (
    CalledProcessError,
    check_output,
    STDOUT,
)

from ._settings import load_config, load_config_from_file
from ._builder import find_fragments


def _run(args, **kwargs):
    kwargs["stderr"] = STDOUT
    return check_output(args, **kwargs)


@click.command()
@click.option("--compare-with", default="origin/master")
@click.option("--dir", "directory", default=".")
@click.option("--pyproject", "pyproject", default=None)
def _main(compare_with, directory, pyproject):
    return __main(compare_with, directory, pyproject)


def __main(comparewith, directory, pyproject):
    base_directory = os.path.abspath(directory)
    if pyproject is None:
        config = load_config(directory)
    else:
        config = load_config_from_file(pyproject)

    try:
        files_changed = (
            _run(["git", "diff", "--name-only", comparewith + "..."], cwd=base_directory)
            .decode(getattr(sys.stdout, "encoding", "utf8"))
            .strip()
        )
    except CalledProcessError as e:
        click.echo("git produced output while failing:")
        click.echo(e.output)
        raise

    if not files_changed:
        click.echo("On trunk, or no diffs, so no newsfragment required.")
        sys.exit(0)

    files = set(
        map(
            lambda x: os.path.join(base_directory, x),
            files_changed.strip().split(os.linesep),
        )
    )

    click.echo("Looking at these files:")
    click.echo("----")
    for n, change in enumerate(files, start=1):
        click.echo("{}. {}".format(n, change))
    click.echo("----")

    fragments = set()

    if config.get("directory"):
        base_directory = os.path.abspath(config["directory"])
        fragment_directory = None
    else:
        base_directory = os.path.abspath(
            os.path.join(directory, config["package_dir"], config["package"])
        )
        fragment_directory = "newsfragments"

    fragments = set(
        find_fragments(
            base_directory, config["sections"], fragment_directory, config["types"]
        )[1]
    )
    fragments_in_branch = fragments & files

    if not fragments_in_branch:
        click.echo("No new newsfragments found on this branch.")
        sys.exit(1)
    else:
        click.echo("Found:")
        for n, fragment in enumerate(fragments_in_branch, start=1):
            click.echo("{}. {}".format(n, fragment))
        sys.exit(0)


if __name__ == "__main__":  # pragma: no cover
    _main()
