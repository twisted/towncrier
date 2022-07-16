# Copyright (c) Amber Brown, 2017
# See LICENSE for details.

import os
import os.path
import sys

from subprocess import PIPE, Popen, call

from click.testing import CliRunner
from twisted.trial.unittest import TestCase

from towncrier.check import _main as towncrier_check


def create_project(pyproject_path="pyproject.toml", main_branch="main"):
    """
    Create the project files in the main branch that already has a
    news-fragment and then switch to a new in-work branch.
    """
    with open(pyproject_path, "w") as f:
        f.write("[tool.towncrier]\n" 'package = "foo"\n')
    os.mkdir("foo")
    with open("foo/__init__.py", "w") as f:
        f.write('__version__ = "1.2.3"\n')
    os.mkdir("foo/newsfragments")
    fragment_path = "foo/newsfragments/123.feature"
    with open(fragment_path, "w") as f:
        f.write("Adds levitation")

    initial_commit(branch=main_branch)
    call(["git", "checkout", "-b", "otherbranch"])


def commit(message):
    """Stage and commit the repo in the current working directory

    There must be uncommitted changes otherwise git will complain:
    "nothing to commit, working tree clean"
    """
    call(["git", "add", "."])
    call(["git", "commit", "-m", message])


def write(path, contents):
    """Create a file with given contents including any missing parent directories"""
    dir = os.path.dirname(path)
    if dir:
        try:
            os.makedirs(dir)
        except OSError:  # pragma: no cover
            pass
    with open(path, "w") as f:
        f.write(contents)


def initial_commit(branch="main"):
    """
    Create a git repo, configure it and make an initial commit

    There must be uncommitted changes otherwise git will complain:
    "nothing to commit, working tree clean"
    """
    # --initial-branch is explicitly set to `main` because
    # git has deprecated the default branch name.
    call(["git", "init", f"--initial-branch={branch}"])
    # Without ``git config` user.name and user.email `git commit` fails
    # unless the settings are set globally
    call(["git", "config", "user.name", "user"])
    call(["git", "config", "user.email", "user@example.com"])
    commit("Initial Commit")


class TestChecker(TestCase):
    maxDiff = None

    def test_git_fails(self):
        """
        If git fails to report a comparison, git's output is reported to aid in
        debugging the situation.
        """
        runner = CliRunner()
        with runner.isolated_filesystem():
            create_project("pyproject.toml")

            result = runner.invoke(towncrier_check, ["--compare-with", "hblaugh"])
            self.assertIn("git produced output while failing", result.output)
            self.assertIn("hblaugh", result.output)

    def test_no_changes_made(self):
        self._test_no_changes_made(
            "pyproject.toml", lambda runner, main, argv: runner.invoke(main, argv)
        )

    def test_no_changes_made_config_path(self):
        pyproject = "not-pyproject.toml"
        self._test_no_changes_made(
            pyproject,
            lambda runner, main, argv: runner.invoke(
                main, argv + ["--config", pyproject]
            ),
        )

    def _test_no_changes_made(self, pyproject_path, invoke):
        """
        When no changes are made on a new branch, no checks are performed.
        """
        runner = CliRunner()

        with runner.isolated_filesystem():
            create_project(pyproject_path, main_branch="master")

            result = invoke(runner, towncrier_check, ["--compare-with", "master"])

            self.assertEqual(0, result.exit_code, result.output)
            self.assertEqual(
                "On master branch, or no diffs, so no newsfragment required.\n",
                result.output,
            )

    def test_fragment_exists(self):
        runner = CliRunner()

        with runner.isolated_filesystem():
            create_project("pyproject.toml", main_branch="master")

            file_path = "foo/somefile.py"
            with open(file_path, "w") as f:
                f.write("import os")

            call(["git", "add", "foo/somefile.py"])
            call(["git", "commit", "-m", "add a file"])

            fragment_path = "foo/newsfragments/1234.feature"
            with open(fragment_path, "w") as f:
                f.write("Adds gravity back")

            call(["git", "add", fragment_path])
            call(["git", "commit", "-m", "add a newsfragment"])

            result = runner.invoke(towncrier_check, ["--compare-with", "master"])

            self.assertTrue(
                result.output.endswith(
                    "Found:\n1. " + os.path.abspath(fragment_path) + "\n"
                ),
                result,
            )
            self.assertEqual(0, result.exit_code, result)

    def test_fragment_missing(self):
        runner = CliRunner()

        with runner.isolated_filesystem():
            create_project("pyproject.toml", main_branch="master")

            file_path = "foo/somefile.py"
            with open(file_path, "w") as f:
                f.write("import os")

            call(["git", "add", "foo/somefile.py"])
            call(["git", "commit", "-m", "add a file"])

            result = runner.invoke(towncrier_check, ["--compare-with", "master"])

            self.assertEqual(1, result.exit_code)
            self.assertTrue(
                result.output.endswith("No new newsfragments found on this branch.\n")
            )

    def test_none_stdout_encoding_works(self):
        """
        No failure when output is piped causing None encoding for stdout.
        """
        runner = CliRunner()

        with runner.isolated_filesystem():
            create_project("pyproject.toml", main_branch="master")

            fragment_path = "foo/newsfragments/1234.feature"
            with open(fragment_path, "w") as f:
                f.write("Adds gravity back")

            call(["git", "add", fragment_path])
            call(["git", "commit", "-m", "add a newsfragment"])

            proc = Popen(
                [sys.executable, "-m", "towncrier.check", "--compare-with", "master"],
                stdout=PIPE,
                stderr=PIPE,
            )
            stdout, stderr = proc.communicate()

        self.assertEqual(0, proc.returncode)
        self.assertEqual(b"", stderr)

    def test_first_release(self):
        """
        The checks should be skipped on a branch that creates the news file.

        If the checks are not skipped in this case, towncrier check would fail
        for the first release that has a changelog.
        """
        runner = CliRunner()

        with runner.isolated_filesystem():
            # Arrange
            create_project()
            # Before any release, the NEWS file might no exist.
            self.assertNotIn("NEWS.rst", os.listdir("."))

            call(["towncrier", "build", "--yes", "--version", "1.0"])
            commit("Prepare a release")
            # When missing,
            # the news file is automatically created with a new release.
            self.assertIn("NEWS.rst", os.listdir("."))

            # Act
            result = runner.invoke(towncrier_check, ["--compare-with", "main"])

            # Assert
            self.assertEqual(0, result.exit_code, (result, result.output))
            self.assertIn("Checks SKIPPED: news file changes detected", result.output)

    def test_release_branch(self):
        """
        The checks for missing news fragments are skipped on a branch that
        modifies the news file.
        This is a hint that we are on a release branch
        and at release time is expected no not have news-fragment files.
        """
        runner = CliRunner()

        with runner.isolated_filesystem():
            # Arrange
            create_project()

            # Do a first release without any checks.
            # And merge the release branch back into the main branch.
            call(["towncrier", "build", "--yes", "--version", "1.0"])
            commit("First release")
            # The news file is now created.
            self.assertIn("NEWS.rst", os.listdir("."))
            call(["git", "checkout", "main"])
            call(["git", "merge", "otherbranch", "-m", "Sync release in main branch."])

            # We have a new feature branch that has a news fragment that
            # will be merged to the main branch.
            call(["git", "checkout", "-b", "new-feature-branch"])
            write("foo/newsfragments/456.feature", "Foo the bar")
            commit("A feature in the second release.")
            call(["git", "checkout", "main"])
            call(
                [
                    "git",
                    "merge",
                    "new-feature-branch",
                    "-m",
                    "Merge new-feature-branch.",
                ]
            )

            # We now have the new release branch.
            call(["git", "checkout", "-b", "next-release"])
            call(["towncrier", "build", "--yes", "--version", "2.0"])
            commit("Second release")

            # Act
            result = runner.invoke(towncrier_check, ["--compare-with", "main"])

            # Assert
            self.assertEqual(0, result.exit_code, (result, result.output))
            self.assertIn("Checks SKIPPED: news file changes detected", result.output)
