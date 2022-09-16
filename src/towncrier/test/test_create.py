# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

import os

from textwrap import dedent
from unittest import mock

from click.testing import CliRunner
from twisted.trial.unittest import TestCase

from ..create import _main
from .helpers import setup_simple_project


class TestCli(TestCase):
    maxDiff = None

    def _test_success(
        self, content=None, config=None, mkdir=True, additional_args=None
    ):
        runner = CliRunner()

        with runner.isolated_filesystem():
            setup_simple_project(config=config, mkdir_newsfragments=mkdir)

            args = ["123.feature.rst"]
            if content is None:
                content = ["Add your info here"]
            if additional_args is not None:
                args.extend(additional_args)
            result = runner.invoke(_main, args)

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

    def test_edit_without_comments(self):
        """Create file with dynamic content."""
        content = ["This is line 1\n", "This is line 2"]
        with mock.patch("click.edit") as mock_edit:
            mock_edit.return_value = "".join(content)
            self._test_success(content=content, additional_args=["--edit"])
            mock_edit.assert_called_once_with(
                "# Please write your news content. When finished, save the file.\n"
                "# In order to abort, exit without saving.\n"
                '# Lines starting with "#" are ignored.\n'
                "\n"
                "Add your info here\n"
            )

    def test_edit_with_comment(self):
        """Create file editly with ignored line."""
        content = ["This is line 1\n", "This is line 2"]
        comment = "# I am ignored\n"
        with mock.patch("click.edit") as mock_edit:
            mock_edit.return_value = "".join(content[:1] + [comment] + content[1:])
            self._test_success(content=content, additional_args=["--edit"])

    def test_edit_abort(self):
        """Create file editly and abort."""
        with mock.patch("click.edit") as mock_edit:
            mock_edit.return_value = None

            runner = CliRunner()

            with runner.isolated_filesystem():
                setup_simple_project(config=None, mkdir_newsfragments=True)
                result = runner.invoke(_main, ["123.feature.rst", "--edit"])
                self.assertEqual([], os.listdir("foo/newsfragments"))
                self.assertEqual(1, result.exit_code)

    def test_content(self):
        """
        When creating a new fragment the content can be passed as a
        command line argument.
        The text editor is not invoked.
        """
        content_line = "This is a content"
        self._test_success(content=[content_line], additional_args=["-c", content_line])

    def test_message_and_edit(self):
        """
        When creating a new message, a initial content can be passed via
        the command line and continue modifying the content by invoking the
        text editor.
        """
        content_line = "This is a content line"
        edit_content = ["This is line 1\n", "This is line 2"]
        with mock.patch("click.edit") as mock_edit:
            mock_edit.return_value = "".join(edit_content)
            self._test_success(
                content=edit_content, additional_args=["-c", content_line, "--edit"]
            )
            mock_edit.assert_called_once_with(
                "# Please write your news content. When finished, save the file.\n"
                "# In order to abort, exit without saving.\n"
                '# Lines starting with "#" are ignored.\n'
                "\n"
                "{content_line}\n".format(content_line=content_line)
            )

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
            setup_simple_project(config=config, mkdir_newsfragments=False)
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

    def test_create_orphan_fragment(self):
        """
        When a fragment starts with the only the orphan prefix (``+`` by default), the
        create CLI automatically extends the new file's base name to contain a random
        value to avoid commit collisions.
        """
        runner = CliRunner()

        with runner.isolated_filesystem():
            setup_simple_project()

            self.assertEqual([], os.listdir("foo/newsfragments"))

            runner.invoke(_main, ["+.feature"])
            fragments = os.listdir("foo/newsfragments")

        self.assertEqual(1, len(fragments))
        filename = fragments[0]
        self.assertTrue(filename.endswith(".feature"))
        self.assertTrue(filename.startswith("+"))
        # Length should be '+' character and 8 random hex characters.
        self.assertEqual(len(filename.split(".")[0]), 9)
