from __future__ import absolute_import, division

import os
import sys

import click

from subprocess import check_output, STDOUT

from ._settings import load_config

def _run(args, **kwargs):
    kwargs['stderr'] = STDOUT
    return check_output(args, **kwargs)


@click.command()
@click.option("--comparewith", default="origin/master")
@click.option('--dir', 'directory', default='.')
def _main(comparewith, directory):
    return __main(comparewith, directory)


def __main(comparewith, directory):

    directory = os.path.abspath(directory)
    config = load_config(directory)

    files_changed = _run(["git", "diff", "--name-only", comparewith + "..."],
                         cwd=directory).decode(sys.stdout.encoding).strip()

    if not files_changed:
        click.echo("On trunk, or no diffs, so no newsfragment required.")
        sys.exit(0)

    files = files_changed.strip().split(os.linesep)

    click.echo("Looking at these files:")
    for n, change in enumerate(files):
        click.echo("{}. {}".format(n, change))
    click.echo("----")


if __name__ == "__main__":
    _main()
