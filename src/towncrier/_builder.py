# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from __future__ import absolute_import, division

import os


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


def split_fragments(fragments):

    output = {}

    for section_name, section_fragments in fragments.items():
        section = {}

        for filename, content in section_fragments.items():

            content = normalise(content)

            ticket, category = filename.split(".")
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
