# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from __future__ import annotations

import click

from towncrier._git import remove_files


def remove_news_fragment_files(
    fragment_filenames: list[str], answer_yes: bool, answer_keep: bool
) -> None:
    try:
        if answer_keep:
            click.echo("Keeping the following files:")
            # Not proceeding with the removal of the files.
            return

        if answer_yes:
            click.echo("Removing the following files:")
        else:
            click.echo("I want to remove the following files:")
    finally:
        # Will always be printed, even for answer_keep to help with possible troubleshooting
        for filename in fragment_filenames:
            click.echo(filename)

    if answer_yes or click.confirm("Is it okay if I remove those files?", default=True):
        remove_files(fragment_filenames)
