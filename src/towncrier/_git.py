# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from subprocess import call

import os
import click


def remove_files(base_dir, fragment_directory, sections, fragments,
                 answer_yes):
    to_remove = []

    for section_name, categories in fragments.items():

        if fragment_directory is not None:
            section_dir = os.path.join(base_dir, sections[section_name],
                                       fragment_directory)
        else:
            section_dir = os.path.join(base_dir, sections[section_name])

        for category_name, category_items in categories.items():

            for tickets in category_items.values():

                for ticket in tickets:
                    to_remove.append(find_file_path(
                        section_dir, category_name, ticket))

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
        call(["git", "rm", "--quiet"] + to_remove)


def stage_newsfile(directory, filename):

    call(["git", "add", os.path.join(directory, filename)])


def find_file_path(section_dir, category_name, ticket):
    accepted_extensions = ['', '.rst', '.txt']
    namestub = "%s.%s" % (ticket, category_name)
    for ext in accepted_extensions:
        filename = namestub + ext

        path = os.path.join(section_dir, filename)

        if os.path.exists(path):
            return path

    raise FileNotFoundError(
        "can't find the file for fragment %s at %s - "
        "use no extension or one of the accepted (%s)" % (
            namestub, section_dir, accepted_extensions[1:]))
