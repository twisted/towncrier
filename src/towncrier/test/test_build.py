# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

import os

from pathlib import Path
from subprocess import call
from textwrap import dedent

from click.testing import CliRunner
from twisted.trial.unittest import TestCase

from .._shell import cli
from ..build import _main


def setup_simple_project():
    with open("pyproject.toml", "w") as f:
        f.write("[tool.towncrier]\n" 'package = "foo"\n')
    os.mkdir("foo")
    with open("foo/__init__.py", "w") as f:
        f.write('__version__ = "1.2.3"\n')
    os.mkdir("foo/newsfragments")


class TestCli(TestCase):
    maxDiff = None

    def _test_command(self, command):
        runner = CliRunner()

        with runner.isolated_filesystem():
            setup_simple_project()
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
            # Towncrier ignores files that don't have a dot
            with open("foo/newsfragments/README", "w") as f:
                f.write("Blah blah")
            # And files that don't have a valid category
            with open("foo/newsfragments/README.rst", "w") as f:
                f.write("**Blah blah**")

            result = runner.invoke(command, ["--draft", "--date", "01-01-2001"])

        self.assertEqual(0, result.exit_code)
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
                - Baz fix levitation (#2)
                - Adds levitation (#123)
                - Extends levitation (#124)

                """
            ),
        )

    def test_command(self):
        self._test_command(cli)

    def test_subcommand(self):
        self._test_command(_main)

    def test_no_newsfragment_directory(self):
        """
        A missing newsfragment directory acts as if there are no changes.
        """
        runner = CliRunner()

        with runner.isolated_filesystem():
            setup_simple_project()
            os.rmdir("foo/newsfragments")

            result = runner.invoke(_main, ["--draft", "--date", "01-01-2001"])

        self.assertEqual(1, result.exit_code, result.output)
        self.assertIn("Failed to list the news fragment files.\n", result.output)

    def test_no_newsfragments(self):
        """
        An empty newsfragment directory acts as if there are no changes.
        """
        runner = CliRunner()

        with runner.isolated_filesystem():
            setup_simple_project()

            result = runner.invoke(_main, ["--draft", "--date", "01-01-2001"])

        self.assertEqual(0, result.exit_code)
        self.assertIn("No significant changes.\n", result.output)

    def test_collision(self):
        runner = CliRunner()

        with runner.isolated_filesystem():
            setup_simple_project()
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

    def test_no_confirmation(self):
        runner = CliRunner()

        with runner.isolated_filesystem():
            setup_simple_project()
            fragment_path1 = "foo/newsfragments/123.feature"
            fragment_path2 = "foo/newsfragments/124.feature.rst"
            with open(fragment_path1, "w") as f:
                f.write("Adds levitation")
            with open(fragment_path2, "w") as f:
                f.write("Extends levitation")

            call(["git", "init"])
            call(["git", "config", "user.name", "user"])
            call(["git", "config", "user.email", "user@example.com"])
            call(["git", "add", "."])
            call(["git", "commit", "-m", "Initial Commit"])

            result = runner.invoke(_main, ["--date", "01-01-2001", "--yes"])

            self.assertEqual(0, result.exit_code)
            path = "NEWS.rst"
            self.assertTrue(os.path.isfile(path))
            self.assertFalse(os.path.isfile(fragment_path1))
            self.assertFalse(os.path.isfile(fragment_path2))

    def test_needs_config(self):
        """
        Towncrier needs a configuration file.
        """
        runner = CliRunner()

        with runner.isolated_filesystem():
            result = runner.invoke(_main, ["--draft"])

        self.assertEqual(1, result.exit_code, result.output)
        self.assertTrue(result.output.startswith("No configuration file found."))

    def test_projectless_changelog(self):
        """In which a directory containing news files is built into a changelog

        - without a Python project or version number. We override the
        project title from the commandline.
        """
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open("pyproject.toml", "w") as f:
                f.write("[tool.towncrier]\n" 'package = "foo"\n')
            os.mkdir("foo")
            os.mkdir("foo/newsfragments")
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

    def test_version_in_config(self):
        """The calling towncrier with version defined in configfile.

        Specifying a version in toml file will be helpful if version
        is maintained by i.e. bumpversion and it's not a python project.
        """
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open("pyproject.toml", "w") as f:
                f.write("[tool.towncrier]\n" 'version = "7.8.9"\n')
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

    def test_project_name_in_config(self):
        """The calling towncrier with project name defined in configfile.

        Specifying a project name in toml file will be helpful to keep the
        project name consistent as part of the towncrier configuration, not call.
        """
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open("pyproject.toml", "w") as f:
                f.write("[tool.towncrier]\n" 'name = "ImGoProject"\n')
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

    def test_no_package_changelog(self):
        """The calling towncrier with any package argument.

        Specifying a package in the toml file or the command line
        should not always be needed:
        - we can set the version number on the command line,
          so we do not need the package for that.
        - we don't need to include the package in the changelog header.
        """
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open("pyproject.toml", "w") as f:
                f.write("[tool.towncrier]")
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

    def test_release_notes_in_separate_files(self):
        """
        When `single_file = false` the release notes for each version are stored
        in a separate file.
        The name of the file is defined by the `filename` configuration value.
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
                            " single_file=false",
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
                2,
                len(list(Path.cwd().glob("*-notes.rst"))),
                "one newfile for each build",
            )
            self.assertTrue(os.path.exists("7.8.9-notes.rst"), os.listdir("."))
            self.assertTrue(os.path.exists("7.9.0-notes.rst"), os.listdir("."))

            outputs = []
            with open("7.8.9-notes.rst") as f:
                outputs.append(f.read())
            with open("7.9.0-notes.rst") as f:
                outputs.append(f.read())

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

    def test_singlefile_errors_and_explains_cleanly(self):
        """
        Failure to find the configuration file results in a clean explanation
        without a traceback.
        """
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open("pyproject.toml", "w") as f:
                f.write('[tool.towncrier]\n singlefile="fail!"\n')

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

            with open("{version}-notes.rst") as f:
                output = f.read()

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

    def test_bullet_points_false(self):
        """
        When all_bullets is false, subsequent lines are not indented.

        The automatic ticket number inserted by towcier will allign with the
        manual bullet.
        """
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open("pyproject.toml", "w") as f:
                f.write(
                    "[tool.towncrier]\n"
                    'template="towncrier:single-file-no-bullets"\n'
                    "all_bullets=false"
                )
            os.mkdir("newsfragments")
            with open("newsfragments/123.feature", "w") as f:
                f.write("wow!\n" "~~~~\n" "\n" "No indentation at all.")
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
            with open("NEWS.rst") as f:
                output = f.read()

        self.assertEqual(
            output,
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
""".lstrip(),
        )

    def test_title_format_custom(self):
        """
        A non-empty title format adds the specified title.
        """
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open("pyproject.toml", "w") as f:
                f.write(
                    dedent(
                        """\
                    [tool.towncrier]
                    package = "foo"
                    title_format = "[{project_date}] CUSTOM RELEASE for {name} version {version}"
                """
                    )
                )
            os.mkdir("foo")
            os.mkdir("foo/newsfragments")
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

    def test_title_format_false(self):
        """
        Setting the title format to false disables the explicit title.  This
        would be used, for example, when the template creates the title itself.
        """
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open("pyproject.toml", "w") as f:
                f.write(
                    dedent(
                        """\
                    [tool.towncrier]
                    package = "foo"
                    title_format = false
                    template = "template.rst"
                """
                    )
                )
            os.mkdir("foo")
            os.mkdir("foo/newsfragments")
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

    def test_start_string(self):
        """
        The `start_string` configuration is used to detect the starting point
        for inserting the generated release notes. A newline is automatically
        added to the configured value.
        """
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open("pyproject.toml", "w") as f:
                f.write(
                    dedent(
                        """\
                    [tool.towncrier]
                    start_string="Release notes start marker"
                """
                    )
                )
            os.mkdir("newsfragments")
            with open("newsfragments/123.feature", "w") as f:
                f.write("Adds levitation")
            with open("NEWS.rst", "w") as f:
                f.write("a line\n\nanother\n\nRelease notes start marker\n")

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
            with open("NEWS.rst") as f:
                output = f.read()

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


        """
        )

        self.assertEqual(expected_output, output)

    def test_with_topline_and_template_and_draft(self):
        """
        Spacing is proper when drafting with a topline and a template.
        """
        runner = CliRunner()

        with runner.isolated_filesystem():
            with open("pyproject.toml", "w") as f:
                f.write(
                    dedent(
                        """\
                    [tool.towncrier]
                    title_format = "{version} - {project_date}"
                    template = "template.rst"

                      [[tool.towncrier.type]]
                      directory = "feature"
                      name = ""
                      showcontent = true
                """
                    )
                )
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
