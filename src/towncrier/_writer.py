# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

"""
Responsible for writing the built news fragments to a news file without
affecting existing content.
"""


import os


def append_to_newsfile(
    directory, filename, start_string, top_line, content, single_file
):

    news_file = os.path.join(directory, filename)

    existing_content = _load_existing_content(news_file, start_string, single_file)

    if top_line and top_line in existing_content[-1]:
        raise ValueError("It seems you've already produced newsfiles for this version?")

    with open(os.path.join(directory, filename), "wb") as f:

        if len(existing_content) > 1:
            f.write(existing_content.pop(0).rstrip().encode("utf8"))
            if start_string:
                f.write(("\n\n" + start_string + "\n").encode("utf8"))

        f.write(content.encode("utf8"))
        if existing_content:
            if existing_content[0]:
                f.write(b"\n\n")
            f.write(existing_content[0].lstrip().encode("utf8"))


def _load_existing_content(news_file, start_string, single_file):
    if not single_file:
        # Per-release news files always start empty.
        return [""]

    if not os.path.exists(news_file):
        # Non-existent files are equivalent to empty files.
        return [""]

    with open(news_file, encoding="utf8") as f:
        return f.read().split(start_string, 1)
