# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

"""
Responsible for writing the built news fragments to a news file without
affecting existing content.
"""

from __future__ import annotations

from pathlib import Path


def append_to_newsfile(
    directory: str,
    filename: str,
    start_string: str,
    top_line: str,
    content: str,
    single_file: bool,
) -> None:
    """
    Write *content* to *directory*/*filename* behind *start_string*.

    Double-check *top_line* (i.e. the release header) is not already in the
    file.

    if *single_file* is True, add it to an existing file, otherwise create a
    fresh one.
    """
    news_file = Path(directory) / filename

    header, prev_body = _figure_out_existing_content(
        news_file, start_string, single_file
    )

    if top_line and top_line in prev_body:
        raise ValueError("It seems you've already produced newsfiles for this version?")

    # Leave newlines alone. This probably leads to inconsistent newlines,
    # because we've loaded existing content with universal newlines, but that's
    # the original behavior.
    with news_file.open("w", encoding="utf8", newline="") as f:
        if header:
            f.write(header)
        # If there is no previous body that means we're writing a brand new news file.
        # We don't want extra whitespace at the end of this new file.
        f.write(content + prev_body if prev_body else content.rstrip() + "\n")


def _figure_out_existing_content(
    news_file: Path, start_string: str, single_file: bool
) -> tuple[str, str]:
    """
    Try to read *news_file* and split it into header (everything before
    *start_string*) and the old body (everything after *start_string*).

    If there's no *start_string*, return empty header.

    Empty file and per-release files have neither.
    """
    if not single_file or not news_file.exists():
        # Per-release news files always start empty.
        # Non-existent files have no existing content.
        return "", ""

    # If we didn't use universal newlines here, we wouldn't find *start_string*
    # which usually contains a `\n`.
    with news_file.open(encoding="utf8") as f:
        content = f.read()

    t = content.split(start_string, 1)
    if len(t) == 2:
        return f"{t[0].rstrip()}\n\n{start_string}\n", t[1].lstrip()

    return "", content.lstrip()
