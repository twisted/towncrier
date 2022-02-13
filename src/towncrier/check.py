# Copyright (c) Amber Brown, 2018
# See LICENSE for details.

from __future__ import absolute_import, division

import os
import sys

import click

from subprocess import CalledProcessError, check_output, STDOUT

from ._settings import load_config_from_options
from ._builder import find_fragments


def _run(args, **kwargs):
    kwargs["stderr"] = STDOUT
    return check_output(args, **kwargs)


@click.command(name="check")
@click.option("--compare-with", default="origin/master")
@click.option("--dir", "directory", default=None)
@click.option("--config", "config", default=None)
def _main(compare_with, directory, config):
    return __main(compare_with, directory, config)


def __main(comparewith, directory, config):

    base_directory, config = load_config_from_options(directory, config)

    # Use UTF-8 both when sys.stdout does not have .encoding (Python 2.7) and
    # when the attribute is present but set to None (explicitly piped output
    # and also some CI such as GitHub Actions).
    encoding = getattr(sys.stdout, "encoding", None)
    if encoding is None:
        encoding = "utf8"

    try:
        files_changed = (
            _run(
                ["git", "diff", "--name-only", comparewith + "..."], cwd=base_directory
            )
            .decode(encoding)
            .strip()
        )
    except CalledProcessError as e:
        click.echo("git produced output while failing:")
        click.echo(e.output)
        raise

    if not files_changed:
        click.echo("On trunk, or no diffs, so no newsfragment required.")
        sys.exit(0)

    files = {
        os.path.normpath(os.path.join(base_directory, path))
        for path in files_changed.strip().splitlines()
    }

    click.echo("Looking at these files:")
    click.echo("----")
    for n, change in enumerate(files, start=1):
        click.echo("{}. {}".format(n, change))
    click.echo("----")

    if config.get("directory"):
        fragment_base_directory = os.path.abspath(config["directory"])
        fragment_directory = None
    else:
        fragment_base_directory = os.path.abspath(
            os.path.join(base_directory, config["package_dir"], config["package"])
        )
        fragment_directory = "newsfragments"

    fragments = {
        os.path.normpath(path)
        for path in find_fragments(
            fragment_base_directory,
            config["sections"],
            fragment_directory,
            config["types"],
        )[1]
    }
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
