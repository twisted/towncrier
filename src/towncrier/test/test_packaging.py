# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from twisted.trial.unittest import TestCase

import towncrier


class TestPackaging(TestCase):
    def no_version_attr(self):
        """
        towncrier.__version__ was deprecated, now no longer exists.
        """

        with self.assertRaises(AttributeError):
            towncrier.__version__
