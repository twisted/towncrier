# Copyright (c) Stephen Finucane, 2019
# See LICENSE for details.

"""
towncrier, a builder for your news files.
"""

import click
from click_default_group import DefaultGroup

from .build import _main as _build_cmd
from .check import _main as _check_cmd
from .create import _main as _create_cmd
from ._version import __version__


@click.group(cls=DefaultGroup, default="build", default_if_no_args=True)
@click.version_option(__version__.public())
def cli():
    pass


cli.add_command(_build_cmd)
cli.add_command(_check_cmd)
cli.add_command(_create_cmd)
