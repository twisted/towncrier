# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

"""
Build a combined news file from news fragments.
"""

from __future__ import absolute_import, division, print_function

import os
import click
import sys

from datetime import date

from ._settings import load_config_from_options, ConfigError
from ._builder import find_fragments, split_fragments, render_fragments
from ._project import get_version, get_project_name
from ._writer import append_to_newsfile
from ._git import remove_files, stage_newsfile


def _get_date():
    return date.today().isoformat()


@click.command(name="build")
@click.option(
    "--draft",
    "draft",
    default=False,
    flag_value=True,
    help="Render the news fragments, don't write to files, don't check versions.",
)
@click.option("--config", "config_file", default=None, help="Configuration file name.")
@click.option("--dir", "directory", default=None)
@click.option("--name", "project_name", default=None)
@click.option(
    "--version",
    "project_version",
    default=None,
    help="Render the news fragments using given version.",
)
@click.option("--date", "project_date", default=None)
@click.option(
    "--yes",
    "answer_yes",
    default=False,
    flag_value=True,
    help="Do not ask for confirmation to remove news fragments.",
)
def _main(
    draft,
    directory,
    config_file,
    project_name,
    project_version,
    project_date,
    answer_yes,
):
    try:
        return __main(
            draft,
            directory,
            config_file,
            project_name,
            project_version,
            project_date,
            answer_yes,
        )
    except ConfigError as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def __main(
    draft,
    directory,
    config_file,
    project_name,
    project_version,
    project_date,
    answer_yes,
):
    """
    The main entry point.
    """
    base_directory, config = load_config_from_options(directory, config_file)
    to_err = draft

    click.echo("Loading template...", err=to_err)
    with open(config["template"], "rb") as tmpl:
        template = tmpl.read().decode("utf8")

    click.echo("Finding news fragments...", err=to_err)

    definitions = config["types"]

    if config.get("directory"):
        fragment_base_directory = os.path.abspath(config["directory"])
        fragment_directory = None
    else:
        fragment_base_directory = os.path.abspath(
            os.path.join(base_directory, config["package_dir"], config["package"])
        )
        fragment_directory = "newsfragments"

    fragments, fragment_filenames = find_fragments(
        fragment_base_directory, config["sections"], fragment_directory, definitions
    )

    click.echo("Rendering news fragments...", err=to_err)
    fragments = split_fragments(
        fragments, definitions, all_bullets=config["all_bullets"]
    )

    if project_version is None:
        project_version = config.get('version')
        if project_version is None:
            project_version = get_version(
                os.path.join(base_directory, config["package_dir"]), config["package"]
            ).strip()

    if project_name is None:
        project_name = config.get('name')
        if not project_name:
            package = config.get("package")
            if package:
                project_name = get_project_name(
                    os.path.abspath(os.path.join(base_directory, config["package_dir"])),
                    package,
                )
            else:
                # Can't determine a project_name, but maybe it is not needed.
                project_name = ""

    if project_date is None:
        project_date = _get_date().strip()

    if config["title_format"]:
        top_line = config["title_format"].format(
            name=project_name, version=project_version, project_date=project_date
        )
    else:
        top_line = ""

    rendered = render_fragments(
        # The 0th underline is used for the top line
        template,
        config["issue_format"],
        top_line,
        fragments,
        definitions,
        config["underlines"][1:],
        config["wrap"],
        {"name": project_name, "version": project_version, "date": project_date},
        top_underline=config["underlines"][0],
        all_bullets=config["all_bullets"],
    )

    if draft:
        click.echo(
            "Draft only -- nothing has been written.\n"
            "What is seen below is what would be written.\n",
            err=to_err,
        )
        click.echo(rendered)
    else:
        click.echo("Writing to newsfile...", err=to_err)
        start_string = config["start_string"]
        news_file = config["filename"]

        if config["single_file"]:
            # When single_file is enabled, the news file name changes based on the version.
            news_file = news_file.format(
                name=project_name, version=project_version, project_date=project_date
            )

        append_to_newsfile(
            base_directory,
            news_file,
            start_string,
            top_line,
            rendered,
            single_file=config["single_file"],
        )

        click.echo("Staging newsfile...", err=to_err)
        stage_newsfile(base_directory, news_file)

        click.echo("Removing news fragments...", err=to_err)
        remove_files(fragment_filenames, answer_yes)

        click.echo("Done!", err=to_err)


if __name__ == "__main__":  # pragma: no cover
    _main()
