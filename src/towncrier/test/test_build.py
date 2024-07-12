# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

import os
import tempfile

from datetime import date
from pathlib import Path
from textwrap import dedent
from unittest.mock import patch

from click.testing import CliRunner
from twisted.trial.unittest import TestCase

from .._shell import cli
from ..build import _main
from .helpers import read, with_git_project, with_project, write


class TestCli(TestCase):
    maxDiff = None

    @with_project()
    def _test_command(self, command, runner):
        # Off the shelf newsfragment
        with open("foo/newsfragments/123.feature", "w") as f:
            f.write("Adds levitation")
        # Towncrier treats this as 124.feature, ignoring .rst extension
        with open("foo/newsfragments/124.feature.rst", "w") as f:
            f.write("Extends levitation")
        # Towncrier supports non-numeric newsfragment names.
        with open("foo/newsfragments/baz.feature.rst", "w") as f:
            f.write("Baz levitation")
        # Towncrier supports files that have a dot in the name of the
        # newsfragment
        with open("foo/newsfragments/fix-1.2.feature", "w") as f:
            f.write("Baz fix levitation")
        # Towncrier supports fragments not linked to a feature
        with open("foo/newsfragments/+anything.feature", "w") as f:
            f.write("Orphaned feature")
        with open("foo/newsfragments/+xxx.feature", "w") as f:
            f.write("Another orphaned feature")
        with open("foo/newsfragments/+123_orphaned.feature", "w") as f:
            f.write("An orphaned feature starting with a number")
        with open("foo/newsfragments/+12.3_orphaned.feature", "w") as f:
            f.write("An orphaned feature starting with a dotted number")
        with open("foo/newsfragments/+orphaned_123.feature", "w") as f:
            f.write("An orphaned feature ending with a number")
        with open("foo/newsfragments/+orphaned_12.3.feature", "w") as f:
            f.write("An orphaned feature ending with a dotted number")
        # Towncrier ignores files that don't have a dot
        with open("foo/newsfragments/README", "w") as f:
            f.write("Blah blah")
        # And files that don't have a valid category
        with open("foo/newsfragments/README.rst", "w") as f:
            f.write("**Blah blah**")

        result = runner.invoke(command, ["--draft", "--date", "01-01-2001"])

        self.assertEqual(0, result.exit_code, result.output)
        self.assertEqual(
            result.output,
            dedent(
                """\
                Loading template...
                Finding news fragments...
                Rendering news fragments...
                Draft only -- nothing has been written.
                What is seen below is what would be written.

                Foo 1.2.3 (01-01-2001)
                ======================

                Features
                --------

                - Baz levitation (baz)
                - Baz fix levitation (fix-1.2)
                - Adds levitation (#123)
                - Extends levitation (#124)
                - An orphaned feature ending with a dotted number
                - An orphaned feature ending with a number
                - An orphaned feature starting with a dotted number
                - An orphaned feature starting with a number
                - Another orphaned feature
                - Orphaned feature



                """
            ),
        )

    def test_command(self):
        self._test_command(cli)

    def test_subcommand(self):
        self._test_command(_main)

    @with_project()
    def test_in_different_dir_dir_option(self, runner):
        """
        The current working directory doesn't matter as long as we pass
        the correct one.
        """
        project_dir = Path(".").resolve()

        Path("foo/newsfragments/123.feature").write_text("Adds levitation")
        # Ensure our assetion below is meaningful.
        self.assertFalse((project_dir / "NEWS.rst").exists())

        # Create a temporary directory, run Towncrier from there and assert
        # it didn't litter into it.
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)

        os.chdir(td.name)
        result = runner.invoke(cli, ("--yes", "--dir", str(project_dir)))

        self.assertEqual([], list(Path(td.name).glob("*")))
        self.assertEqual(0, result.exit_code)
        self.assertTrue((project_dir / "NEWS.rst").exists())

    @with_project()
    def test_traverse_up_to_find_config(self, runner):
        """
        When the current directory doesn't contain the configuration file, Towncrier
        will traverse up the directory tree until it finds it.
        """
        os.chdir("foo")
        result = runner.invoke(_main, ["--draft", "--date", "01-01-2001"])
        self.assertEqual(0, result.exit_code, result.output)

    @with_project()
    def test_in_different_dir_config_option(self, runner):
        """
        The current working directory and the location of the configuration
        don't matter as long as we pass correct paths to the directory and the
        config file.
        """
        project_dir = Path(".").resolve()

        Path("foo/newsfragments/123.feature").write_text("Adds levitation")
        # Ensure our assetion below is meaningful.
        self.assertFalse((project_dir / "NEWS.rst").exists())

        # Create a temporary directory, move the config file there, run
        # Towncrier from there, and assert it didn't litter into it.
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)

        os.chdir(td.name)
        (project_dir / "pyproject.toml").rename("pyproject.toml")
        result = runner.invoke(
            cli, ("--yes", "--config", "pyproject.toml", "--dir", str(project_dir))
        )

        # There's only pyproject.toml in this directory.
        self.assertEqual(
            [Path(td.name) / "pyproject.toml"], list(Path(td.name).glob("*"))
        )
        self.assertEqual(0, result.exit_code)
        self.assertTrue((project_dir / "NEWS.rst").exists())

    @with_project(
        config="""
        [tool.towncrier]
        directory = "changelog.d"
        """
    )
    def test_in_different_dir_with_nondefault_newsfragments_directory(self, runner):
        """
        Using the `--dir` CLI argument, the NEWS file can
        be generated in a sub-directory from fragments
        that are relatives to that sub-directory.

        The path passed to `--dir` becomes the
        working directory.
        """
        Path("foo/foo").mkdir(parents=True)
        Path("foo/foo/__init__.py").write_text("")
        Path("foo/changelog.d").mkdir()
        Path("foo/changelog.d/123.feature").write_text("Adds levitation")
        self.assertFalse(Path("foo/NEWS.rst").exists())

        result = runner.invoke(
            cli,
            ("--yes", "--config", "pyproject.toml", "--dir", "foo", "--version", "1.0"),
        )

        self.assertEqual(0, result.exit_code)
        self.assertTrue(Path("foo/NEWS.rst").exists())

    @with_project()
    def test_no_newsfragment_directory(self, runner):
        """
        A missing newsfragment directory acts as if there are no changes.
        """
        os.rmdir("foo/newsfragments")

        result = runner.invoke(_main, ["--draft", "--date", "01-01-2001"])

        self.assertEqual(0, result.exit_code)
        self.assertIn("No significant changes.\n", result.output)

    @with_project()
    def test_no_newsfragments_draft(self, runner):
        """
        An empty newsfragment directory acts as if there are no changes.
        """
        result = runner.invoke(_main, ["--draft", "--date", "01-01-2001"])

        self.assertEqual(0, result.exit_code)
        self.assertIn("No significant changes.\n", result.output)

    @with_project()
    def test_no_newsfragments(self, runner):
        """
        An empty newsfragment directory acts as if there are no changes and
        removing files handles it gracefully.
        """
        result = runner.invoke(_main, ["--date", "01-01-2001"])

        news = read("NEWS.rst")

        self.assertEqual(0, result.exit_code)
        self.assertIn("No significant changes.\n", news)

    @with_project()
    def test_collision(self, runner):
        # Note that both are 123.feature
        with open("foo/newsfragments/123.feature", "w") as f:
            f.write("Adds levitation")
        with open("foo/newsfragments/123.feature.rst", "w") as f:
            f.write("Extends levitation")

        result = runner.invoke(_main, ["--draft", "--date", "01-01-2001"])

        # This should fail
        self.assertEqual(type(result.exception), ValueError)
        self.assertIn("multiple files for 123.feature", str(result.exception))

    def test_section_and_type_sorting(self):
        """
        Sections and types should be output in the same order that they're
        defined in the config file.
        """

        runner = CliRunner()

        def run_order_scenario(sections, types):
            with runner.isolated_filesystem():
                with open("pyproject.toml", "w") as f:
                    f.write(
                        dedent(
                            """
                    [tool.towncrier]
                        package = "foo"
                        directory = "news"

                    """
                        )
                    )

                    for section in sections:
                        f.write(
                            dedent(
                                """
                        [[tool.towncrier.section]]
                            path = "{section}"
                            name = "{section}"
                        """.format(
                                    section=section
                                )
                            )
                        )

                    for type_ in types:
                        f.write(
                            dedent(
                                """
                        [[tool.towncrier.type]]
                            directory = "{type_}"
                            name = "{type_}"
                            showcontent = true
                        """.format(
                                    type_=type_
                                )
                            )
                        )

                os.mkdir("foo")
                with open("foo/__init__.py", "w") as f:
                    f.write('__version__ = "1.2.3"\n')
                os.mkdir("news")
                for section in sections:
                    sectdir = "news/" + section
                    os.mkdir(sectdir)
                    for type_ in types:
                        with open(f"{sectdir}/1.{type_}", "w") as f:
                            f.write(f"{section} {type_}")

                return runner.invoke(
                    _main, ["--draft", "--date", "01-01-2001"], catch_exceptions=False
                )

        result = run_order_scenario(["section-a", "section-b"], ["type-1", "type-2"])
        self.assertEqual(0, result.exit_code)
        self.assertEqual(
            result.output,
            "Loading template...\nFinding news fragments...\nRendering news "
            "fragments...\nDraft only -- nothing has been written.\nWhat is "
            "seen below is what would be written.\n\nFoo 1.2.3 (01-01-2001)"
            "\n======================"
            + dedent(
                """
                  section-a
                  ---------

                  type-1
                  ~~~~~~

                  - section-a type-1 (#1)


                  type-2
                  ~~~~~~

                  - section-a type-2 (#1)


                  section-b
                  ---------

                  type-1
                  ~~~~~~

                  - section-b type-1 (#1)


                  type-2
                  ~~~~~~

                  - section-b type-2 (#1)



            """
            ),
        )

        result = run_order_scenario(["section-b", "section-a"], ["type-2", "type-1"])
        self.assertEqual(0, result.exit_code)
        self.assertEqual(
            result.output,
            "Loading template...\nFinding news fragments...\nRendering news "
            "fragments...\nDraft only -- nothing has been written.\nWhat is "
            "seen below is what would be written.\n\nFoo 1.2.3 (01-01-2001)"
            "\n======================"
            + dedent(
                """
                  section-b
                  ---------

                  type-2
                  ~~~~~~

                  - section-b type-2 (#1)


                  type-1
                  ~~~~~~

                  - section-b type-1 (#1)


                  section-a
                  ---------

                  type-2
                  ~~~~~~

                  - section-a type-2 (#1)


                  type-1
                  ~~~~~~

                  - section-a type-1 (#1)



            """
            ),
        )

    @with_git_project()
    def test_draft_no_date(self, runner, commit):
        """
        If no date is passed, today's date is used.
        """
        fragment_path1 = "foo/newsfragments/123.feature"
        fragment_path2 = "foo/newsfragments/124.feature.rst"
        with open(fragment_path1, "w") as f:
            f.write("Adds levitation")
        with open(fragment_path2, "w") as f:
            f.write("Extends levitation")

        commit()

        today = date.today()
        result = runner.invoke(_main, ["--draft"])

        self.assertEqual(0, result.exit_code)
        self.assertIn(f"Foo 1.2.3 ({today.isoformat()})", result.output)

    @with_git_project()
    def test_no_confirmation(self, runner, commit):
        fragment_path1 = "foo/newsfragments/123.feature"
        fragment_path2 = "foo/newsfragments/124.feature.rst"
        with open(fragment_path1, "w") as f:
            f.write("Adds levitation")
        with open(fragment_path2, "w") as f:
            f.write("Extends levitation")

        commit()

        result = runner.invoke(_main, ["--date", "01-01-2001", "--yes"])

        self.assertEqual(0, result.exit_code)
        path = "NEWS.rst"
        self.assertTrue(os.path.isfile(path))
        self.assertFalse(os.path.isfile(fragment_path1))
        self.assertFalse(os.path.isfile(fragment_path2))

    @with_git_project()
    def test_keep_fragments(self, runner, commit):
        """
        The `--keep` option will build the full final news file
        without deleting the fragment files and without
        any extra CLI interaction or confirmation.
        """
        fragment_path1 = "foo/newsfragments/123.feature"
        fragment_path2 = "foo/newsfragments/124.feature.rst"
        with open(fragment_path1, "w") as f:
            f.write("Adds levitation")
        with open(fragment_path2, "w") as f:
            f.write("Extends levitation")

        commit()

        result = runner.invoke(_main, ["--date", "01-01-2001", "--keep"])

        self.assertEqual(0, result.exit_code)
        # The NEWS file is created.
        # So this is not just `--draft`.
        self.assertTrue(os.path.isfile("NEWS.rst"))
        self.assertTrue(os.path.isfile(fragment_path1))
        self.assertTrue(os.path.isfile(fragment_path2))

    @with_git_project()
    def test_yes_keep_error(self, runner, commit):
        """
        It will fail to perform any action when the
        conflicting --keep and --yes options are provided.

        Called twice with the different order of --keep and --yes options
        to make sure both orders are validated since click triggers the validator
        in the order it parses the command line.
        """
        fragment_path1 = "foo/newsfragments/123.feature"
        fragment_path2 = "foo/newsfragments/124.feature.rst"
        with open(fragment_path1, "w") as f:
            f.write("Adds levitation")
        with open(fragment_path2, "w") as f:
            f.write("Extends levitation")

        commit()

        result = runner.invoke(_main, ["--date", "01-01-2001", "--yes", "--keep"])
        self.assertEqual(1, result.exit_code)

        result = runner.invoke(_main, ["--date", "01-01-2001", "--keep", "--yes"])
        self.assertEqual(1, result.exit_code)

    @with_git_project()
    def test_confirmation_says_no(self, runner, commit):
        """
        If the user says "no" to removing the newsfragements, we end up with
        a NEWS.rst AND the newsfragments.
        """
        fragment_path1 = "foo/newsfragments/123.feature"
        fragment_path2 = "foo/newsfragments/124.feature.rst"
        with open(fragment_path1, "w") as f:
            f.write("Adds levitation")
        with open(fragment_path2, "w") as f:
            f.write("Extends levitation")

        commit()

        with patch("towncrier.build.click.confirm") as m:
            m.return_value = False
            result = runner.invoke(_main, [])

        self.assertEqual(0, result.exit_code)
        path = "NEWS.rst"
        self.assertTrue(os.path.isfile(path))
        self.assertTrue(os.path.isfile(fragment_path1))
        self.assertTrue(os.path.isfile(fragment_path2))

    def test_needs_config(self):
        """
        Towncrier needs a configuration file.
        """
        runner = CliRunner()

        with runner.isolated_filesystem():
            result = runner.invoke(_main, ["--draft"])

        self.assertEqual(1, result.exit_code, result.output)
        self.assertTrue(result.output.startswith("No configuration file found."))

    @with_project(config="[tool.towncrier]")
    def test_needs_version(self, runner: CliRunner):
        """
        If the configuration file doesn't specify a version or a package, the version
        option is required.
        """
        result = runner.invoke(_main, ["--draft"], catch_exceptions=False)

        self.assertEqual(2, result.exit_code)
        self.assertIn("Error: '--version' is required", result.output)

    @with_project()
    def test_projectless_changelog(self, runner):
        """In which a directory containing news files is built into a changelog

        - without a Python project or version number. We override the
        project title from the commandline.
        """
        # Remove the version from the project
        Path("foo/__init__.py").unlink()

        with open("foo/newsfragments/123.feature", "w") as f:
            f.write("Adds levitation")
        # Towncrier ignores .rst extension
        with open("foo/newsfragments/124.feature.rst", "w") as f:
            f.write("Extends levitation")

        result = runner.invoke(
            _main,
            [
                "--name",
                "FooBarBaz",
                "--version",
                "7.8.9",
                "--date",
                "01-01-2001",
                "--draft",
            ],
        )

        self.assertEqual(0, result.exit_code)
        self.assertEqual(
            result.output,
            dedent(
                """
            Loading template...
            Finding news fragments...
            Rendering news fragments...
            Draft only -- nothing has been written.
            What is seen below is what would be written.

            FooBarBaz 7.8.9 (01-01-2001)
            ============================

            Features
            --------

            - Adds levitation (#123)
            - Extends levitation (#124)



            """
            ).lstrip(),
        )

    @with_project(
        config="""
        [tool.towncrier]
        version = "7.8.9"
        """
    )
    def test_version_in_config(self, runner):
        """Calling towncrier with version defined in configfile.

        Specifying a version in toml file will be helpful if version
        is maintained by i.e. bumpversion and it's not a python project.
        """
        os.mkdir("newsfragments")
        with open("newsfragments/123.feature", "w") as f:
            f.write("Adds levitation")

        result = runner.invoke(_main, ["--date", "01-01-2001", "--draft"])

        self.assertEqual(0, result.exit_code, result.output)
        self.assertEqual(
            result.output,
            dedent(
                """
            Loading template...
            Finding news fragments...
            Rendering news fragments...
            Draft only -- nothing has been written.
            What is seen below is what would be written.

            7.8.9 (01-01-2001)
            ==================

            Features
            --------

            - Adds levitation (#123)



            """
            ).lstrip(),
        )

    @with_project(
        config="""
        [tool.towncrier]
        name = "ImGoProject"
        """
    )
    def test_project_name_in_config(self, runner):
        """The calling towncrier with project name defined in configfile.

        Specifying a project name in toml file will be helpful to keep the
        project name consistent as part of the towncrier configuration, not call.
        """
        os.mkdir("newsfragments")
        with open("newsfragments/123.feature", "w") as f:
            f.write("Adds levitation")

        result = runner.invoke(
            _main, ["--version", "7.8.9", "--date", "01-01-2001", "--draft"]
        )

        self.assertEqual(0, result.exit_code, result.output)
        self.assertEqual(
            result.output,
            dedent(
                """
            Loading template...
            Finding news fragments...
            Rendering news fragments...
            Draft only -- nothing has been written.
            What is seen below is what would be written.

            ImGoProject 7.8.9 (01-01-2001)
            ==============================

            Features
            --------

            - Adds levitation (#123)



            """
            ).lstrip(),
        )

    @with_project(config="[tool.towncrier]")
    def test_no_package_changelog(self, runner):
        """The calling towncrier with any package argument.

        Specifying a package in the toml file or the command line
        should not always be needed:
        - we can set the version number on the command line,
          so we do not need the package for that.
        - we don't need to include the package in the changelog header.
        """
        os.mkdir("newsfragments")
        with open("newsfragments/123.feature", "w") as f:
            f.write("Adds levitation")

        result = runner.invoke(
            _main, ["--version", "7.8.9", "--date", "01-01-2001", "--draft"]
        )

        self.assertEqual(0, result.exit_code, result.output)
        self.assertEqual(
            result.output,
            dedent(
                """
            Loading template...
            Finding news fragments...
            Rendering news fragments...
            Draft only -- nothing has been written.
            What is seen below is what would be written.

            7.8.9 (01-01-2001)
            ==================

            Features
            --------

            - Adds levitation (#123)



            """
            ).lstrip(),
        )

    @with_project(
        config="""
        [tool.towncrier]
         single_file=false
         filename="{version}-notes.rst"
        """
    )
    def test_release_notes_in_separate_files(self, runner):
        """
        When `single_file = false` the release notes for each version are stored
        in a separate file.
        The name of the file is defined by the `filename` configuration value.
        """

        def do_build_once_with(version, fragment_file, fragment):
            with open(f"newsfragments/{fragment_file}", "w") as f:
                f.write(fragment)

            result = runner.invoke(
                _main,
                [
                    "--version",
                    version,
                    "--name",
                    "foo",
                    "--date",
                    "01-01-2001",
                    "--yes",
                ],
            )
            # not git repository, manually remove fragment file
            Path(f"newsfragments/{fragment_file}").unlink()
            return result

        results = []
        os.mkdir("newsfragments")
        results.append(do_build_once_with("7.8.9", "123.feature", "Adds levitation"))
        results.append(do_build_once_with("7.9.0", "456.bugfix", "Adds catapult"))

        self.assertEqual(0, results[0].exit_code, results[0].output)
        self.assertEqual(0, results[1].exit_code, results[1].output)
        self.assertEqual(
            2,
            len(list(Path.cwd().glob("*-notes.rst"))),
            "one newfile for each build",
        )
        self.assertTrue(os.path.exists("7.8.9-notes.rst"), os.listdir("."))
        self.assertTrue(os.path.exists("7.9.0-notes.rst"), os.listdir("."))

        outputs = []
        outputs.append(read("7.8.9-notes.rst"))
        outputs.append(read("7.9.0-notes.rst"))

        self.assertEqual(
            outputs[0],
            dedent(
                """
            foo 7.8.9 (01-01-2001)
            ======================

            Features
            --------

            - Adds levitation (#123)
            """
            ).lstrip(),
        )
        self.assertEqual(
            outputs[1],
            dedent(
                """
            foo 7.9.0 (01-01-2001)
            ======================

            Bugfixes
            --------

            - Adds catapult (#456)
            """
            ).lstrip(),
        )

    @with_project(
        config="""
        [tool.towncrier]
        singlefile="fail!"
        """
    )
    def test_singlefile_errors_and_explains_cleanly(self, runner):
        """
        Failure to find the configuration file results in a clean explanation
        without a traceback.
        """
        result = runner.invoke(_main)

        self.assertEqual(1, result.exit_code)
        self.assertEqual(
            "`singlefile` is not a valid option. Did you mean `single_file`?\n",
            result.output,
        )

    def test_all_version_notes_in_a_single_file(self):
        """
        When `single_file = true` the single file is used to store the notes
        for multiple versions.

        The name of the file is fixed as the literal option `filename` option
        in the configuration file, instead of extrapolated with variables.
        """
        runner = CliRunner()

        def do_build_once_with(version, fragment_file, fragment):
            with open(f"newsfragments/{fragment_file}", "w") as f:
                f.write(fragment)

            result = runner.invoke(
                _main,
                [
                    "--version",
                    version,
                    "--name",
                    "foo",
                    "--date",
                    "01-01-2001",
                    "--yes",
                ],
                catch_exceptions=False,
            )
            # not git repository, manually remove fragment file
            Path(f"newsfragments/{fragment_file}").unlink()
            return result

        results = []
        with runner.isolated_filesystem():
            with open("pyproject.toml", "w") as f:
                f.write(
                    "\n".join(
                        [
                            "[tool.towncrier]",
                            " single_file=true",
                            " # The `filename` variable is fixed and not formated in any way.",
                            ' filename="{version}-notes.rst"',
                        ]
                    )
                )
            os.mkdir("newsfragments")
            results.append(
                do_build_once_with("7.8.9", "123.feature", "Adds levitation")
            )
            results.append(do_build_once_with("7.9.0", "456.bugfix", "Adds catapult"))

            self.assertEqual(0, results[0].exit_code, results[0].output)
            self.assertEqual(0, results[1].exit_code, results[1].output)
            self.assertEqual(
                1,
                len(list(Path.cwd().glob("*-notes.rst"))),
                "single newfile for multiple builds",
            )
            self.assertTrue(os.path.exists("{version}-notes.rst"), os.listdir("."))

            output = read("{version}-notes.rst")

            self.assertEqual(
                output,
                dedent(
                    """
                foo 7.9.0 (01-01-2001)
                ======================

                Bugfixes
                --------

                - Adds catapult (#456)


                foo 7.8.9 (01-01-2001)
                ======================

                Features
                --------

                - Adds levitation (#123)
                """
                ).lstrip(),
            )

    @with_project(
        config="""
        [tool.towncrier]
        template="towncrier:single-file-no-bullets"
        all_bullets=false
        """
    )
    def test_bullet_points_false(self, runner):
        """
        When all_bullets is false, subsequent lines are not indented.

        The automatic issue number inserted by towncrier will align with the
        manual bullet.
        """
        os.mkdir("newsfragments")
        with open("newsfragments/123.feature", "w") as f:
            f.write("wow!\n~~~~\n\nNo indentation at all.")
        with open("newsfragments/124.bugfix", "w") as f:
            f.write("#. Numbered bullet list.")
        with open("newsfragments/125.removal", "w") as f:
            f.write("- Hyphen based bullet list.")
        with open("newsfragments/126.doc", "w") as f:
            f.write("* Asterisk based bullet list.")

        result = runner.invoke(
            _main,
            [
                "--version",
                "7.8.9",
                "--name",
                "foo",
                "--date",
                "01-01-2001",
                "--yes",
            ],
        )

        self.assertEqual(0, result.exit_code, result.output)
        output = read("NEWS.rst")

        self.assertEqual(
            output,
            dedent(
                """
                foo 7.8.9 (01-01-2001)
                ======================

                Features
                --------

                wow!
                ~~~~

                No indentation at all.
                (#123)


                Bugfixes
                --------

                #. Numbered bullet list.
                   (#124)


                Improved Documentation
                ----------------------

                * Asterisk based bullet list.
                  (#126)


                Deprecations and Removals
                -------------------------

                - Hyphen based bullet list.
                  (#125)
                """
            ).lstrip(),
        )

    @with_project(
        config="""
        [tool.towncrier]
        package = "foo"
        title_format = "[{project_date}] CUSTOM RELEASE for {name} version {version}"
        """
    )
    def test_title_format_custom(self, runner):
        """
        A non-empty title format adds the specified title.
        """
        with open("foo/newsfragments/123.feature", "w") as f:
            f.write("Adds levitation")
        # Towncrier ignores .rst extension
        with open("foo/newsfragments/124.feature.rst", "w") as f:
            f.write("Extends levitation")

        result = runner.invoke(
            _main,
            [
                "--name",
                "FooBarBaz",
                "--version",
                "7.8.9",
                "--date",
                "20-01-2001",
                "--draft",
            ],
        )

        expected_output = dedent(
            """\
            Loading template...
            Finding news fragments...
            Rendering news fragments...
            Draft only -- nothing has been written.
            What is seen below is what would be written.

            [20-01-2001] CUSTOM RELEASE for FooBarBaz version 7.8.9
            =======================================================

            Features
            --------

            - Adds levitation (#123)
            - Extends levitation (#124)



        """
        )

        self.assertEqual(0, result.exit_code)
        self.assertEqual(expected_output, result.output)

    @with_project(
        config="""
        [tool.towncrier]
        package = "foo"
        filename = "NEWS.md"
        title_format = "[{project_date}] CUSTOM RELEASE for {name} version {version}"
        """
    )
    def test_title_format_custom_markdown(self, runner):
        """
        A non-empty title format adds the specified title, and if the target filename is
        markdown then the title is added as a markdown header.
        """
        with open("foo/newsfragments/123.feature", "w") as f:
            f.write("Adds levitation")
        result = runner.invoke(
            _main,
            [
                "--name",
                "FooBarBaz",
                "--version",
                "7.8.9",
                "--date",
                "20-01-2001",
                "--draft",
            ],
        )

        expected_output = dedent(
            """\
            Loading template...
            Finding news fragments...
            Rendering news fragments...
            Draft only -- nothing has been written.
            What is seen below is what would be written.

            # [20-01-2001] CUSTOM RELEASE for FooBarBaz version 7.8.9

            ### Features

            - Adds levitation (#123)



        """
        )

        self.assertEqual(0, result.exit_code)
        self.assertEqual(expected_output, result.output)

    @with_project(
        config="""
        [tool.towncrier]
        package = "foo"
        title_format = false
        template = "template.rst"
        """
    )
    def test_title_format_false(self, runner):
        """
        Setting the title format to false disables the explicit title.  This
        would be used, for example, when the template creates the title itself.
        """
        with open("template.rst", "w") as f:
            f.write(
                dedent(
                    """\
                Here's a hardcoded title added by the template
                ==============================================
                {% for section in sections %}
                {% set underline = "-" %}
                {% for category, val in definitions.items() if category in sections[section] %}

                {% for text, values in sections[section][category]|dictsort(by='value') %}
                - {{ text }}

                {% endfor %}
                {% endfor %}
                {% endfor %}
            """
                )
            )

        result = runner.invoke(
            _main,
            [
                "--name",
                "FooBarBaz",
                "--version",
                "7.8.9",
                "--date",
                "20-01-2001",
                "--draft",
            ],
            catch_exceptions=False,
        )

        expected_output = dedent(
            """\
            Loading template...
            Finding news fragments...
            Rendering news fragments...
            Draft only -- nothing has been written.
            What is seen below is what would be written.

            Here's a hardcoded title added by the template
            ==============================================

        """
        )

        self.assertEqual(0, result.exit_code)
        self.assertEqual(expected_output, result.output)

    @with_project(
        config="""
        [tool.towncrier]
        start_string="Release notes start marker"
        """
    )
    def test_start_string(self, runner):
        """
        The `start_string` configuration is used to detect the starting point
        for inserting the generated release notes. A newline is automatically
        added to the configured value.
        """
        os.mkdir("newsfragments")
        with open("newsfragments/123.feature", "w") as f:
            f.write("Adds levitation")
        with open("NEWS.rst", "w") as f:
            f.write("a line\n\nanother\n\nRelease notes start marker\na footer!\n")

        result = runner.invoke(
            _main,
            [
                "--version",
                "7.8.9",
                "--name",
                "foo",
                "--date",
                "01-01-2001",
                "--yes",
            ],
        )

        self.assertEqual(0, result.exit_code, result.output)
        self.assertTrue(os.path.exists("NEWS.rst"), os.listdir("."))
        output = read("NEWS.rst")

        expected_output = dedent(
            """\
            a line

            another

            Release notes start marker
            foo 7.8.9 (01-01-2001)
            ======================

            Features
            --------

            - Adds levitation (#123)


            a footer!
        """
        )

        self.assertEqual(expected_output, output)

    @with_project()
    def test_default_start_string(self, runner):
        """
        The default start string is ``.. towncrier release notes start``.
        """
        write("foo/newsfragments/123.feature", "Adds levitation")
        write(
            "NEWS.rst",
            contents="""
                a line

                another

                .. towncrier release notes start

                a footer!
            """,
            dedent=True,
        )

        result = runner.invoke(_main, ["--date", "01-01-2001"], catch_exceptions=False)
        self.assertEqual(0, result.exit_code, result.output)
        output = read("NEWS.rst")

        expected_output = dedent(
            """
            a line

            another

            .. towncrier release notes start

            Foo 1.2.3 (01-01-2001)
            ======================

            Features
            --------

            - Adds levitation (#123)


            a footer!
            """
        )

        self.assertEqual(expected_output, output)

    @with_project(
        config="""
        [tool.towncrier]
        package = "foo"
        filename = "NEWS.md"
        """
    )
    def test_default_start_string_markdown(self, runner):
        """
        The default start string is ``<!-- towncrier release notes start -->`` for
        Markdown.
        """
        write("foo/newsfragments/123.feature", "Adds levitation")
        write(
            "NEWS.md",
            contents="""
                a line

                another

                <!-- towncrier release notes start -->

                a footer!
            """,
            dedent=True,
        )

        result = runner.invoke(_main, ["--date", "01-01-2001"], catch_exceptions=False)
        self.assertEqual(0, result.exit_code, result.output)
        output = read("NEWS.md")

        expected_output = dedent(
            """
            a line

            another

            <!-- towncrier release notes start -->

            # Foo 1.2.3 (01-01-2001)

            ### Features

            - Adds levitation (#123)


            a footer!
            """
        )

        self.assertEqual(expected_output, output)

    @with_project(
        config="""
        [tool.towncrier]
        name = ""
        directory = "changes"
        filename = "NEWS.md"
        version = "1.2.3"
        """
    )
    def test_markdown_no_name_title(self, runner):
        """
        When configured with an empty `name` option,
        the default template used for Markdown
        renders the title of the release note with just
        the version number and release date.
        """
        write("changes/123.feature", "Adds levitation")
        write(
            "NEWS.md",
            contents="""
                A line

                <!-- towncrier release notes start -->
            """,
            dedent=True,
        )

        result = runner.invoke(_main, ["--date", "01-01-2001"], catch_exceptions=False)
        self.assertEqual(0, result.exit_code, result.output)
        output = read("NEWS.md")

        expected_output = dedent(
            """
            A line

            <!-- towncrier release notes start -->

            # 1.2.3 (01-01-2001)

            ### Features

            - Adds levitation (#123)
            """
        )

        self.assertEqual(expected_output, output)

    @with_project(
        config="""
        [tool.towncrier]
        title_format = "{version} - {project_date}"
        template = "template.rst"

          [[tool.towncrier.type]]
          directory = "feature"
          name = ""
          showcontent = true
        """
    )
    def test_with_topline_and_template_and_draft(self, runner):
        """
        Spacing is proper when drafting with a topline and a template.
        """
        os.mkdir("newsfragments")
        with open("newsfragments/123.feature", "w") as f:
            f.write("Adds levitation")
        with open("template.rst", "w") as f:
            f.write(
                dedent(
                    """\
                {% for section in sections %}
                {% set underline = "-" %}
                {% for category, val in definitions.items() if category in sections[section] %}

                {% for text, values in sections[section][category]|dictsort(by='value') %}
                - {{ text }}

                {% endfor %}
                {% endfor %}
                {% endfor %}
            """
                )
            )

        result = runner.invoke(
            _main,
            [
                "--version=7.8.9",
                "--name=foo",
                "--date=20-01-2001",
                "--draft",
            ],
        )

        expected_output = dedent(
            """\
            Loading template...
            Finding news fragments...
            Rendering news fragments...
            Draft only -- nothing has been written.
            What is seen below is what would be written.

            7.8.9 - 20-01-2001
            ==================

            - Adds levitation


        """
        )

        self.assertEqual(0, result.exit_code, result.output)
        self.assertEqual(expected_output, result.output)

    @with_project(
        config="""
        [tool.towncrier]
        """
    )
    def test_orphans_in_non_showcontent(self, runner):
        """
        When ``showcontent`` is false (like in the ``misc`` category by default),
        orphans are still rendered because they don't have an issue number to display.
        """
        os.mkdir("newsfragments")
        with open("newsfragments/123.misc", "w") as f:
            f.write("Misc")
        with open("newsfragments/345.misc", "w") as f:
            f.write("Another misc")
        with open("newsfragments/+.misc", "w") as f:
            f.write("Orphan misc still displayed!")
        with open("newsfragments/+2.misc", "w") as f:
            f.write("Another orphan misc still displayed!")

        result = runner.invoke(
            _main,
            [
                "--version=7.8.9",
                "--date=20-01-2001",
                "--draft",
            ],
        )

        expected_output = dedent(
            """\
            Loading template...
            Finding news fragments...
            Rendering news fragments...
            Draft only -- nothing has been written.
            What is seen below is what would be written.

            7.8.9 (20-01-2001)
            ==================

            Misc
            ----

            - #123, #345
            - Another orphan misc still displayed!
            - Orphan misc still displayed!



        """
        )

        self.assertEqual(0, result.exit_code, result.output)
        self.assertEqual(expected_output, result.output)

    @with_project(
        config="""
        [tool.towncrier]
        filename = "CHANGES.md"
        """
    )
    def test_orphans_in_non_showcontent_markdown(self, runner):
        """
        When ``showcontent`` is false (like in the ``misc`` category by default),
        orphans are still rendered because they don't have an issue number to display.
        """
        os.mkdir("newsfragments")
        with open("newsfragments/123.misc", "w") as f:
            f.write("Misc")
        with open("newsfragments/345.misc", "w") as f:
            f.write("Another misc")
        with open("newsfragments/+.misc", "w") as f:
            f.write("Orphan misc still displayed!")
        with open("newsfragments/+2.misc", "w") as f:
            f.write("Another orphan misc still displayed!")

        result = runner.invoke(
            _main,
            [
                "--version=7.8.9",
                "--date=20-01-2001",
                "--draft",
            ],
        )

        expected_output = dedent(
            """\
            Loading template...
            Finding news fragments...
            Rendering news fragments...
            Draft only -- nothing has been written.
            What is seen below is what would be written.

            # 7.8.9 (20-01-2001)

            ### Misc

            - #123, #345
            - Another orphan misc still displayed!
            - Orphan misc still displayed!



        """
        )

        self.assertEqual(0, result.exit_code, result.output)
        self.assertEqual(expected_output, result.output)

    @with_project(
        config="""
        [tool.towncrier]
        package = "foo"
        build_ignore_filenames = ["template.jinja", "CAPYBARAS.md"]
        """
    )
    def test_invalid_fragment_names(self, runner):
        """
        When build_ignore_filenames is set, files with those names are ignored.
        """
        opts = ["--draft", "--date", "01-01-2001", "--version", "1.0.0"]
        # Valid filename:
        with open("foo/newsfragments/123.feature", "w") as f:
            f.write("Adds levitation")
        # Files that should be ignored:
        with open("foo/newsfragments/template.jinja", "w") as f:
            f.write("Jinja template")
        with open("foo/newsfragments/CAPYBARAS.md", "w") as f:
            f.write("Peanut butter")
        # Automatically ignored:
        with open("foo/newsfragments/.gitignore", "w") as f:
            f.write("!.gitignore")

        result = runner.invoke(_main, opts)
        # Should succeed
        self.assertEqual(0, result.exit_code, result.output)

        # Invalid filename:
        with open("foo/newsfragments/feature.124", "w") as f:
            f.write("Extends levitation")

        result = runner.invoke(_main, opts)
        # Should now fail
        self.assertEqual(1, result.exit_code, result.output)
        self.assertIn("Invalid news fragment name: feature.124", result.output)

    @with_project()
    def test_invalid_fragment_names_strict(self, runner):
        """
        When using --strict, any invalid filenames will cause an error even if
        build_ignore_filenames is NOT set.
        """
        opts = ["--draft", "--date", "01-01-2001", "--version", "1.0.0"]
        # Invalid filename:
        with open("foo/newsfragments/feature.124", "w") as f:
            f.write("Extends levitation")

        result = runner.invoke(_main, opts)
        # Should succeed in normal mode
        self.assertEqual(0, result.exit_code, result.output)

        result = runner.invoke(_main, [*opts, "--strict"])
        # Should now fail
        self.assertEqual(1, result.exit_code, result.output)
        self.assertIn("Invalid news fragment name: feature.124", result.output)
