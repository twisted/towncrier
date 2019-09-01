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
                blah=baz
                """
                )
            )

        with self.assertRaises(ConfigError) as e:
            config = load_config(temp)

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
            config = load_config(temp)

        self.assertEqual(e.exception.failing_option, "single_file")

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
            config = load_config(temp)

        self.assertEqual(e.exception.failing_option, "singlefile")
