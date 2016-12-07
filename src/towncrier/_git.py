# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from subprocess import call

import os
import click


def remove_files(base_dir, fragment_directory, sections, fragments):
    to_remove = []

    for section_name, categories in fragments.items():

        if fragment_directory is not None:
            section_dir = os.path.join(base_dir, fragment_directory,
                                       sections[section_name])
        else:
            section_dir = os.path.join(base_dir, sections[section_name])

        for category_name, category_items in categories.items():

            for tickets in category_items.values():

                for ticket in tickets:

                    filename = str(ticket) + "." + category_name
                    to_remove.append(os.path.join(section_dir, filename))

    if not to_remove:
        return

    click.echo("I want to remove the following files:")

    for filename in to_remove:
        click.echo(filename)

    if click.confirm('Is it okay if I remove those files?', default=True):
        call(["git", "rm", "--quiet"] + to_remove)


def stage_newsfile(directory, filename):

    call(["git", "add", os.path.join(directory, filename)])
