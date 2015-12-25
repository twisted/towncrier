# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from __future__ import absolute_import

import os

import click

from ._settings import load_config

@click.command()
@click.option('--draft', 'draft', default=False, flag_value=True)
def _main(draft):


    config = load_config(os.path.abspath("."))

    click.echo(config)

    click.echo("hi" + str(draft))


__all__ = []
