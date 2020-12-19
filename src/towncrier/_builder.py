# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from __future__ import absolute_import, division, print_function

import os
import sys
import textwrap
import traceback

from collections import OrderedDict

from jinja2 import Template

from ._settings import ConfigError


def strip_if_integer_string(s):
    try:
        i = int(s)
    except ValueError:
        return s

    return str(i)


# Returns ticket, category and counter or (None, None, None) if the basename
# could not be parsed or doesn't contain a valid category.
def parse_newfragment_basename(basename, definitions):
    invalid = (None, None, None)
    parts = basename.split(".")

    if len(parts) == 1:
        return invalid
    if len(parts) == 2:
        ticket, category = parts
        ticket = strip_if_integer_string(ticket)
        return (ticket, category, 0) if category in definitions else invalid

    # There are at least 3 parts. Search for a valid category from the second
    # part onwards.
    # The category is used as the reference point in the parts list to later
    # infer the issue number and counter value.
    for i in range(1, len(parts)):
        if parts[i] in definitions:
            # Current part is a valid category according to given definitions.
            category = parts[i]
            # Use the previous part as the ticket number.
            # NOTE: This allows news fragment names like fix-1.2.3.feature or
            # something-cool.feature.ext for projects that don't use ticket
            # numbers in news fragment names.
            ticket = strip_if_integer_string(parts[i-1])
            counter = 0
            # Use the following part as the counter if it exists and is a valid
            # digit.
            if len(parts) > (i + 1) and parts[i+1].isdigit():
                counter = int(parts[i+1])
            return ticket, category, counter
    else:
        # No valid category found.
        return invalid


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

        if sys.version_info >= (3,):
            expected_exception = FileNotFoundError
        else:
            expected_exception = OSError

        try:
            files = os.listdir(section_dir)
        except expected_exception as e:
            message = "Failed to list the news fragment files.\n{}".format(
                ''.join(traceback.format_exception_only(type(e), e)),
            )
            raise ConfigError(message)

        file_content = {}

        for basename in files:

            ticket, category, counter = parse_newfragment_basename(
                basename, definitions
            )
            if category is None:
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
def split_fragments(fragments, definitions, all_bullets=True):

    output = OrderedDict()

    for section_name, section_fragments in fragments.items():
        section = {}

        for (ticket, category, counter), content in section_fragments.items():

            if all_bullets:
                # By default all fragmetns are append by "-" automatically,
                # and need to be indented because of that.
                # (otherwise, assume they are formatted correctly)
                content = indent(content.strip(), u"  ")[2:]
            else:
                # Assume the text is formatted correctly
                content = content.rstrip()

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


def bullet_key(entry):
    text, _ = entry
    if not text:
        return -1
    if text[:2] == u"- ":
        return 0
    elif text[:2] == "* ":
        return 1
    elif text[:3] == u"#. ":
        return 2
    return 3


def render_issue(issue_format, issue):
    if issue_format is None:
        try:
            int(issue)
            return u"#" + issue
        except Exception:
            return issue
    else:
        return issue_format.format(issue=issue)


def render_fragments(
    template,
    issue_format,
    top_line,
    fragments,
    definitions,
    underlines,
    wrap,
    versiondata,
    top_underline="=",
    all_bullets=False,
):
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
            if not all_bullets:
                entries.sort(key=bullet_key)

            # Then we put these nicely sorted entries back in an ordered dict
            # for the template, after formatting each issue number
            categories = OrderedDict()
            for text, issues in entries:
                rendered = [render_issue(issue_format, i) for i in issues]
                categories[text] = rendered

            data[section_name][category_name] = categories

    done = []

    def get_indent(text):
        # If bullets are not assumed and we wrap, the subsequent
        # indentation depends on whether or not this is a bullet point.
        # (it is probably usually best to disable wrapping in that case)
        if all_bullets or text[:2] == u"- " or text[:2] == u"* ":
            return u"  "
        elif text[:3] == "#. ":
            return u"   "
        return u""

    res = jinja_template.render(
        top_line=top_line,
        sections=data,
        definitions=definitions,
        underlines=underlines,
        versiondata=versiondata,
        top_underline=top_underline,
        get_indent=get_indent,  # simplify indentation in the jinja template.
    )

    for line in res.split(u"\n"):
        if wrap:
            done.append(
                textwrap.fill(
                    line,
                    width=79,
                    subsequent_indent=get_indent(line),
                    break_long_words=False,
                    break_on_hyphens=False,
                )
            )
        else:
            done.append(line)

    return u"\n".join(done).rstrip() + u"\n"
