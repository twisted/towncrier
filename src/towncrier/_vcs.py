import os

if os.path.exists(".git"):
    flavor = "git"
    from ._git import *

elif os.path.exists(".hg"):
    flavor = "hg"
    from ._hg import *

else:
    flavor = "none"

    def remove_files(fragment_filenames: list[str]) -> None:
        if not fragment_filenames:
            return

        for fragment in fragment_filenames:
            os.remove(fragment)

    def stage_newsfile(directory: str, filename: str) -> None:
        return

    def get_remote_branches(base_directory: str) -> list[str]:
        return []

    def list_changed_files_compared_to_branch(
        base_directory: str, compare_with: str, include_staged: bool
    ) -> list[str]:
        return []
