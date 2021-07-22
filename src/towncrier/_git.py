# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from __future__ import annotations

import os

from subprocess import STDOUT, CalledProcessError, call, check_output


def remove_files(fragment_filenames: list[str]) -> None:
    if not fragment_filenames:
        return

    # Filter out files that are unknown to git
    try:
        git_fragments = check_output(
            ["git", "ls-files"] + fragment_filenames, encoding="utf-8"
        ).split("\n")
    except CalledProcessError:
        # we may not be in a git repository
        git_fragments = []

    git_fragments = [os.path.abspath(f) for f in git_fragments if os.path.isfile(f)]
    call(["git", "rm", "--quiet", "--force"] + git_fragments)
    unknown_fragments = set(fragment_filenames) - set(git_fragments)
    for unknown_fragment in unknown_fragments:
        os.remove(unknown_fragment)


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
