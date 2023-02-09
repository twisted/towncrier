# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from incremental import Version
from twisted.trial.unittest import TestCase

from towncrier._version import _hatchling_version


class TestPackaging(TestCase):
    def test_version_warning(self):
        """
        Import __version__ from towncrier returns an Incremental version object
        and raises a warning.
        """
        with self.assertWarnsRegex(
            DeprecationWarning, "Accessing towncrier.__version__ is deprecated.*"
        ):
            from towncrier import __version__

        self.assertIsInstance(__version__, Version)
        self.assertEqual(_hatchling_version, __version__.short())
