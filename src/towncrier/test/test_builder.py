# Copyright (c) Povilas Kanapickas, 2019
# See LICENSE for details.

from twisted.trial.unittest import TestCase

from .._builder import parse_newfragment_basename


class TestParseNewsfragmentBasename(TestCase):

    def test_simple(self):
        self.assertEqual(parse_newfragment_basename('123.feature'),
                         ('123', 'feature', 0))

    def test_counter(self):
        self.assertEqual(parse_newfragment_basename('123.feature.1'),
                         ('123', 'feature', 1))

    def test_ignores_extension(self):
        self.assertEqual(parse_newfragment_basename('123.feature.ext'),
                         ('123', 'feature', 0))

    def test_non_numeric_ticket(self):
        self.assertEqual(parse_newfragment_basename('baz.feature'),
                         ('baz', 'feature', 0))
