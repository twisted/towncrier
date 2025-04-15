from twisted.trial.unittest import TestCase

from towncrier import _novcs


class TestNOVCS(TestCase):
    def test_get_default_compare_branch(self):
        self.assertEqual(None, _novcs.get_default_compare_branch([]))

    def test_empty_remove(self):
        """
        If remove_files gets an empty list, it returns gracefully.
        """
        _novcs.remove_files([])

    def test_get_remote_branches(self):
        self.assertEqual([], _novcs.get_remote_branches("."))

    def test_list_changed_files_compared_to_branch(self):
        self.assertEqual(
            [], _novcs.list_changed_files_compared_to_branch(".", "main", False)
        )
