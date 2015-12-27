# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from subprocess import call

import os
import click

def detect_git(self):

    r = call(["git", "rev-parse", "--is-inside-work-tree"])

    print(r)


def remove_files(directory, package_dir, package, sections, fragments):

    base_dir = os.path.join(directory, package_dir, package)

    to_remove = []

    for section_name, categories in fragments.items():

        section_dir = os.path.join(base_dir, "newsfragments",
                                   sections[section_name])

        for category_name, category_items in categories.items():

            for tickets in category_items.values():

                for ticket in tickets:

                    filename = str(ticket) + "." + category_name
                    to_remove.append(os.path.join(section_dir, filename))

    click.echo("I want to remove the following files:")

    for filename in to_remove:
        click.echo(filename)

    if click.confirm('Is it okay if I remove those files?'):
        call(["git", "rm", "--quiet"] + to_remove)
