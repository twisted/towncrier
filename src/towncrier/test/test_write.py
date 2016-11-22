# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from twisted.trial.unittest import TestCase

import pkg_resources
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
            ("feature", {"name": "Features", "showcontent": True}),
            ("bugfix", {"name": "Bugfixes", "showcontent": True}),
            ("misc", {"name": "Misc", "showcontent": False}),
        ])

        expected_output = """MyProject 1.0
=============

Features
--------

- Foo added. (#2, #72)
- Stuff! (#4)

Misc
----

- #1, #142


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

        template = pkg_resources.resource_string(
            "towncrier",
            "templates/template.rst").decode('utf8')

        append_to_newsfile(tempdir,
                           "NEWS.rst",
                           ".. towncrier release notes start\n",
                           "MyProject 1.0\n=============\n",
                           render_fragments(template, fragments, definitions))

        with open(os.path.join(tempdir, "NEWS.rst"), "r") as f:
            output = f.read()

        self.assertEqual(expected_output, output)

    def test_append_at_top_with_hint(self):
        """
        If there is a comment with C{.. towncrier release notes start},
        towncrier will add the version notes after it.
        """
        fragments = {
            "": {
                "142.misc": u"",
                "1.misc": u"",
                "4.feature": u"Stuff!",
                "2.feature": u"Foo added.",
                "72.feature": u"Foo added.",
                "99.feature": u"Foo! " * 100
            },
            "Web": {
                "3.bugfix": u"Web fixed.",
            },
            "Names": {}
        }

        definitions = OrderedDict([
            ("feature", {"name": "Features", "showcontent": True}),
            ("bugfix", {"name": "Bugfixes", "showcontent": True}),
            ("misc", {"name": "Misc", "showcontent": False}),
        ])

        expected_output = """Hello there! Here is some info.

.. towncrier release notes start

MyProject 1.0
=============

Features
--------

- Foo added. (#2, #72)
- Stuff! (#4)
- Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo!
  Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo!
  Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo!
  Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo!
  Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo!
  Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo!
  Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! Foo! (#99)

Misc
----

- #1, #142


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
            f.write(("Hello there! Here is some info.\n\n"
                     ".. towncrier release notes start\nOld text.\n"))

        fragments = split_fragments(fragments, definitions)

        template = pkg_resources.resource_string(
            "towncrier",
            "templates/template.rst").decode('utf8')

        append_to_newsfile(tempdir,
                           "NEWS.rst",
                           ".. towncrier release notes start\n",
                           "MyProject 1.0\n=============\n",
                           render_fragments(template, fragments, definitions))

        with open(os.path.join(tempdir, "NEWS.rst"), "r") as f:
            output = f.read()

        self.assertEqual(expected_output, output)
