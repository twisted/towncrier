# Copyright (c) Povilas Kanapickas, 2019
# See LICENSE for details.

from twisted.trial.unittest import TestCase

from .._builder import parse_newfragment_basename


class TestParseNewsfragmentBasename(TestCase):
    def test_simple(self):
        self.assertEqual(
            parse_newfragment_basename("123.feature", ["feature"]),
            ("123", "feature", 0),
        )

    def test_counter(self):
        self.assertEqual(
            parse_newfragment_basename("123.feature.1", ["feature"]),
            ("123", "feature", 1),
        )

    def test_ignores_extension(self):
        self.assertEqual(
            parse_newfragment_basename("123.feature.ext", ["feature"]),
            ("123", "feature", 0),
        )

    def test_non_numeric_ticket(self):
        self.assertEqual(
            parse_newfragment_basename("baz.feature", ["feature"]),
            ("baz", "feature", 0),
        )

    def test_dots_in_ticket_name(self):
        self.assertEqual(
            parse_newfragment_basename("baz.1.2.feature", ["feature"]),
            ("2", "feature", 0),
        )

    def test_dots_in_ticket_name_unknown_category(self):
        self.assertEqual(
            parse_newfragment_basename("baz.1.2.notfeature", ["feature"]), ("1", "2", 0)
        )

    def test_dots_in_ticket_name_and_counter(self):
        self.assertEqual(
            parse_newfragment_basename("baz.1.2.feature.3", ["feature"]),
            ("2", "feature", 3),
        )
