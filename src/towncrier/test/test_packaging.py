# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from twisted.trial.unittest import TestCase

import towncrier


class TestPackaging(TestCase):
    def test_version_attr(self):
        """
        towncrier.__version__ was deprecated, but still exists for now.
        """

        def access__version():
            return towncrier.__version__

        expected_warning = (
            "Accessing towncrier.__version__ is deprecated and will be "
            "removed in a future release. Use importlib.metadata directly "
            "to query for towncrier's packaging metadata."
        )

        self.assertWarns(
            DeprecationWarning, expected_warning, __file__, access__version
        )
