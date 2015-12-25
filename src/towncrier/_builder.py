# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from __future__ import absolute_import, division

import os


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


def render_fragments(fragments):
    """
    Render the fragments into a news file.
    """
