# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from __future__ import annotations

import os

from subprocess import STDOUT, call, check_output


def remove_files(fragment_filenames: list[str]) -> None:
    if fragment_filenames:
        call(["git", "rm", "--quiet"] + fragment_filenames)


def stage_newsfile(directory: str, filename: str) -> None:
    call(["git", "add", os.path.join(directory, filename)])


def get_remote_branches(base_directory: str) -> list[str]:
    output = check_output(
        ["git", "branch", "-r"], cwd=base_directory, encoding="utf-8", stderr=STDOUT
    )

    return [branch.strip() for branch in output.strip().splitlines()]


def list_changed_files_compared_to_branch(
    base_directory: str, compare_with: str
) -> list[str]:
    output = check_output(
        ["git", "diff", "--name-only", compare_with + "..."],
        cwd=base_directory,
        encoding="utf-8",
        stderr=STDOUT,
    )

    return output.strip().splitlines()
