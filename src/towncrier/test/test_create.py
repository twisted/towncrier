# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

import os
import string

from pathlib import Path
from textwrap import dedent
from unittest import mock

from click.testing import CliRunner
from twisted.trial.unittest import TestCase

from ..create import _main
from .helpers import setup_simple_project, with_isolated_runner


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

    @with_isolated_runner
    def test_file_exists(self, runner: CliRunner):
        """Ensure we don't overwrite existing files."""
        setup_simple_project()
        frag_path = Path("foo", "newsfragments")

        for _ in range(3):
            result = runner.invoke(_main, ["123.feature"])
            self.assertEqual(result.exit_code, 0, result.output)

        fragments = [f.name for f in frag_path.iterdir()]
        self.assertEqual(
            sorted(fragments),
            [
                "123.feature",
                "123.feature.1",
                "123.feature.2",
            ],
        )

    @with_isolated_runner
    def test_file_exists_with_ext(self, runner: CliRunner):
        """
        Ensure we don't overwrite existing files when using an extension after the
        fragment type.
        """
        setup_simple_project()
        frag_path = Path("foo", "newsfragments")

        for _ in range(3):
            result = runner.invoke(_main, ["123.feature.rst"])
            self.assertEqual(result.exit_code, 0, result.output)

        fragments = [f.name for f in frag_path.iterdir()]
        self.assertEqual(
            sorted(fragments),
            [
                "123.feature.1.rst",
                "123.feature.2.rst",
                "123.feature.rst",
            ],
        )

    @with_isolated_runner
    def test_create_orphan_fragment(self, runner: CliRunner):
        """
        When a fragment starts with the only the orphan prefix (``+`` by default), the
        create CLI automatically extends the new file's base name to contain a random
        value to avoid commit collisions.
        """
        setup_simple_project()

        frag_path = Path("foo", "newsfragments")
        sub_frag_path = frag_path / "subsection"
        sub_frag_path.mkdir()

        result = runner.invoke(_main, ["+.feature"])
        self.assertEqual(0, result.exit_code)
        result = runner.invoke(
            _main, [str(Path("subsection", "+.feature"))], catch_exceptions=False
        )
        self.assertEqual(0, result.exit_code, result.output)

        fragments = [p for p in frag_path.rglob("*") if p.is_file()]
        self.assertEqual(2, len(fragments))
        change1, change2 = fragments

        self.assertEqual(change1.suffix, ".feature")
        self.assertTrue(change1.stem.startswith("+"))
        # Length should be '+' character and 8 random hex characters.
        self.assertEqual(len(change1.stem), 9)

        self.assertEqual(change2.suffix, ".feature")
        self.assertTrue(change2.stem.startswith("+"))
        self.assertEqual(change2.parent, sub_frag_path)
        # Length should be '+' character and 8 random hex characters.
        self.assertEqual(len(change2.stem), 9)

    @with_isolated_runner
    def test_create_orphan_fragment_custom_prefix(self, runner: CliRunner):
        """
        Check that the orphan prefix can be customized.
        """
        setup_simple_project(extra_config='orphan_prefix = "$$$"')

        frag_path = Path("foo", "newsfragments")

        result = runner.invoke(_main, ["$$$.feature"])
        self.assertEqual(0, result.exit_code, result.output)

        fragments = list(frag_path.rglob("*"))
        self.assertEqual(len(fragments), 1)
        change = fragments[0]
        self.assertTrue(change.stem.startswith("$$$"))
        # Length should be '$$$' characters and 8 random hex characters.
        self.assertEqual(len(change.stem), 11)
        # Check the remainder are all hex characters.
        self.assertTrue(all(c in string.hexdigits for c in change.stem[3:]))

    @with_isolated_runner
    def test_in_different_dir_with_nondefault_newsfragments_directory(self, runner):
        """
        When the `--dir` CLI argument is passed,
        it will create a new file in directory that is
        created by combining the `--dir` value
        with the `directory` option from the configuration
        file.
        """
        Path("pyproject.toml").write_text(
            # Important to customize `config.directory` because the default
            # already supports this scenario.
            "[tool.towncrier]\n"
            + 'directory = "changelog.d"\n'
        )
        Path("foo/foo").mkdir(parents=True)
        Path("foo/foo/__init__.py").write_text("")

        result = runner.invoke(
            _main,
            (
                "--config",
                "pyproject.toml",
                "--dir",
                "foo",
                "--content",
                "Adds levitation.",
                "123.feature",
            ),
        )

        self.assertEqual(0, result.exit_code)
        self.assertTrue(Path("foo/changelog.d/123.feature").exists())
