# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from twisted.trial.unittest import TestCase

import tempfile
import os

from .._settings import load_config


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
        self.assertEqual(config['underlines'], ["=", "-", "~"])

    def test_can_load_custom_config(self):
        conf = """[tool.towncrier]
package = "custom"
"""
        config_file = tempfile.NamedTemporaryFile('w', delete=False)
        config_file.write(conf)
        config_file.close()
        config = load_config(config_file.name)
        self.assertEqual(config['package'], "custom")
