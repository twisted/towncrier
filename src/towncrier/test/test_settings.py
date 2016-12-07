# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from twisted.trial.unittest import TestCase

import os

from .._settings import load_config


class IniSettingsTests(TestCase):

    def test_base(self):
        """
        Test a "base config" -- with just a package name.
        """
        temp = self.mktemp()
        os.makedirs(temp)

        with open(os.path.join(temp, "towncrier.ini"), "w") as f:
            f.write("""[towncrier]
package = foobar
""")

        config = load_config(temp)
        self.assertEqual(config['package'], "foobar")
        self.assertEqual(config['package_dir'], ".")
        self.assertEqual(config['filename'], "NEWS.rst")


class TomlSettingsTests(TestCase):

    def test_base(self):
        """
        Test a "base config".
        """
        temp = self.mktemp()
        os.makedirs(temp)

        with open(os.path.join(temp, "pyproject.toml"), "w") as f:
            f.write("""[tool.towncrier]
package = "foobar"
""")

        config = load_config(temp)
        self.assertEqual(config['package'], "foobar")
        self.assertEqual(config['package_dir'], ".")
        self.assertEqual(config['filename'], "NEWS.rst")
