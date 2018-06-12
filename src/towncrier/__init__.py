# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

"""
towncrier, a builder for your news files.
"""

from __future__ import absolute_import, division

import os
import click
import pkg_resources

from datetime import date

from ._settings import load_config
from ._builder import find_fragments, split_fragments, render_fragments
from ._project import get_version, get_project_name
from ._writer import append_to_newsfile
from ._git import remove_files, stage_newsfile
from ._version import __version__


def _get_date():
    return date.today().isoformat()


@click.command()
@click.option(
    "--draft",
    "draft",
    default=False,
    flag_value=True,
    help=("Render the news fragments, don't write to files, " "don't check versions."),
)
@click.option("--dir", "directory", default=".")
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
def _main(draft, directory, project_name, project_version, project_date, answer_yes):
    return __main(
        draft, directory, project_name, project_version, project_date, answer_yes
    )


def __main(draft, directory, project_name, project_version, project_date, answer_yes):
    """
    The main entry point.
    """
    directory = os.path.abspath(directory)
    config = load_config(directory)
    to_err = draft

    click.echo("Loading template...", err=to_err)
    if config["template"] is None:
        template = pkg_resources.resource_string(
            __name__, "templates/template.rst"
        ).decode("utf8")
    else:
        with open(config["template"], "rb") as tmpl:
            template = tmpl.read().decode("utf8")

    click.echo("Finding news fragments...", err=to_err)

    definitions = config["types"]

    if config.get("directory"):
        base_directory = os.path.abspath(config["directory"])
        fragment_directory = None
    else:
        base_directory = os.path.abspath(
            os.path.join(directory, config["package_dir"], config["package"])
        )
        fragment_directory = "newsfragments"

    fragments, fragment_filenames = find_fragments(
        base_directory, config["sections"], fragment_directory, definitions
    )

    click.echo("Rendering news fragments...", err=to_err)
    fragments = split_fragments(fragments, definitions)
    rendered = render_fragments(
        # The 0th underline is used for the top line
        template,
        config["issue_format"],
        fragments,
        definitions,
        config["underlines"][1:],
        config["wrap"],
    )

    if project_version is None:
        project_version = get_version(
            os.path.join(directory, config["package_dir"]), config["package"]
        )

    if project_name is None:
        package = config.get("package")
        if package:
            project_name = get_project_name(
                os.path.abspath(os.path.join(directory, config["package_dir"])), package
            )
        else:
            # Can't determine a project_name, but maybe it is not needed.
            project_name = ""

    if project_date is None:
        project_date = _get_date()

    top_line = config["title_format"].format(
        name=project_name, version=project_version, project_date=project_date
    )
    top_line += u"\n" + (config["underlines"][0] * len(top_line)) + u"\n"

    if draft:
        click.echo(
            "Draft only -- nothing has been written.\n"
            "What is seen below is what would be written.\n",
            err=to_err,
        )
        click.echo("%s\n%s" % (top_line, rendered))
    else:
        click.echo("Writing to newsfile...", err=to_err)
        start_line = config["start_line"]
        append_to_newsfile(
            directory, config["filename"], start_line, top_line, rendered
        )

        click.echo("Staging newsfile...", err=to_err)
        stage_newsfile(directory, config["filename"])

        click.echo("Removing news fragments...", err=to_err)
        remove_files(fragment_filenames, answer_yes)

        click.echo("Done!", err=to_err)


__all__ = ["__version__"]
