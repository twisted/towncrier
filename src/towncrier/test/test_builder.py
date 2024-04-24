# Copyright (c) Povilas Kanapickas, 2019
# See LICENSE for details.

from twisted.trial.unittest import TestCase

from .._builder import parse_newfragment_basename


class TestParseNewsfragmentBasename(TestCase):
    def test_simple(self):
        """<number>.<category> generates a counter value of 0."""
        self.assertEqual(
            parse_newfragment_basename("123.feature", ["feature"]),
            ("123", "feature", 0),
        )

    def test_invalid_category(self):
        """Files without a valid category are rejected."""
        self.assertEqual(
            parse_newfragment_basename("README.ext", ["feature"]),
            (None, None, None),
        )

    def test_counter(self):
        """<number>.<category>.<counter> generates a custom counter value."""
        self.assertEqual(
            parse_newfragment_basename("123.feature.1", ["feature"]),
            ("123", "feature", 1),
        )

    def test_counter_with_extension(self):
        """File extensions are ignored."""
        self.assertEqual(
            parse_newfragment_basename("123.feature.1.ext", ["feature"]),
            ("123", "feature", 1),
        )

    def test_ignores_extension(self):
        """File extensions are ignored."""
        self.assertEqual(
            parse_newfragment_basename("123.feature.ext", ["feature"]),
            ("123", "feature", 0),
        )

    def test_non_numeric_ticket(self):
        """Non-numeric issue identifiers are preserved verbatim."""
        self.assertEqual(
            parse_newfragment_basename("baz.feature", ["feature"]),
            ("baz", "feature", 0),
        )

    def test_non_numeric_ticket_with_extension(self):
        """File extensions are ignored."""
        self.assertEqual(
            parse_newfragment_basename("baz.feature.ext", ["feature"]),
            ("baz", "feature", 0),
        )

    def test_dots_in_ticket_name(self):
        """Non-numeric issue identifiers are preserved verbatim."""
        self.assertEqual(
            parse_newfragment_basename("baz.1.2.feature", ["feature"]),
            ("baz.1.2", "feature", 0),
        )

    def test_dots_in_ticket_name_invalid_category(self):
        """Files without a valid category are rejected."""
        self.assertEqual(
            parse_newfragment_basename("baz.1.2.notfeature", ["feature"]),
            (None, None, None),
        )

    def test_dots_in_ticket_name_and_counter(self):
        """Non-numeric issue identifiers are preserved verbatim."""
        self.assertEqual(
            parse_newfragment_basename("baz.1.2.feature.3", ["feature"]),
            ("baz.1.2", "feature", 3),
        )

    def test_strip(self):
        """Leading spaces and subsequent leading zeros are stripped
        when parsing newsfragment names into ticket numbers etc.
        """
        self.assertEqual(
            parse_newfragment_basename("  007.feature", ["feature"]),
            ("7", "feature", 0),
        )

    def test_strip_with_counter(self):
        """Leading spaces and subsequent leading zeros are stripped
        when parsing newsfragment names into ticket numbers etc.
        """
        self.assertEqual(
            parse_newfragment_basename("  007.feature.3", ["feature"]),
            ("7", "feature", 3),
        )

    def test_orphan(self):
        """Orphaned snippets must remain the orphan marker in the issue
        identifier."""
        self.assertEqual(
            parse_newfragment_basename("+orphan.feature", ["feature"]),
            ("+orphan", "feature", 0),
        )

    def test_orphan_with_number(self):
        """Orphaned snippets can contain numbers in the identifier."""
        self.assertEqual(
            parse_newfragment_basename("+123_orphan.feature", ["feature"]),
            ("+123_orphan", "feature", 0),
        )
        self.assertEqual(
            parse_newfragment_basename("+orphan_123.feature", ["feature"]),
            ("+orphan_123", "feature", 0),
        )

    def test_orphan_with_dotted_number(self):
        """Orphaned snippets can contain numbers with dots in the
        identifier."""
        self.assertEqual(
            parse_newfragment_basename("+12.3_orphan.feature", ["feature"]),
            ("+12.3_orphan", "feature", 0),
        )
        self.assertEqual(
            parse_newfragment_basename("+orphan_12.3.feature", ["feature"]),
            ("+orphan_12.3", "feature", 0),
        )
