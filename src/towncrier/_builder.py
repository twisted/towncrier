# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from __future__ import absolute_import, division, print_function

import os
import textwrap

from collections import OrderedDict

from jinja2 import Template


def normalise(text):

    # Blitz newlines
    text = text.replace(u"\r\n", u"\n")
    text = text.replace(u"\n", u" ")

    # No tabs!
    text = text.replace(u"\t", u" ")

    # Remove double spaces
    while u"  " in text:
        text = text.replace(u"  ", u" ")

    # Remove left/right whitespace
    text = text.strip()

    return text


def find_fragments(base_directory, sections, fragment_directory):
    """
    Sections are a dictonary of section names to paths.
    """
    content = {}

    for key, val in sections.items():

        if fragment_directory is not None:
            section_dir = os.path.join(base_directory, val, fragment_directory)
        else:
            section_dir = os.path.join(base_directory, val)

        files = os.listdir(section_dir)

        file_content = {}

        for fragment in files:
            with open(os.path.join(section_dir, fragment), "rb") as f:
                file_content[fragment] = f.read().decode('utf8', 'replace')

        content[key] = file_content

    return content


def split_fragments(fragments, definitions):

    output = {}

    for section_name, section_fragments in fragments.items():
        section = {}

        for filename, content in section_fragments.items():

            content = normalise(content)
            parts = filename.split(u".")

            if len(parts) == 1:
                continue
            else:
                ticket, category = parts

            if category not in definitions:
                continue

            if definitions[category]["showcontent"] is False:
                content = u""

            texts = section.get(category, {})

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


def render_fragments(
        template, issue_format, fragments, definitions, major=u"-", minor=u"~"
):
    """
    Render the fragments into a news file.
    """

    jinja_template = Template(template, trim_blocks=True)

    data = {}

    for section_name, section_value in fragments.items():

        data[section_name] = {}

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

    res = jinja_template.render(sections=data, definitions=definitions)

    for line in res.split(u"\n"):
        done.append(textwrap.fill(line, width=79, subsequent_indent=u"  "))

    return u"\n".join(done).rstrip() + u"\n"
