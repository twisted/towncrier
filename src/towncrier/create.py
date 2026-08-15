# Copyright (c) Stephen Finucane, 2019
# See LICENSE for details.

"""
Create a new fragment.
"""

from __future__ import annotations

import os

from collections.abc import Iterable
from pathlib import Path
from typing import cast

import click

from ._builder import FragmentsPath, parse_newfragment_basename
from ._settings import config_option_help, load_config_from_options


DEFAULT_CONTENT = "Add your info here"


@click.command(name="create")
@click.pass_context
@click.option(
    "--dir",
    "directory",
    default=None,
    metavar="PATH",
    help="Create fragment in directory. Default to current directory.",
)
@click.option(
    "--config",
    "config",
    default=None,
    metavar="FILE_PATH",
    help=config_option_help,
)
@click.option(
    "--edit/--no-edit",
    default=None,
    help="Open an editor for writing the newsfragment content.",
)
@click.option(
    "-c",
    "--content",
    type=str,
    default=DEFAULT_CONTENT,
    help="Sets the content of the new fragment.",
)
@click.option(
    "--section",
    type=str,
    help="The section to create the fragment for.",
)
@click.option(
    "--sub-issue",
    type=click.IntRange(min=0),
    metavar="N",
    default=None,
    help="Optional numeric sub issue id of the fragment",
)
@click.argument("filename", default="")
def _main(
    ctx: click.Context,
    directory: str | None,
    config: str | None,
    filename: str,
    edit: bool | None,
    content: str,
    section: str | None,
    sub_issue: int | None,
) -> None:
    """
    Create a new news fragment.

    If FILENAME is not provided, you'll be prompted to create it.

    Towncrier has a few standard types of news fragments, signified by the file
    extension.

    \b
    These are:
    * .feature - a new feature
    * .bugfix - a bug fix
    * .doc - a documentation improvement,
    * .removal - a deprecation or removal of public API,
    * .misc - an issue has been closed, but it is not of interest to users.

    If the FILENAME base is just '+' (to create a fragment not tied to an
    issue), it will be appended with a random hex string.
    """
    __main(ctx, directory, config, filename, edit, content, section, sub_issue)


def __main(
    ctx: click.Context,
    directory: str | None,
    config_path: str | None,
    filename: str,
    edit: bool | None,
    content: str,
    section: str | None,
    sub_issue: int | None,
) -> None:
    """
    The main entry point.
    """
    base_directory, config = load_config_from_options(directory, config_path)

    filename_ext = ""
    if config.create_add_extension:
        ext = os.path.splitext(config.filename)[1]
        if ext.lower() in (".rst", ".md"):
            filename_ext = ext

    section_provided = section is not None
    if not section_provided:
        # Get the default section.
        if len(config.sections) == 1:
            section = next(iter(config.sections))
        else:
            # If there are multiple sections then the first without a path is the default
            # section, otherwise it's the first defined section.
            for (
                section_name,
                section_dir,
            ) in config.sections.items():  # pragma: no branch
                if not section_dir:
                    section = section_name
                    break
            if section is None:
                section = list(config.sections.keys())[0]

    if section not in config.sections:
        # Raise a click exception with the correct parameter.
        section_param = None
        for p in ctx.command.params:  # pragma: no branch
            if p.name == "section":
                section_param = p
                break
        expected_sections = ", ".join(f"'{s}'" for s in config.sections)
        raise click.BadParameter(
            f"expected one of {expected_sections}",
            param=section_param,
        )
    section = cast(str, section)

    if not filename:
        if not section_provided:
            sections = list(config.sections)
            if len(sections) > 1:
                click.echo("Pick a section:")
                default_section_index = None
                for i, s in enumerate(sections):
                    click.echo(f" {i + 1}: {s or '(primary)'}")
                    if not default_section_index and s == section:
                        default_section_index = str(i + 1)
                section_index = click.prompt(
                    "Section",
                    type=click.Choice([str(i + 1) for i in range(len(sections))]),
                    default=default_section_index,
                )
                section = sections[int(section_index) - 1]
        prompt = "Issue number"
        # Add info about adding orphan if config is set.
        if config.orphan_prefix:
            prompt += f" (`{config.orphan_prefix}` if none)"
        issue = click.prompt(prompt)
        fragment_type = click.prompt(
            "Fragment type",
            type=click.Choice(list(config.types)),
        )
        filename = f"{issue}.{fragment_type}"
        if edit is None and content == DEFAULT_CONTENT:
            edit = True

    file_dir, file_basename = os.path.split(filename)
    if config.orphan_prefix and file_basename.startswith(f"{config.orphan_prefix}."):
        # Append a random hex string to the orphan news fragment base name.
        filename = os.path.join(
            file_dir,
            (
                f"{config.orphan_prefix}{os.urandom(4).hex()}"
                f"{file_basename[len(config.orphan_prefix) :]}"
            ),
        )
    filename_parts = filename.split(".")
    _validate_create_filename(filename, config.types)

    if filename_parts[-1] in config.types and filename_ext:
        filename += filename_ext

    get_fragments_path = FragmentsPath(base_directory, config)
    fragments_directory = get_fragments_path(section_directory=config.sections[section])

    if not os.path.exists(fragments_directory):
        os.makedirs(fragments_directory)

    segment_file = os.path.join(fragments_directory, filename)

    if filename.split(".")[-1] not in config.types:
        filename, extra_ext = os.path.splitext(filename)
    else:
        extra_ext = ""

    if sub_issue is None:
        retry = 0
        while os.path.exists(segment_file):
            retry += 1
            segment_file = os.path.join(
                fragments_directory, f"{filename}.{retry}{extra_ext}"
            )
    else:
        segment_file = os.path.join(
            fragments_directory,
            f"{filename}{'.' + str(sub_issue) if sub_issue > 0 else ''}{extra_ext}",
        )

    if edit:
        if content == DEFAULT_CONTENT:
            content = ""
        content = _get_news_content_from_user(content, extension=filename_ext)
        if not content:
            click.echo("Aborted creating news fragment due to empty message.")
            ctx.exit(1)

    add_newline = bool(
        config.create_eof_newline and content and not content.endswith("\n")
    )
    Path(segment_file).write_text(content + "\n" * add_newline, encoding="utf-8")

    click.echo(f"Created news fragment at {segment_file}")


def _validate_create_filename(filename: str, types: Iterable[str]) -> None:
    """Reject fragment names that ``build`` cannot parse, or that hide extra dots.

    ``towncrier create`` previously only checked that the last or second-to-last
    component was a known type. That accepted names such as
    ``foo.bar.baz.config`` (when ``config`` is a type), which ``build`` then
    treats as issue ``foo.bar.baz``. The issue identifier must not contain
    ``.`` because dots separate ``{name}.{type}`` (and an optional counter or
    suffix).
    """
    basename = os.path.basename(filename)
    issue, category, _counter = parse_newfragment_basename(basename, types)
    if category is None or issue is None:
        raise click.BadParameter(
            "Expected filename '{}' to be of format '{{name}}.{{type}}', "
            "where '{{name}}' is an arbitrary slug and '{{type}}' is "
            "one of: {}".format(filename, ", ".join(types))
        )
    if "." in issue:
        raise click.BadParameter(
            f"Issue identifier '{issue}' in '{filename}' must not contain '.'. "
            "Dots separate '{name}.{type}' (and an optional counter or suffix)."
        )


def _get_news_content_from_user(message: str, extension: str = "") -> str:
    initial_content = """
# Please write your news content. Lines starting with '#' will be ignored, and
# an empty message aborts.
"""
    if message:
        initial_content = f"{message}\n{initial_content}"
    content = click.edit(initial_content, extension=extension or ".txt")
    if content is None:
        return message
    all_lines = content.split("\n")
    lines = [line.rstrip() for line in all_lines if not line.lstrip().startswith("#")]
    return "\n".join(lines).strip()


if __name__ == "__main__":  # pragma: no cover
    _main()
