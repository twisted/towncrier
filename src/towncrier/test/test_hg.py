# Copyright (c) Amber Brown, 2015
# See LICENSE for details.


from twisted.trial.unittest import TestCase

from towncrier import _hg


class TestHg(TestCase):
    def test_empty_remove(self):
        """
        If remove_files gets an empty list, it returns gracefully.
        """
        _hg.remove_files([])
