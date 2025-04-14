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
        hg_fragments = check_output(
            ["hg", "files"] + fragment_filenames, encoding="utf-8"
        ).split("\n")
    except CalledProcessError:
        # we may not be in a git repository
        hg_fragments = []

    hg_fragments = [os.path.abspath(f) for f in hg_fragments if os.path.isfile(f)]
    call(["hg", "rm", "--force"] + hg_fragments)
    unknown_fragments = set(fragment_filenames) - set(hg_fragments)
    for unknown_fragment in unknown_fragments:
        os.remove(unknown_fragment)


def stage_newsfile(directory: str, filename: str) -> None:
    call(["hg", "add", os.path.join(directory, filename)])


def get_remote_branches(base_directory: str) -> list[str]:
    return []


def list_changed_files_compared_to_branch(
    base_directory: str, compare_with: str, include_staged: bool
) -> list[str]:
    return []
