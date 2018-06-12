# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from subprocess import call

import os
import click


def remove_files(fragment_filenames, answer_yes):
    if not fragment_filenames:
        return

    if answer_yes:
        click.echo("Removing the following files:")
    else:
        click.echo("I want to remove the following files:")

    for filename in fragment_filenames:
        click.echo(filename)

    if answer_yes or click.confirm("Is it okay if I remove those files?", default=True):
        call(["git", "rm", "--quiet"] + fragment_filenames)


def stage_newsfile(directory, filename):

    call(["git", "add", os.path.join(directory, filename)])
