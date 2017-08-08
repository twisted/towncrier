# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from subprocess import call

import os
import click


def remove_files(base_dir, fragment_directory, sections, fragments,
                 answer_yes):
    to_remove = set()

    for section in [x.keys() for x in fragments.values()]:
        to_remove.update(section)

    if not to_remove:
        return

    if answer_yes:
        click.echo("Removing the following files:")
    else:
        click.echo("I want to remove the following files:")

    for filename in to_remove:
        click.echo(filename)

    if answer_yes or click.confirm('Is it okay if I remove those files?',
                                   default=True):
        call(["git", "rm", "--quiet"] + list(set(to_remove)))


def stage_newsfile(directory, filename):

    call(["git", "add", os.path.join(directory, filename)])
