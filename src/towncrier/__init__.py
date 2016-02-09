# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

"""
towncrier, a builder for your news files.
"""

from __future__ import absolute_import, division

import os
import click

from datetime import date

from collections import OrderedDict

from ._settings import load_config
from ._builder import find_fragments, split_fragments, render_fragments
from ._project import get_version, get_project_name
from ._writer import append_to_newsfile
from ._git import remove_files, stage_newsfile
from ._version import __version__


def _get_date():
    return date.today().isoformat()


@click.command()
@click.option('--draft', 'draft', default=False, flag_value=True,
              help=("Render the news fragments, don't write to files, "
                    "don't check versions."))
@click.option('--dir', 'directory', default='.')
@click.option('--version', 'project_version', default=None)
@click.option('--date', 'project_date', default=None)
def _main(draft, directory, project_version, project_date):
    return __main(draft, directory, project_version, project_date)


def __main(draft, directory, project_version, project_date):
    """
    The main entry point.
    """
    directory = os.path.abspath(directory)
    config = load_config(directory)

    click.echo("Finding news fragments...")

    # TODO make these customisable
    definitions = OrderedDict([
        ("feature", ("Features", True)),
        ("bugfix", ("Bugfixes", True)),
        ("doc", ("Improved Documentation", True)),
        ("removal", ("Deprecations and Removals", True)),
        ("misc", ("Misc", False)),
    ])

    fragments = find_fragments(
        os.path.join(directory, config['package_dir'], config['package']),
        config['sections'])

    click.echo("Rendering news fragments...")

    fragments = split_fragments(fragments, definitions)
    rendered = render_fragments(fragments, definitions)

    if not project_version:
        project_version = get_version(
            os.path.abspath(os.path.join(directory, config['package_dir'])),
            config['package'])

    project_name = get_project_name(
        os.path.abspath(os.path.join(directory, config['package_dir'])),
        config['package'])

    name_and_version = project_name + " " + project_version

    if project_date is None:
        project_date = _get_date()

    if project_date != "":
        name_and_version += " (" + project_date + ")"

    if draft:
        click.echo("Draft only -- nothing has been written.")
        click.echo("What is seen below is what would be written.\n")
        click.echo(name_and_version)
        click.echo("=" * len(name_and_version) + "\n")
        click.echo(rendered)
    else:
        click.echo("Writing to newsfile...")
        append_to_newsfile(directory, config['filename'],
                           name_and_version, rendered)

        click.echo("Staging newsfile...")
        stage_newsfile(directory, config['filename'])

        click.echo("Removing news fragments...")
        remove_files(directory, config['package_dir'],
                     config['package'], config['sections'], fragments)

        click.echo("Done!")


__all__ = ["__version__"]
