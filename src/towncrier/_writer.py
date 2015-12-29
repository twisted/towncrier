# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

"""
Responsible for writing the built news fragments to a news file without
affecting existing content.
"""

from __future__ import absolute_import, division

import os


def append_to_newsfile(directory, filename, name_and_version, content):

    news_file = os.path.join(directory, filename)

    if not os.path.exists(news_file):
        existing_content = ""
    else:
        with open(news_file, "r") as f:
            existing_content = f.read()

    top_line = name_and_version + "\n" + "=" * len(name_and_version) + "\n\n"

    if top_line in existing_content:
        raise ValueError(
            "It seems you've already produced newsfiles for this version?")

    with open(os.path.join(directory, filename), "w") as f:

        f.write(top_line)
        f.write(content)
        if existing_content:
            f.write("\n\n")
        f.write(existing_content)
