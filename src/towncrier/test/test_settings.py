# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

import collections as clt
import os
import textwrap

from textwrap import dedent

from twisted.trial.unittest import TestCase

from .._settings import ConfigError, load_config


class TomlSettingsTests(TestCase):
    def test_base(self):
        """
        Test a "base config".
        """
        temp = self.mktemp()
        os.makedirs(temp)

        with open(os.path.join(temp, "pyproject.toml"), "w") as f:
            f.write(
                """[tool.towncrier]
package = "foobar"
orphan_prefix = "~"
"""
            )

        config = load_config(temp)
        self.assertEqual(config.package, "foobar")
        self.assertEqual(config.package_dir, ".")
        self.assertEqual(config.filename, "NEWS.rst")
        self.assertEqual(config.underlines, ["=", "-", "~"])
        self.assertEqual(config.orphan_prefix, "~")

    def test_missing(self):
        """
        If the config file doesn't have the correct toml key, we error.
        """
        temp = self.mktemp()
        os.makedirs(temp)

        with open(os.path.join(temp, "pyproject.toml"), "w") as f:
            f.write(
                dedent(
                    """
                [something.else]
                blah='baz'
                """
                )
            )

        with self.assertRaises(ConfigError) as e:
            load_config(temp)

        self.assertEqual(e.exception.failing_option, "all")

    def test_incorrect_single_file(self):
        """
        single_file must be a bool.
        """
        temp = self.mktemp()
        os.makedirs(temp)

        with open(os.path.join(temp, "pyproject.toml"), "w") as f:
            f.write(
                dedent(
                    """
                [tool.towncrier]
                single_file = "a"
                """
                )
            )

        with self.assertRaises(ConfigError) as e:
            load_config(temp)

        self.assertEqual(e.exception.failing_option, "single_file")

    def test_incorrect_all_bullets(self):
        """
        all_bullets must be a bool.
        """
        temp = self.mktemp()
        os.makedirs(temp)

        with open(os.path.join(temp, "pyproject.toml"), "w") as f:
            f.write(
                dedent(
                    """
                [tool.towncrier]
                all_bullets = "a"
                """
                )
            )

        with self.assertRaises(ConfigError) as e:
            load_config(temp)

        self.assertEqual(e.exception.failing_option, "all_bullets")

    def test_mistype_singlefile(self):
        """
        singlefile is not accepted, single_file is.
        """
        temp = self.mktemp()
        os.makedirs(temp)

        with open(os.path.join(temp, "pyproject.toml"), "w") as f:
            f.write(
                dedent(
                    """
                [tool.towncrier]
                singlefile = "a"
                """
                )
            )

        with self.assertRaises(ConfigError) as e:
            load_config(temp)

        self.assertEqual(e.exception.failing_option, "singlefile")

    def test_towncrier_toml_preferred(self):
        """
        Towncrier prefers the towncrier.toml for autodetect over pyproject.toml.
        """
        temp = self.mktemp()
        os.makedirs(temp)

        with open(os.path.join(temp, "towncrier.toml"), "w") as f:
            f.write(
                dedent(
                    """
                [tool.towncrier]
                package = "a"
                """
                )
            )

        with open(os.path.join(temp, "pyproject.toml"), "w") as f:
            f.write(
                dedent(
                    """
                [tool.towncrier]
                package = "b"
                """
                )
            )

        config = load_config(temp)
        self.assertEqual(config.package, "a")

    def test_missing_template(self):
        """
        Towncrier will raise an exception saying when it can't find a template.
        """
        temp = self.mktemp()
        os.makedirs(temp)

        with open(os.path.join(temp, "towncrier.toml"), "w") as f:
            f.write(
                dedent(
                    """
                [tool.towncrier]
                template = "foo.rst"
                """
                )
            )

        with self.assertRaises(ConfigError) as e:
            load_config(temp)

        self.assertEqual(
            str(e.exception),
            "The template file '{}' does not exist.".format(
                os.path.normpath(os.path.join(temp, "foo.rst")),
            ),
        )

    def test_missing_template_in_towncrier(self):
        """
        Towncrier will raise an exception saying when it can't find a template
        from the Towncrier templates.
        """
        temp = self.mktemp()
        os.makedirs(temp)

        with open(os.path.join(temp, "towncrier.toml"), "w") as f:
            f.write(
                dedent(
                    """
                [tool.towncrier]
                template = "towncrier:foo"
                """
                )
            )

        with self.assertRaises(ConfigError) as e:
            load_config(temp)

        self.assertEqual(
            str(e.exception), "Towncrier does not have a template named 'foo'."
        )

    def test_custom_types_as_tables_array_deprecated(self):
        """
        Custom fragment categories can be defined inside
        the toml config file using an array of tables
        (a table name in double brackets).

        This functionality is considered deprecated, but we continue
        to support it to keep backward compatibility.
        """
        toml_content = """
        [tool.towncrier]
        package = "foobar"
        [[tool.towncrier.type]]
        directory="foo"
        name="Foo"
        showcontent=false

        [[tool.towncrier.type]]
        directory="spam"
        name="Spam"
        showcontent=true
        """
        toml_content = textwrap.dedent(toml_content)
        expected = [
            (
                "foo",
                {
                    "name": "Foo",
                    "showcontent": False,
                },
            ),
            (
                "spam",
                {
                    "name": "Spam",
                    "showcontent": True,
                },
            ),
        ]
        expected = clt.OrderedDict(expected)
        config = self.load_config_from_string(
            toml_content,
        )
        actual = config.types
        self.assertDictEqual(expected, actual)

    def test_custom_types_as_tables(self):
        """
        Custom fragment categories can be defined inside
        the toml config file using tables.
        """
        test_project_path = self.mktemp()
        os.makedirs(test_project_path)
        toml_content = """
        [tool.towncrier]
        package = "foobar"
        [tool.towncrier.fragment.feat]
        ignored_field="Bazz"
        [tool.towncrier.fragment.fix]
        [tool.towncrier.fragment.chore]
        name = "Other Tasks"
        showcontent = false
        """
        toml_content = textwrap.dedent(toml_content)
        expected = [
            (
                "chore",
                {
                    "name": "Other Tasks",
                    "showcontent": False,
                },
            ),
            (
                "feat",
                {
                    "name": "Feat",
                    "showcontent": True,
                },
            ),
            (
                "fix",
                {
                    "name": "Fix",
                    "showcontent": True,
                },
            ),
        ]

        expected = clt.OrderedDict(expected)
        config = self.load_config_from_string(
            toml_content,
        )
        actual = config.types
        self.assertDictEqual(expected, actual)

    def load_config_from_string(self, toml_content):
        """Load configuration from a string.

        Given a string following toml syntax,
        obtain the towncrier configuration.
        """
        test_project_path = self.mktemp()
        os.makedirs(test_project_path)
        toml_path = os.path.join(test_project_path, "pyproject.toml")
        with open(toml_path, "w") as f:
            f.write(toml_content)
        config = load_config(test_project_path)
        return config
