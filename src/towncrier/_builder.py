# Copyright (c) Amber Brown, 2015
# See LICENSE for details.


from __future__ import annotations

import os
import re
import textwrap

from collections import defaultdict
from pathlib import Path
from typing import Any, DefaultDict, Iterable, Iterator, Mapping, NamedTuple, Sequence

from jinja2 import Template


# Returns ticket, category and counter or (None, None, None) if the basename
# could not be parsed or doesn't contain a valid category.
def parse_newfragment_basename(
    basename: str, frag_type_names: Iterable[str]
) -> tuple[str, str, int] | tuple[None, None, None]:
    invalid = (None, None, None)
    parts = basename.split(".")

    if len(parts) == 1:
        return invalid

    # There are at least 2 parts. Search for a valid category from the second
    # part onwards starting at the back.
    # The category is used as the reference point in the parts list to later
    # infer the issue number and counter value.
    for i in reversed(range(1, len(parts))):
        if parts[i] in frag_type_names:
            # Current part is a valid category according to given definitions.
            category = parts[i]
            # Use all previous parts as the ticket number.
            # NOTE: This allows news fragment names like fix-1.2.3.feature or
            # something-cool.feature.ext for projects that don't use ticket
            # numbers in news fragment names.
            ticket = ".".join(parts[0:i]).strip()
            # If the ticket is an integer, remove any leading zeros (to resolve
            # issue #126).
            if ticket.isdigit():
                ticket = str(int(ticket))
            counter = 0
            # Use the following part as the counter if it exists and is a valid
            # digit.
            if len(parts) > (i + 1) and parts[i + 1].isdigit():
                counter = int(parts[i + 1])
            return ticket, category, counter
    else:
        # No valid category found.
        return invalid


# Returns a structure like:
#
# {
#     "": {
#         ("142", "misc"): "",
#         ("1", "feature"): "some cool description",
#     },
#     "Names": {},
#     "Web": {("3", "bugfix"): "Fixed a thing"},
# }
#
# We should really use attrs.
#
# Also returns a list of the paths that the fragments were taken from.
def find_fragments(
    base_directory: str,
    sections: Mapping[str, str],
    fragment_directory: str | None,
    frag_type_names: Iterable[str],
    orphan_prefix: str | None = None,
) -> tuple[Mapping[str, Mapping[tuple[str, str, int], str]], list[str]]:
    """
    Sections are a dictonary of section names to paths.
    """
    content = {}
    fragment_filenames = []
    # Multiple orphan news fragments are allowed per section, so initialize a counter
    # that can be incremented automatically.
    orphan_fragment_counter: DefaultDict[str | None, int] = defaultdict(int)

    for key, val in sections.items():
        if fragment_directory is not None:
            section_dir = os.path.join(base_directory, val, fragment_directory)
        else:
            section_dir = os.path.join(base_directory, val)

        try:
            files = os.listdir(section_dir)
        except FileNotFoundError:
            files = []

        file_content = {}

        for basename in files:
            ticket, category, counter = parse_newfragment_basename(
                basename, frag_type_names
            )
            if category is None:
                continue
            assert ticket is not None
            assert counter is not None
            if orphan_prefix and ticket.startswith(orphan_prefix):
                ticket = ""
                # Use and increment the orphan news fragment counter.
                counter = orphan_fragment_counter[category]
                orphan_fragment_counter[category] += 1

            full_filename = os.path.join(section_dir, basename)
            fragment_filenames.append(full_filename)
            data = Path(full_filename).read_text(encoding="utf-8", errors="replace")

            if (ticket, category, counter) in file_content:
                raise ValueError(
                    "multiple files for {}.{} in {}".format(
                        ticket, category, section_dir
                    )
                )
            file_content[ticket, category, counter] = data

        content[key] = file_content

    return content, fragment_filenames


def indent(text: str, prefix: str) -> str:
    """
    Adds `prefix` to the beginning of non-empty lines in `text`.
    """

    # Based on Python 3's textwrap.indent
    def prefixed_lines() -> Iterator[str]:
        for line in text.splitlines(True):
            yield (prefix + line if line.strip() else line)

    return "".join(prefixed_lines())


# Takes the output from find_fragments above. Probably it would be useful to
# add an example output here. Next time someone digs deep enough to figure it
# out, please do so...
def split_fragments(
    fragments: Mapping[str, Mapping[tuple[str, str, int], str]],
    definitions: Mapping[str, Mapping[str, Any]],
    all_bullets: bool = True,
) -> Mapping[str, Mapping[str, Mapping[str, Sequence[str]]]]:
    output = {}

    for section_name, section_fragments in fragments.items():
        section: dict[str, dict[str, list[str]]] = {}

        for (ticket, category, counter), content in section_fragments.items():
            if all_bullets:
                # By default all fragmetns are append by "-" automatically,
                # and need to be indented because of that.
                # (otherwise, assume they are formatted correctly)
                content = indent(content.strip(), "  ")[2:]
            else:
                # Assume the text is formatted correctly
                content = content.rstrip()

            if definitions[category]["showcontent"] is False:
                content = ""

            texts = section.setdefault(category, {})

            tickets = texts.setdefault(content, [])
            if ticket:
                # Only add the ticket if we have one (it can be blank for orphan news
                # fragments).
                tickets.append(ticket)
                tickets.sort()

        output[section_name] = section

    return output


class IssueParts(NamedTuple):
    is_digit: bool
    has_digit: bool
    non_digit_part: str
    number: int


def issue_key(issue: str) -> IssueParts:
    """
    Used to sort issues in a human-friendly way.

    Issues are grouped their non-integer part, then sorted by their integer part.

    For backwards compatible consistency, issues without no number are sorted first and
    digit only issues are sorted last.

    For example::

    >>> sorted(["2", "#11", "#3", "gh-10", "gh-4", "omega", "alpha"], key=issue_key)
    ['alpha', 'omega', '#3', '#11', 'gh-4', 'gh-10', '2']
    """
    if issue.isdigit():
        return IssueParts(
            is_digit=True, has_digit=True, non_digit_part="", number=int(issue)
        )
    match = re.search(r"\d+", issue)
    if not match:
        return IssueParts(
            is_digit=False, has_digit=False, non_digit_part=issue, number=-1
        )
    return IssueParts(
        is_digit=False,
        has_digit=True,
        non_digit_part=issue[: match.start()] + issue[match.end() :],
        number=int(match.group()),
    )


def entry_key(entry: tuple[str, Sequence[str]]) -> tuple[str, list[IssueParts]]:
    content, issues = entry
    # Orphan news fragments (those without any issues) should sort last by content.
    return "" if issues else content, [issue_key(issue) for issue in issues]


def bullet_key(entry: tuple[str, Sequence[str]]) -> int:
    text, _ = entry
    if not text:
        return -1
    if text[:2] == "- ":
        return 0
    elif text[:2] == "* ":
        return 1
    elif text[:3] == "#. ":
        return 2
    return 3


def render_issue(issue_format: str | None, issue: str) -> str:
    if issue_format is None:
        try:
            int(issue)
            return "#" + issue
        except Exception:
            return issue
    else:
        return issue_format.format(issue=issue)


def render_fragments(
    template: str,
    issue_format: str | None,
    fragments: Mapping[str, Mapping[str, Mapping[str, Sequence[str]]]],
    definitions: Mapping[str, Mapping[str, Any]],
    underlines: Sequence[str],
    wrap: bool,
    versiondata: Mapping[str, str],
    top_underline: str = "=",
    all_bullets: bool = False,
    render_title: bool = True,
) -> str:
    """
    Render the fragments into a news file.
    """

    jinja_template = Template(template, trim_blocks=True)

    data: dict[str, dict[str, dict[str, list[str]]]] = {}
    issues_by_category: dict[str, dict[str, list[str]]] = {}

    for section_name, section_value in fragments.items():
        data[section_name] = {}
        issues_by_category[section_name] = {}

        for category_name, category_value in section_value.items():
            category_issues: set[str] = set()
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
                category_issues.update(issues)

            # Then we sort the lines:
            #
            # - Fix the other thing (#1)
            # - Fix the thing (#2, #7, #123)
            entries.sort(key=entry_key)
            if not all_bullets:
                entries.sort(key=bullet_key)

            # Then we put these nicely sorted entries back in an ordered dict
            # for the template, after formatting each issue number
            categories = {}
            for text, issues in entries:
                rendered = [render_issue(issue_format, i) for i in issues]
                categories[text] = rendered

            data[section_name][category_name] = categories
            issues_by_category[section_name][category_name] = [
                render_issue(issue_format, i)
                for i in sorted(category_issues, key=issue_key)
            ]

    done = []

    def get_indent(text: str) -> str:
        # If bullets are not assumed and we wrap, the subsequent
        # indentation depends on whether or not this is a bullet point.
        # (it is probably usually best to disable wrapping in that case)
        if all_bullets or text[:2] == "- " or text[:2] == "* ":
            return "  "
        elif text[:3] == "#. ":
            return "   "
        return ""

    res = jinja_template.render(
        render_title=render_title,
        sections=data,
        definitions=definitions,
        underlines=underlines,
        versiondata=versiondata,
        top_underline=top_underline,
        get_indent=get_indent,  # simplify indentation in the jinja template.
        issues_by_category=issues_by_category,
    )

    for line in res.split("\n"):
        if wrap:
            done.append(
                textwrap.fill(
                    line,
                    width=79,
                    subsequent_indent=get_indent(line),
                    break_long_words=False,
                    break_on_hyphens=False,
                )
            )
        else:
            done.append(line)

    return "\n".join(done)
