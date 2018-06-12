# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

"""
Responsible for writing the built news fragments to a news file without
affecting existing content.
"""

from __future__ import absolute_import, division

import os


def append_to_newsfile(directory, filename, start_line, top_line, content):

    news_file = os.path.join(directory, filename)

    if not os.path.exists(news_file):
        existing_content = u""
    else:
        with open(news_file, "rb") as f:
            existing_content = f.read().decode("utf8")

    existing_content = existing_content.split(start_line, 1)

    if top_line in existing_content:
        raise ValueError("It seems you've already produced newsfiles for this version?")

    with open(os.path.join(directory, filename), "wb") as f:

        if len(existing_content) > 1:
            f.write(existing_content.pop(0).rstrip().encode("utf8"))
            f.write((u"\n\n" + start_line + u"\n").encode("utf8"))

        f.write(top_line.encode("utf8"))
        f.write(content.encode("utf8"))
        if existing_content[0]:
            f.write(b"\n\n")
        f.write(existing_content[0].lstrip().encode("utf8"))
