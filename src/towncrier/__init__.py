# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from __future__ import absolute_import, division

import os
import click

from collections import OrderedDict

from ._settings import load_config
from ._builder import find_fragments, render_fragments


@click.command()
@click.option('--draft', 'draft', default=False, flag_value=True,
              help="Render the news fragments, don't write to files, don't check versions.")
@click.option('--dir', 'directory', default='.')
def _main(draft, directory):

    directory = os.path.abspath(directory)
    config = load_config(directory)

    fragments = find_fragments(
        os.path.join(directory, config['package_dir'], config['package']),
        config['sections'])

    click.echo(config)
    click.echo(fragments)

    click.echo("\n-------\n")

    # TODO make these customisable
    definitions = OrderedDict([
        ("feature", ("Features", True)),
        ("bugfix", ("Bugfixes", True)),
        ("doc", ("Improved Documentation", True)),
        ("removal", ("Deprecations and Removals", True)),
        ("misc", ("Misc", False)),
    ])

    rendered = render_fragments(fragments, definitions)

    if draft:
        click.echo(rendered)


__all__ = []
