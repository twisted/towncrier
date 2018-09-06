# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from __future__ import absolute_import, division, print_function

import os
import textwrap

from collections import OrderedDict

from jinja2 import Template


# Returns a structure like:
#
# OrderedDict([
#   ("",
#    {
#      ("142", "misc"): u"",
#      ("1", "feature"): u"some cool description",
#    }),
#   ("Names", {}),
#   ("Web", {("3", "bugfix"): u"Fixed a thing"}),
# ])
#
# We should really use attrs.
#
# Also returns a list of the paths that the fragments were taken from.
def find_fragments(base_directory, sections, fragment_directory, definitions):
    """
    Sections are a dictonary of section names to paths.
    """
    content = OrderedDict()
    fragment_filenames = []

    for key, val in sections.items():

        if fragment_directory is not None:
            section_dir = os.path.join(base_directory, val, fragment_directory)
        else:
            section_dir = os.path.join(base_directory, val)

        files = os.listdir(section_dir)

        file_content = {}

        for basename in files:
            parts = basename.split(u".")

            counter = 0
            if len(parts) == 1:
                continue
            else:
                ticket, category = parts[:2]

            # If there is a number after the category then use it as a counter,
            # otherwise ignore it.
            # This means 1.feature.1 and 1.feature do not conflict but
            # 1.feature.rst and 1.feature do.
            if len(parts) > 2:
                try:
                    counter = int(parts[2])
                except ValueError:
                    pass

            if category not in definitions:
                continue

            full_filename = os.path.join(section_dir, basename)
            fragment_filenames.append(full_filename)
            with open(full_filename, "rb") as f:
                data = f.read().decode("utf8", "replace")

            if (ticket, category, counter) in file_content:
                raise ValueError(
                    "multiple files for {}.{} in {}".format(
                        ticket, category, section_dir
                    )
                )
            file_content[ticket, category, counter] = data

        content[key] = file_content

    return content, fragment_filenames


def indent(text, prefix):
    """
    Adds `prefix` to the beginning of non-empty lines in `text`.
    """
    # Based on Python 3's textwrap.indent
    def prefixed_lines():
        for line in text.splitlines(True):
            yield (prefix + line if line.strip() else line)
    return u"".join(prefixed_lines())


# Takes the output from find_fragments above. Probably it would be useful to
# add an example output here. Next time someone digs deep enough to figure it
# out, please do so...
def split_fragments(fragments, definitions):

    output = OrderedDict()

    for section_name, section_fragments in fragments.items():
        section = {}

        for (ticket, category, counter), content in section_fragments.items():

            content = indent(content.strip(), u"  ")[2:]

            if definitions[category]["showcontent"] is False:
                content = u""

            texts = section.get(category, OrderedDict())

            if texts.get(content):
                texts[content] = sorted(texts[content] + [ticket])
            else:
                texts[content] = [ticket]

            section[category] = texts

        output[section_name] = section

    return output


def issue_key(issue):
    # We want integer issues to sort as integers, and we also want string
    # issues to sort as strings. We arbitrarily put string issues before
    # integer issues (hopefully no-one uses both at once).
    try:
        return (int(issue), u"")
    except Exception:
        # Maybe we should sniff strings like "gh-10" -> (10, "gh-10")?
        return (-1, issue)


def entry_key(entry):
    _, issues = entry
    return [issue_key(issue) for issue in issues]


def render_issue(issue_format, issue):
    if issue_format is None:
        try:
            int(issue)
            return u"#" + issue
        except Exception:
            return issue
    else:
        return issue_format.format(issue=issue)


def render_fragments(template, issue_format, fragments, definitions, underlines, wrap):
    """
    Render the fragments into a news file.
    """

    jinja_template = Template(template, trim_blocks=True)

    data = OrderedDict()

    for section_name, section_value in fragments.items():

        data[section_name] = OrderedDict()

        for category_name, category_value in section_value.items():
            # Suppose we start with an ordering like this:
            #
            # - Fix the thing (#7, #123, #2)
            # - Fix the other thing (#1)

            # First we sort the issues inside each line:
            #
            # - Fix the thing (#2, #7, #123)
            # - Fix the other thing (#1)
            entries = []
            for text, issues in category_value.items():
                entries.append((text, sorted(issues, key=issue_key)))

            # Then we sort the lines:
            #
            # - Fix the other thing (#1)
            # - Fix the thing (#2, #7, #123)
            entries.sort(key=entry_key)

            # Then we put these nicely sorted entries back in an ordered dict
            # for the template, after formatting each issue number
            categories = OrderedDict()
            for text, issues in entries:
                rendered = [render_issue(issue_format, i) for i in issues]
                categories[text] = rendered

            data[section_name][category_name] = categories

    done = []

    res = jinja_template.render(
        sections=data, definitions=definitions, underlines=underlines
    )

    for line in res.split(u"\n"):
        if wrap:
            done.append(
                textwrap.fill(
                    line,
                    width=79,
                    subsequent_indent=u"  ",
                    break_long_words=False,
                    break_on_hyphens=False,
                )
            )
        else:
            done.append(line)

    return u"\n".join(done).rstrip() + u"\n"
