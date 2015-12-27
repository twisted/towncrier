# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from twisted.trial.unittest import TestCase

from collections import OrderedDict

from .._builder import render_fragments, split_fragments, normalise

class FormatterTests(TestCase):

    def test_normalise(self):

        cases = [
            ("   hello", "hello"),
            ("\thello\nthere\n people", "hello there people"),
            ("hi\nthere        what's up\n\n\n", "hi there what's up"),
        ]

        for case in cases:
            self.assertEqual(normalise(case[0]), case[1])


    def test_split(self):

        fragments = {
            "": {
                "1.misc": u"",
                "2.feature": u"Foo added.",
                "421.feature~": u"Foo added.",
                "5.feature": u"Foo added.    \n",
                "6.bugfix": u"Foo added.",
                "NEWS": u"Some junk.",
            },
            "Web": {
                "3.bugfix": u"Web fixed.    ",
                "4.feature": u"Foo added."
            }
        }

        expected_output = {
            "": {
                "misc": {
                    '': [1],
                },
                "feature": {
                    u"Foo added.": [2, 5]
                },
                "bugfix": {
                    u"Foo added.": [6]
                }
            },
            "Web": {
                "bugfix": {
                    u"Web fixed.": [3],
                },
                "feature": {
                    u"Foo added.": [4]
                }
            }

        }

        definitions = OrderedDict([
            ("feature", ("Features", True)),
            ("bugfix", ("Bugfixes", True)),
            ("misc", ("Misc", False)),
        ])

        output = split_fragments(fragments, definitions)

        self.assertEqual(expected_output, output)


    def test_basic(self):
        """
        Basic functionality -- getting a bunch of news fragments and formatting
        them into a rST file -- works.
        """
        fragments = {
            "": {
                "142.misc": u"",
                "1.misc": u"",
                "4.feature": u"Stuff!",
                "2.feature": u"Foo added.",
                "72.feature": u"Foo added.",
            },
            "Web": {
                "3.bugfix": u"Web fixed.",
            },
            "Names": {}
        }

        definitions = OrderedDict([
            ("feature", ("Features", True)),
            ("bugfix", ("Bugfixes", True)),
            ("misc", ("Misc", False)),
        ])

        expected_output = (
u"""Features
--------

 - Foo added. (#2, #72)
 - Stuff! (#4)

Misc
----

   #1, #142


Names
-----

No significant changes.


Web
---

Bugfixes
~~~~~~~~

 - Web fixed. (#3)
""")

        fragments = split_fragments(fragments, definitions)
        output = render_fragments(fragments, definitions)
        self.assertEqual(output, expected_output)
