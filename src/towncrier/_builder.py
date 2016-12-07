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


def render_fragments(template, fragments, definitions, major=u"-", minor=u"~"):
    """
    Render the fragments into a news file.
    """

    jinja_template = Template(template, trim_blocks=True)

    data = {}

    for section_name, section_value in fragments.items():

        data[section_name] = {}

        for category_name, category_value in section_value.items():
            categories = OrderedDict()

            for text, tickets in category_value.items():
                ticket_numbers = []

                for ticket in tickets:
                    try:
                        int(ticket)
                        ticket_numbers.append(u"#" + ticket)
                    except:
                        ticket_numbers.append(ticket)

                categories[text] = ticket_numbers

            data[section_name][category_name] = categories

    done = []

    res = jinja_template.render(sections=data, definitions=definitions)

    for line in res.split("\n"):
        done.append(textwrap.fill(line, width=79, subsequent_indent=u"  "))

    return "\n".join(done)
