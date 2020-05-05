# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

import os
import sys
from subprocess import check_output

from twisted.trial.unittest import TestCase

from .._project import get_version


class VersionFetchingTests(TestCase):
    def test_str(self):
        """
        A str __version__ will be picked up.
        """
        temp = self.mktemp()
        os.makedirs(temp)
        os.makedirs(os.path.join(temp, "mytestproj"))

        with open(os.path.join(temp, "mytestproj", "__init__.py"), "w") as f:
            f.write("__version__ = '1.2.3'")

        version = get_version(temp, "mytestproj")
        self.assertEqual(version, "1.2.3")

    def test_tuple(self):
        """
        A tuple __version__ will be picked up.
        """
        temp = self.mktemp()
        os.makedirs(temp)
        os.makedirs(os.path.join(temp, "mytestproja"))

        with open(os.path.join(temp, "mytestproja", "__init__.py"), "w") as f:
            f.write("__version__ = (1, 3, 12)")

        version = get_version(temp, "mytestproja")
        self.assertEqual(version, "1.3.12")


class InvocationTests(TestCase):
    def test_dash_m(self):
        """
        `python -m towncrier` invokes the main entrypoint.
        """
        temp = self.mktemp()
        new_dir = os.path.join(temp, "dashm")
        os.makedirs(new_dir)
        orig_dir = os.getcwd()
        try:
            os.chdir(new_dir)
            with open("pyproject.toml", "w") as f:
                f.write('[tool.towncrier]\n' 'directory = "news"\n')
            os.makedirs("news")
            out = check_output([sys.executable, "-m", "towncrier", "--help"])
            self.assertIn(b"[OPTIONS] COMMAND [ARGS]...", out)
            self.assertIn(b"--help  Show this message and exit.", out)
        finally:
            os.chdir(orig_dir)
