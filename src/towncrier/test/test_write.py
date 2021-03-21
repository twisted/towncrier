# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from twisted.trial.unittest import TestCase

import pkg_resources
import os
from textwrap import dedent

from collections import OrderedDict

from .._builder import render_fragments, split_fragments
from .._writer import append_to_newsfile


class WritingTests(TestCase):
    def test_append_at_top(self):

        fragments = OrderedDict(
            [
                (
                    "",
                    OrderedDict(
                        [
                            (("142", "misc", 0), u""),
                            (("1", "misc", 0), u""),
                            (("4", "feature", 0), u"Stuff!"),
                            (("4", "feature", 1), u"Second Stuff!"),
                            (("2", "feature", 0), u"Foo added."),
                            (("72", "feature", 0), u"Foo added."),
                        ]
                    ),
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

        expected_output = """MyProject 1.0 (never)
=====================

Features
--------

- Foo added. (#2, #72)
- Stuff! (#4)
- Second Stuff! (#4)


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
            "towncrier", "templates/default.rst"
        ).decode("utf8")

        append_to_newsfile(
            tempdir,
            "NEWS.rst",
            ".. towncrier release notes start\n",
            "",
            render_fragments(
                template,
                None,
                "",
                fragments,
                definitions,
                ["-", "~"],
                wrap=True,
                versiondata={"name": "MyProject", "version": "1.0", "date": "never"},
            ),
        )

        with open(os.path.join(tempdir, "NEWS.rst"), "r") as f:
            output = f.read()

        self.assertEqual(expected_output, output)

    def test_append_at_top_with_hint(self):
        """
        If there is a comment with C{.. towncrier release notes start},
        towncrier will add the version notes after it.
        """
        fragments = OrderedDict(
            [
                (
                    "",
                    {
                        ("142", "misc", 0): u"",
                        ("1", "misc", 0): u"",
                        ("4", "feature", 0): u"Stuff!",
                        ("2", "feature", 0): u"Foo added.",
                        ("72", "feature", 0): u"Foo added.",
                        ("99", "feature", 0): u"Foo! " * 100,
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

        expected_output = """Hello there! Here is some info.

.. towncrier release notes start

MyProject 1.0 (never)
=====================

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
            f.write(
                (
                    "Hello there! Here is some info.\n\n"
                    ".. towncrier release notes start\nOld text.\n"
                )
            )

        fragments = split_fragments(fragments, definitions)

        template = pkg_resources.resource_string(
            "towncrier", "templates/default.rst"
        ).decode("utf8")

        append_to_newsfile(
            tempdir,
            "NEWS.rst",
            ".. towncrier release notes start\n",
            "",
            render_fragments(
                template,
                None,
                "",
                fragments,
                definitions,
                ["-", "~"],
                wrap=True,
                versiondata={"name": "MyProject", "version": "1.0", "date": "never"},
            ),
        )

        with open(os.path.join(tempdir, "NEWS.rst"), "r") as f:
            output = f.read()

        self.assertEqual(expected_output, output)

    def test_multiple_file_no_start_string(self):
        """
        When no `start_string` is defined, the generated content is added at
        the start of the file.
        """
        tempdir = self.mktemp()
        os.mkdir(tempdir)

        definitions = {}
        fragments = split_fragments(fragments={}, definitions=definitions)

        template = pkg_resources.resource_string(
            "towncrier", "templates/default.rst"
        ).decode("utf8")

        content = render_fragments(
            template=template,
            issue_format=None,
            top_line="",
            fragments=fragments,
            definitions=definitions,
            underlines=["-", "~"],
            wrap=True,
            versiondata={"name": "MyProject", "version": "1.0", "date": "never"},
        )

        append_to_newsfile(
            directory=tempdir,
            filename="NEWS.rst",
            start_string=None,
            top_line="",
            content=content,
        )

        with open(os.path.join(tempdir, "NEWS.rst"), "r") as f:
            output = f.read()

        expected_output = dedent("""\
            MyProject 1.0 (never)
            =====================
        """)

        self.assertEqual(expected_output, output)
