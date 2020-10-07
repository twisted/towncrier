# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

import os
from textwrap import dedent
from twisted.trial.unittest import TestCase

from click.testing import CliRunner

from ..create import _main


def setup_simple_project(config=None, mkdir=True):
    if not config:
        config = dedent(
            """\
            [tool.towncrier]
            package = "foo"
            """
        )

    with open("pyproject.toml", "w") as f:
        f.write(config)

    os.mkdir("foo")
    with open("foo/__init__.py", "w") as f:
        f.write('__version__ = "1.2.3"\n')

    if mkdir:
        os.mkdir("foo/newsfragments")


class TestCli(TestCase):
    maxDiff = None

    def _test_success(self, config=None, mkdir=True, interactive=False):
        runner = CliRunner()

        with runner.isolated_filesystem():
            setup_simple_project(config, mkdir)

            input_content = None
            args = ["123.feature.rst"]
            content = ["Add your info here"]
            if interactive:
                args.append("-i")
                input_content = "This is line 1\nThis is line 2\n"
                content = ['This is line 1\n', 'This is line 2']
            result = runner.invoke(_main, args, input=input_content)

            self.assertEqual(["123.feature.rst"], os.listdir("foo/newsfragments"))

            with open("foo/newsfragments/123.feature.rst") as fh:
                self.assertEqual(content, fh.readlines())

        self.assertEqual(0, result.exit_code)

    def test_basics(self):
        """Ensure file created where output directory already exists."""
        self._test_success(mkdir=True)

    def test_directory_created(self):
        """Ensure both file and output directory created if necessary."""
        self._test_success(mkdir=False)

    def test_interactive(self):
        """Create file with dynamic content."""
        self._test_success(interactive=True)

    def test_different_directory(self):
        """Ensure non-standard directories are used."""
        runner = CliRunner()
        config = dedent(
            """\
            [tool.towncrier]
            directory = "releasenotes"
            """
        )

        with runner.isolated_filesystem():
            setup_simple_project(config, mkdir=False)
            os.mkdir("releasenotes")

            result = runner.invoke(_main, ["123.feature.rst"])

            self.assertEqual(["123.feature.rst"], os.listdir("releasenotes"))

        self.assertEqual(0, result.exit_code)

    def test_invalid_section(self):
        """Ensure creating a path without a valid section is rejected."""
        runner = CliRunner()

        with runner.isolated_filesystem():
            setup_simple_project()

            self.assertEqual([], os.listdir("foo/newsfragments"))

            result = runner.invoke(_main, ["123.foobar.rst"])

            self.assertEqual([], os.listdir("foo/newsfragments"))

        self.assertEqual(type(result.exception), SystemExit, result.exception)
        self.assertIn(
            "Expected filename '123.foobar.rst' to be of format", result.output
        )

    def test_file_exists(self):
        """Ensure we don't overwrite existing files."""
        runner = CliRunner()

        with runner.isolated_filesystem():
            setup_simple_project()

            self.assertEqual([], os.listdir("foo/newsfragments"))

            runner.invoke(_main, ["123.feature.rst"])
            result = runner.invoke(_main, ["123.feature.rst"])

        self.assertEqual(type(result.exception), SystemExit)
        self.assertIn("123.feature.rst already exists", result.output)
