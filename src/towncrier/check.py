# Copyright (c) Amber Brown, 2017
# See LICENSE for details.

from __future__ import absolute_import, division

import os
import sys

import click

from subprocess import check_output, STDOUT

from ._settings import load_config
from ._builder import find_fragments


def _run(args, **kwargs):
    kwargs['stderr'] = STDOUT
    return check_output(args, **kwargs)


@click.command()
@click.option("--comparewith", default="origin/master")
@click.option('--dir', 'directory', default='.')
def _main(comparewith, directory):
    return __main(comparewith, directory)


def __main(comparewith, directory):

    base_directory = os.path.abspath(directory)
    config = load_config(directory)

    files_changed = _run(
        ["git", "diff", "--name-only", comparewith + "..."],
        cwd=base_directory).decode(
            getattr(sys.stdout, 'encoding', 'utf8')).strip()

    if not files_changed:
        click.echo("On trunk, or no diffs, so no newsfragment required.")
        sys.exit(0)

    files = set(map(lambda x: os.path.join(base_directory, x),
                    files_changed.strip().split(os.linesep)))

    click.echo("Looking at these files:")
    click.echo("----")
    for n, change in enumerate(files, start=1):
        click.echo("{}. {}".format(n, change))
    click.echo("----")

    fragments = set()

    for section in [x.keys() for x in find_fragments(
            directory, config).values()]:
        fragments.update(section)

    fragments_in_branch = fragments & files

    if not fragments_in_branch:
        click.echo("No new newsfragments found on this branch.")
        sys.exit(1)
    else:
        click.echo("Found:")
        for n, fragment in enumerate(fragments_in_branch, start=1):
            click.echo("{}. {}".format(n, fragment))
        sys.exit(0)


if __name__ == "__main__": # pragma: no cover
    _main()
