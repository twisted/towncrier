# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from __future__ import absolute_import, division

import os

import click

from ._settings import load_config
from ._builder import find_fragments


@click.command()
@click.option('--draft', 'draft', default=False, flag_value=True)
@click.option('--dir', 'directory', default='.')
def _main(draft, directory):

    directory = os.path.abspath(directory)
    config = load_config(directory)

    fragments = find_fragments(
        os.path.join(directory, config['package_dir'], config['package']),
        config['sections'])

    click.echo(config)
    click.echo(fragments)


    click.echo("hi" + str(draft))


__all__ = []
