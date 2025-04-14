import os

from typing import Container


def _get_mod(base_directory: str):
    if os.path.exists(os.path.join(base_directory, ".git")):
        from . import _git

        return _git
    elif os.path.exists(os.path.join(base_directory, ".hg")):
        from . import _hg

        return _hg
    else:
        from . import _novcs

        return _novcs


def get_default_compare_branch(
    base_directory: str, branches: Container[str]
) -> str | None:
    return _get_mod(base_directory).get_default_compare_branch(branches)


def remove_files(base_directory: str, fragment_filenames: list[str]) -> None:
    return _get_mod(base_directory).remove_files(fragment_filenames)


def stage_newsfile(directory: str, filename: str) -> None:
    return _get_mod(directory).stage_newsfile(directory, filename)


def get_remote_branches(base_directory: str) -> list[str]:
    return _get_mod(base_directory).get_remote_branches(base_directory)


def list_changed_files_compared_to_branch(
    base_directory: str, compare_with: str, include_staged: bool
) -> list[str]:
    return _get_mod(base_directory).list_changed_files_compared_to_branch(
        base_directory,
        compare_with,
        include_staged,
    )
