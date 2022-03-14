# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

import os
import sys
from subprocess import call, check_output, CalledProcessError

import click


def run(args, **kwargs):
    # Use UTF-8 both when sys.stdout does not have .encoding (Python 2.7) and
    # when the attribute is present but set to None (explicitly piped output
    # and also some CI such as GitHub Actions).
    encoding = getattr(sys.stdout, "encoding", None)
    if encoding is None:
        encoding = "utf8"

    return check_output(args, **kwargs).decode(encoding).strip()


def remove_files(fragment_filenames, answer_yes):
    if not fragment_filenames:
        return

    if answer_yes:
        click.echo("Removing the following files:")
    else:
        click.echo("I want to remove the following files:")

    for filename in sorted(fragment_filenames):
        click.echo(filename)

    # Filter out files that are unknown to git
    try:
        known_fragments = run(
            ["git", "ls-files"] + fragment_filenames
        ).split("\n")
    except CalledProcessError:
        known_fragments = []

    if answer_yes or click.confirm("Is it okay if I remove those files?", default=True):
        call(["git", "rm", "--quiet", "--force"] + known_fragments)
        known_fragments_full = [os.path.abspath(f) for f in known_fragments]
        unknown_fragments = set(fragment_filenames) - set(known_fragments_full)
        for unknown_fragment in unknown_fragments:
            os.remove(unknown_fragment)


def stage_newsfile(directory, filename):

    call(["git", "add", os.path.join(directory, filename)])
