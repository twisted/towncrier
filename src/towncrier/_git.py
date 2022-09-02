# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

import os

from subprocess import STDOUT, call, check_output

import click


def remove_files(fragment_filenames, answer_yes):
    if not fragment_filenames:
        return

    if answer_yes:
        click.echo("Removing the following files:")
    else:
        click.echo("I want to remove the following files:")

    for filename in fragment_filenames:
        click.echo(filename)

    if answer_yes or click.confirm("Is it okay if I remove those files?", default=True):
        call(["git", "rm", "--quiet"] + fragment_filenames)


def stage_newsfile(directory, filename):

    call(["git", "add", os.path.join(directory, filename)])


def get_remote_branches(base_directory, encoding):
    output = check_output(
        ["git", "branch", "-r"], cwd=base_directory, encoding=encoding, stderr=STDOUT
    )

    return [branch.strip() for branch in output.strip().splitlines()]


def list_changed_files_compared_to_branch(base_directory, encoding, compare_with):
    output = check_output(
        ["git", "diff", "--name-only", compare_with + "..."],
        cwd=base_directory,
        encoding=encoding,
        stderr=STDOUT,
    )

    return output.strip().splitlines()
