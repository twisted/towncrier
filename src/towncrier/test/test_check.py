# Copyright (c) Amber Brown, 2017
# See LICENSE for details.

import os

from twisted.trial.unittest import TestCase
from click.testing import CliRunner
from subprocess import call

from towncrier.check import _main


class TestChecker(TestCase):
    maxDiff = None

    def test_no_changes_made(self):
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open("pyproject.toml", "w") as f:
                f.write("[tool.towncrier]\n" 'package = "foo"\n')
            os.mkdir("foo")
            with open("foo/__init__.py", "w") as f:
                f.write('__version__ = "1.2.3"\n')
            os.mkdir("foo/newsfragments")
            fragment_path = "foo/newsfragments/123.feature"
            with open(fragment_path, "w") as f:
                f.write("Adds levitation")

            call(["git", "init"])
            call(["git", "config", "user.name", "user"])
            call(["git", "config", "user.email", "user@example.com"])
            call(["git", "add", "."])
            call(["git", "commit", "-m", "Initial Commit"])
            call(["git", "checkout", "-b", "otherbranch"])

            result = runner.invoke(_main, ["--compare-with", "master"])

            self.assertEqual(0, result.exit_code)
            self.assertEqual(
                "On trunk, or no diffs, so no newsfragment required.\n", result.output
            )

    def test_fragment_exists(self):
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open("pyproject.toml", "w") as f:
                f.write("[tool.towncrier]\n" 'package = "foo"\n')
            os.mkdir("foo")
            with open("foo/__init__.py", "w") as f:
                f.write('__version__ = "1.2.3"\n')
            os.mkdir("foo/newsfragments")
            fragment_path = "foo/newsfragments/123.feature"
            with open(fragment_path, "w") as f:
                f.write("Adds levitation")

            call(["git", "init"])
            call(["git", "config", "user.name", "user"])
            call(["git", "config", "user.email", "user@example.com"])
            call(["git", "add", "."])
            call(["git", "commit", "-m", "Initial Commit"])
            call(["git", "checkout", "-b", "otherbranch"])

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

            result = runner.invoke(_main, ["--compare-with", "master"])

            self.assertTrue(
                result.output.endswith(
                    "Found:\n1. " + os.path.abspath(fragment_path) + "\n"
                )
            )
            self.assertEqual(0, result.exit_code)

    def test_fragment_missing(self):
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open("pyproject.toml", "w") as f:
                f.write("[tool.towncrier]\n" 'package = "foo"\n')
            os.mkdir("foo")
            with open("foo/__init__.py", "w") as f:
                f.write('__version__ = "1.2.3"\n')
            os.mkdir("foo/newsfragments")
            fragment_path = "foo/newsfragments/123.feature"
            with open(fragment_path, "w") as f:
                f.write("Adds levitation")

            call(["git", "init"])
            call(["git", "config", "user.name", "user"])
            call(["git", "config", "user.email", "user@example.com"])
            call(["git", "add", "."])
            call(["git", "commit", "-m", "Initial Commit"])
            call(["git", "checkout", "-b", "otherbranch"])

            file_path = "foo/somefile.py"
            with open(file_path, "w") as f:
                f.write("import os")

            call(["git", "add", "foo/somefile.py"])
            call(["git", "commit", "-m", "add a file"])

            result = runner.invoke(_main, ["--compare-with", "master"])

            self.assertEqual(1, result.exit_code)
            self.assertTrue(
                result.output.endswith("No new newsfragments found on this branch.\n")
            )
