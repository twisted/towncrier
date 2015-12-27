# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from twisted.trial.unittest import TestCase

import os

from collections import OrderedDict

from .._builder import render_fragments, split_fragments
from .._writer import append_to_newsfile

class WritingTests(TestCase):

    def test_append_at_top(self):

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

        expected_output = """MyProject 1.0
=============

Features
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


Old text.
"""

        tempdir = self.mktemp()
        os.mkdir(tempdir)

        with open(os.path.join(tempdir, "NEWS.rst"), "w") as f:
            f.write("Old text.\n")

        fragments = split_fragments(fragments, definitions)

        append_to_newsfile(tempdir,
                           "NEWS.rst",
                           "MyProject 1.0",
                           render_fragments(fragments, definitions))



        with open(os.path.join(tempdir, "NEWS.rst"), "r") as f:
            output = f.read()

        self.assertEqual(expected_output, output)
