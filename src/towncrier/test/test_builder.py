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

    def test_invalid_category(self):
        self.assertEqual(
            parse_newfragment_basename("README.ext", ["feature"]),
            (None, None, None),
        )

    def test_counter(self):
        self.assertEqual(
            parse_newfragment_basename("123.feature.1", ["feature"]),
            ("123", "feature", 1),
        )

    def test_counter_with_extension(self):
        self.assertEqual(
            parse_newfragment_basename("123.feature.1.ext", ["feature"]),
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

    def test_non_numeric_ticket_with_extension(self):
        self.assertEqual(
            parse_newfragment_basename("baz.feature.ext", ["feature"]),
            ("baz", "feature", 0),
        )

    def test_dots_in_ticket_name(self):
        self.assertEqual(
            parse_newfragment_basename("baz.1.2.feature", ["feature"]),
            ("2", "feature", 0),
        )

    def test_dots_in_ticket_name_invalid_category(self):
        self.assertEqual(
            parse_newfragment_basename("baz.1.2.notfeature", ["feature"]),
            (None, None, None),
        )

    def test_dots_in_ticket_name_and_counter(self):
        self.assertEqual(
            parse_newfragment_basename("baz.1.2.feature.3", ["feature"]),
            ("2", "feature", 3),
        )

    def test_strip(self):
        """Leading spaces and subsequent leading zeros are stripped
        when parsing newsfragment names into ticket numbers etc.
        """
        self.assertEqual(
            parse_newfragment_basename("  007.feature", ["feature"]),
            ("7", "feature", 0)
        )

    def test_strip_with_counter(self):
        self.assertEqual(
            parse_newfragment_basename("  007.feature.3", ["feature"]),
            ("7", "feature", 3)
        )
