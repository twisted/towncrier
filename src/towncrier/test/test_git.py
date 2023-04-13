# Copyright (c) Amber Brown, 2015
# See LICENSE for details.


from twisted.trial.unittest import TestCase

from towncrier import _git


class TestGit(TestCase):
    def test_empty_remove(self):
        """
        If remove_files gets an empty list, it returns gracefully.
        """
        _git.remove_files([])
