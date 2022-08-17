# Copyright (c) Amber Brown, 2018
# See LICENSE for details.


import os
import sys

from subprocess import STDOUT, CalledProcessError, check_output

import click

from ._builder import find_fragments
from ._settings import config_option_help, load_config_from_options


def _run(args, **kwargs):
    kwargs["stderr"] = STDOUT
    return check_output(args, **kwargs)


@click.command(name="check")
@click.option(
    "--compare-with",
    default="origin/master",
    metavar="BRANCH",
    help=(
        "Checks files changed running git diff --name-ony BRANCH... "
        "BRANCH is the branch to be compared with. "
        "Default to origin/master"
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
def _main(compare_with, directory, config):
    """
    Check for new fragments on a branch.
    """
    return __main(compare_with, directory, config)


def __main(comparewith, directory, config):

    base_directory, config = load_config_from_options(directory, config)

    # Use UTF-8 both when sys.stdout does not have .encoding (Python 2.7) and
    # when the attribute is present but set to None (explicitly piped output
    # and also some CI such as GitHub Actions).
    encoding = getattr(sys.stdout, "encoding", "utf8")

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
        click.echo(
            f"On {comparewith} branch, or no diffs, so no newsfragment required."
        )
        sys.exit(0)

    files = {
        os.path.normpath(os.path.join(base_directory, path))
        for path in files_changed.strip().splitlines()
    }

    click.echo("Looking at these files:")
    click.echo("----")
    for n, change in enumerate(files, start=1):
        click.echo(f"{n}. {change}")
    click.echo("----")

    news_file = os.path.normpath(os.path.join(base_directory, config["filename"]))
    if news_file in files:
        click.echo("Checks SKIPPED: news file changes detected.")
        sys.exit(0)

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
            click.echo(f"{n}. {fragment}")
        sys.exit(0)


if __name__ == "__main__":  # pragma: no cover
    _main()
