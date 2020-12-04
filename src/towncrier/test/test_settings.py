# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from twisted.trial.unittest import TestCase

import os
from textwrap import dedent

from .._settings import load_config, ConfigError


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
"""
            )

        config = load_config(temp)
        self.assertEqual(config["package"], "foobar")
        self.assertEqual(config["package_dir"], ".")
        self.assertEqual(config["filename"], "NEWS.rst")
        self.assertEqual(config["underlines"], ["=", "-", "~"])

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
        self.assertEqual(config["package"], "a")

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
            )
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
