# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from __future__ import absolute_import, division

import os
import textwrap

from io import StringIO


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


def find_fragments(base_directory, sections):
    """
    Sections are a dictonary of section names to paths.
    """
    content = {}

    for key, val in sections.items():

        section_dir = os.path.join(base_directory, val, "newsfragments")
        files = os.listdir(section_dir)

        file_content = {}

        for fragment in files:
            with open(os.path.join(section_dir, fragment), "rb") as f:
                file_content[fragment] = f.read().decode('utf8')

        content[key] = file_content

    return content


def split_fragments(fragments, definitions):

    output = {}

    for section_name, section_fragments in fragments.items():
        section = {}

        for filename, content in section_fragments.items():

            content = normalise(content)
            parts = filename.split(".")

            if len(parts) == 1:
                continue
            else:
                ticket, category = parts

            if category not in definitions:
                continue

            texts = section.get(category, {})

            if texts.get(content):
                texts[content] = sorted(texts[content] + [ticket])
            else:
                texts[content] = [ticket]

            section[category] = texts

        output[section_name] = section

    return output


def render_fragments(fragments, definitions, major=u"-", minor=u"~"):
    """
    Render the fragments into a news file.
    """
    result = StringIO()

    for section in sorted(fragments.keys()):

        if section:
            result.write(u"\n" + section + u"\n")
            result.write(major * len(section) + u"\n\n")

        if not fragments[section]:
            result.write(u"No significant changes.\n\n")
            continue

        for category_name, category_info in definitions.items():

            desc = category_info[0]
            includes_text = category_info[1]

            if category_name not in fragments[section]:
                continue

            frags = fragments[section][category_name]

            result.write(desc + u"\n")

            if not section:
                result.write(major * len(desc) + u"\n\n")
            else:
                result.write(minor * len(desc) + u"\n\n")

            if includes_text:

                for text, tickets in sorted(frags.items(),
                                            key=lambda i: i[1][0]):
                    all_tickets = []

                    for i in tickets:
                        try:
                            int(i)
                            all_tickets.append(u"#" + i)
                        except:
                            all_tickets.append(i)

                    to_wrap = (u"- " + text + u" (" +
                               u", ".join(all_tickets) + u")")

                    result.write(
                        textwrap.fill(to_wrap,
                                      subsequent_indent=u"  ") + u"\n")
            else:

                all_tickets = []

                for text, tickets in sorted(frags.items(),
                                            key=lambda i: i[1][0]):

                    for i in tickets:
                        try:
                            int(i)
                            all_tickets.append(u"#" + i)
                        except:
                            all_tickets.append(i)

                result.write(u"- " + textwrap.fill(
                    u", ".join(sorted(all_tickets)), subsequent_indent=u"  "))

            result.write(u"\n")

        result.write(u"\n")

    return result.getvalue().rstrip() + u"\n"
