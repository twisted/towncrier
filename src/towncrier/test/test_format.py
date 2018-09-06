# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from __future__ import absolute_import, division

import pkg_resources

from twisted.trial.unittest import TestCase

from collections import OrderedDict

from .._builder import render_fragments, split_fragments


class FormatterTests(TestCase):
    def test_split(self):

        fragments = {
            "": {
                ("1", "misc", 0): u"",
                ("baz", "misc", 0): u"",
                ("2", "feature", 0): u"Foo added.",
                ("5", "feature", 0): u"Foo added.    \n",
                ("6", "bugfix", 0): u"Foo added.",
            },
            "Web": {
                ("3", "bugfix", 0): u"Web fixed.    ",
                ("4", "feature", 0): u"Foo added.",
            },
        }

        expected_output = {
            "": {
                "misc": {"": ["1", "baz"]},
                "feature": {u"Foo added.": ["2", "5"]},
                "bugfix": {u"Foo added.": ["6"]},
            },
            "Web": {
                "bugfix": {u"Web fixed.": ["3"]},
                "feature": {u"Foo added.": ["4"]},
            },
        }

        definitions = OrderedDict(
            [
                ("feature", {"name": "Features", "showcontent": True}),
                ("bugfix", {"name": "Bugfixes", "showcontent": True}),
                ("misc", {"name": "Misc", "showcontent": False}),
            ]
        )

        output = split_fragments(fragments, definitions)

        self.assertEqual(expected_output, output)

    def test_basic(self):
        """
        Basic functionality -- getting a bunch of news fragments and formatting
        them into a rST file -- works.
        """
        fragments = OrderedDict(
            [
                (
                    "",
                    {
                        # asciibetical sorting will do 1, 142, 9
                        # we want 1, 9, 142 instead
                        ("142", "misc", 0): u"",
                        ("1", "misc", 0): u"",
                        ("9", "misc", 0): u"",
                        ("bar", "misc", 0): u"",
                        ("4", "feature", 0): u"Stuff!",
                        ("2", "feature", 0): u"Foo added.",
                        ("72", "feature", 0): u"Foo added.",
                        ("9", "feature", 0): u"Foo added.",
                        ("baz", "feature", 0): u"Fun!",
                    },
                ),
                ("Names", {}),
                ("Web", {("3", "bugfix", 0): u"Web fixed."}),
            ]
        )

        definitions = OrderedDict(
            [
                ("feature", {"name": "Features", "showcontent": True}),
                ("bugfix", {"name": "Bugfixes", "showcontent": True}),
                ("misc", {"name": "Misc", "showcontent": False}),
            ]
        )

        expected_output = (
            u"""
Features
--------

- Fun! (baz)
- Foo added. (#2, #9, #72)
- Stuff! (#4)


Misc
----

- bar, #1, #9, #142


Names
-----

No significant changes.


Web
---

Bugfixes
~~~~~~~~

- Web fixed. (#3)
"""
        )

        template = pkg_resources.resource_string(
            "towncrier", "templates/template.rst"
        ).decode("utf8")

        fragments = split_fragments(fragments, definitions)
        output = render_fragments(
            template, None, fragments, definitions, ["-", "~"], wrap=True
        )
        self.assertEqual(output, expected_output)

        # Check again with non-default underlines
        expected_output_weird_underlines = (
            u"""
Features
********

- Fun! (baz)
- Foo added. (#2, #9, #72)
- Stuff! (#4)


Misc
****

- bar, #1, #9, #142


Names
*****

No significant changes.


Web
***

Bugfixes
^^^^^^^^

- Web fixed. (#3)
"""
        )

        output = render_fragments(
            template, None, fragments, definitions, ["*", "^"], wrap=True
        )
        self.assertEqual(output, expected_output_weird_underlines)

    def test_issue_format(self):
        """
        issue_format option can be used to format issue text.
        And sorting happens before formatting, so numerical issues are still
        ordered numerically even if that doesn't match asciibetical order on
        the final text.
        """
        fragments = {
            "": {
                # asciibetical sorting will do 1, 142, 9
                # we want 1, 9, 142 instead
                ("142", "misc", 0): u"",
                ("1", "misc", 0): u"",
                ("9", "misc", 0): u"",
                ("bar", "misc", 0): u"",
            }
        }

        definitions = OrderedDict([("misc", {"name": "Misc", "showcontent": False})])

        expected_output = (
            u"""
Misc
----

- xxbar, xx1, xx9, xx142
"""
        )

        template = pkg_resources.resource_string(
            "towncrier", "templates/template.rst"
        ).decode("utf8")

        fragments = split_fragments(fragments, definitions)
        output = render_fragments(
            template, u"xx{issue}", fragments, definitions, ["-", "~"], wrap=True
        )
        self.assertEqual(output, expected_output)

    def test_line_wrapping(self):
        """
        Output is nicely wrapped, but doesn't break up words (which can mess
        up URLs)
        """
        self.maxDiff = None

        fragments = {
            "": {
                (
                    "1",
                    "feature",
                    0,
                ): u"""
                asdf asdf asdf asdf looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong newsfragment.
                """,  # NOQA
                ("2", "feature", 0): u"https://google.com/q=?" + u"-" * 100,
                ("3", "feature", 0): u"a " * 80,
            }
        }

        definitions = OrderedDict(
            [("feature", {"name": "Features", "showcontent": True})]
        )

        expected_output = (
            u"""
Features
--------

- asdf asdf asdf asdf
  looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong
  newsfragment. (#1)
-
  https://google.com/q=?----------------------------------------------------------------------------------------------------
  (#2)
- a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a
  a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a
  a a (#3)
"""
        )

        template = pkg_resources.resource_string(
            "towncrier", "templates/template.rst"
        ).decode("utf8")

        fragments = split_fragments(fragments, definitions)
        output = render_fragments(
            template, None, fragments, definitions, ["-", "~"], wrap=True
        )
        self.assertEqual(output, expected_output)

    def test_line_wrapping_disabled(self):
        """
        Output is not wrapped if it's disabled.
        """
        self.maxDiff = None

        fragments = {
            "": {
                (
                    "1",
                    "feature",
                    0
                ): u"""
                asdf asdf asdf asdf looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong newsfragment.
                """,  # NOQA
                ("2", "feature", 0): u"https://google.com/q=?" + u"-" * 100,
                ("3", "feature", 0): u"a " * 80,
            }
        }

        definitions = OrderedDict(
            [("feature", {"name": "Features", "showcontent": True})]
        )

        expected_output = (
            u"""
Features
--------

- asdf asdf asdf asdf looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong newsfragment. (#1)
- https://google.com/q=?---------------------------------------------------------------------------------------------------- (#2)
- a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a (#3)
"""  # NOQA
        )

        template = pkg_resources.resource_string(
            "towncrier", "templates/template.rst"
        ).decode("utf8")

        fragments = split_fragments(fragments, definitions)
        output = render_fragments(
            template, None, fragments, definitions, ["-", "~"], wrap=False
        )
        self.assertEqual(output, expected_output)
