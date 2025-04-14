# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from __future__ import annotations

import os

from subprocess import STDOUT, CalledProcessError, call, check_output
from typing import Container


def get_default_compare_branch(branches: Container[str]) -> str | None:
    if "default" in branches:
        return "default"
    return None


def _topic_enabled(directory: str) -> bool:
    for e in (
        check_output(
            ["hg", "config"],
            cwd=directory,
            encoding="utf-8",
        )
        .strip()
        .splitlines()
    ):
        if (
            e.startswith("extensions.topic")
            and e.split("=")[0].strip() == "extensions.topic"
        ):
            return True
    return False


_has_topics_cache = {}


def has_topics(directory: str) -> bool:
    if directory not in _has_topics_cache:
        _has_topics_cache[directory] = _topic_enabled(directory)

    return _has_topics_cache[directory] is True


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
    branches = check_output(
        ["hg", "branch"],
        cwd=base_directory,
        encoding="utf-8",
        stderr=STDOUT,
    ).splitlines()

    if has_topics(base_directory):
        branches += check_output(
            ["hg", "topic", "--template", "{topic}"],
            cwd=base_directory,
            encoding="utf-8",
            stderr=STDOUT,
        ).splitlines()

    return branches


def list_changed_files_compared_to_branch(
    base_directory: str, compare_with: str, include_staged: bool
) -> list[str]:
    output = check_output(
        ["hg", "diff", "--stat", "-r", compare_with],
        cwd=base_directory,
        encoding="utf-8",
        stderr=STDOUT,
    ).splitlines()

    return [line.split("|")[0].strip() for line in output if "|" in line]
