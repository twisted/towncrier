# Copyright (c) towncrier contributors, 2025
# See LICENSE for details.

import os.path

from pathlib import Path

from click.testing import CliRunner
from twisted.trial.unittest import TestCase

from towncrier import _vcs

from . import test_check, test_hg
from .helpers import setup_simple_project, write


def novcs_create_project(
    pyproject_path="pyproject.toml", main_branch="main", extra_config=""
):
    setup_simple_project(pyproject_path=pyproject_path, extra_config=extra_config)
    Path("foo/newsfragments/123.feature").write_text("Adds levitation")


def novcs_commit(message):
    pass


class TestVCS(TestCase):
    def test_vcs(self):
        for tt in [
            {
                "name": "git",
                "create_project": test_check.create_project,
                "commit": test_check.commit,
            },
            {
                "name": "mercurial",
                "create_project": test_hg.create_project,
                "commit": test_hg.commit,
            },
            {
                "name": "novcs",
                "create_project": novcs_create_project,
                "commit": novcs_commit,
            },
        ]:
            with self.subTest(tt["name"]):
                create_project = tt["create_project"]
                commit = tt["commit"]

                runner = CliRunner()
                with runner.isolated_filesystem():
                    create_project("pyproject.toml")

                    write("changes/000.misc.rst", "some change")

                    _vcs.stage_newsfile(os.getcwd(), "changes/000.misc.rst")

                    commit("commit 1")

                    branches = sorted(_vcs.get_remote_branches("."))
                    self.assertIn(branches, [[], ["main", "otherbranch"]])

                    if tt["name"] != "novcs":
                        self.assertIn(
                            _vcs.list_changed_files_compared_to_branch(
                                ".", "main", False
                            ),
                            [
                                ["changes/000.misc.rst"],
                                [os.path.join("changes", "000.misc.rst")],
                            ],
                        )

                    write("changes/001.misc.rst", "some change")
                    _vcs.remove_files(
                        os.getcwd(),
                        [
                            os.path.abspath(f)
                            for f in ["changes/000.misc.rst", "changes/001.misc.rst"]
                        ],
                    )
