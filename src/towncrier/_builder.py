# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from __future__ import absolute_import, division

import os
import textwrap

from io import StringIO


def normalise(text):

    # Blitz newlines
    text = text.replace("\r\n", "\n")
    text = text.replace("\n", " ")

    # No tabs!
    text = text.replace("\t", " ")

    # Remove double spaces
    while "  " in text:
        text = text.replace("  ", " ")

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

            ticket = int(ticket)
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
    fragments = split_fragments(fragments, definitions)

    result = StringIO()

    for section in sorted(fragments.keys()):

        if section:
            result.write("\n" + section + "\n")
            result.write(major * len(section) + "\n\n")

        if not fragments[section]:
            result.write("No significant changes.\n\n")
            continue


        for category_name, category_info in definitions.items():

            desc = category_info[0]
            includes_text = category_info[1]

            if category_name not in fragments[section]:
                continue

            frags = fragments[section][category_name]

            result.write(desc + "\n")

            if not section:
                result.write(major * len(desc) + "\n\n")
            else:
                result.write(minor * len(desc) + "\n\n")

            if includes_text:

                for text, tickets in sorted(frags.items(), key=lambda i: i[1][0]):
                    tickets = ["#" + str(i) for i in tickets]
                    to_wrap = " - " + text + " (" + ", ".join(tickets) + ")"

                    result.write(textwrap.fill(to_wrap, subsequent_indent="   ") + "\n")

            else:

                all_tickets = []

                for text, tickets in sorted(frags.items(), key=lambda i: i[1][0]):
                    all_tickets = all_tickets + ["#" + str(i) for i in tickets]

                result.write("   " + textwrap.fill(
                    ", ".join(sorted(all_tickets)), subsequent_indent="   "))

            result.write("\n")

        result.write("\n")

    return result.getvalue().rstrip() + "\n"
