# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from __future__ import annotations

from typing import Callable

import click


def should_remove_fragment_files(
    fragment_filenames: list[str],
    answer_yes: bool,
    answer_keep: bool,
    confirm_fn: Callable[[], bool],
) -> bool:
    try:
        if answer_keep:
            click.echo("Keeping the following files:")
            # Not proceeding with the removal of the files.
            return False

        if answer_yes:
            click.echo("Removing the following files:")
        else:
            click.echo("I want to remove the following files:")
    finally:
        # Will always be printed, even for answer_keep to help with possible troubleshooting
        for filename in fragment_filenames:
            click.echo(filename)

    if answer_yes or confirm_fn():
        return True
    return False
