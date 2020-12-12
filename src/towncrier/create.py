# Copyright (c) Stephen Finucane, 2019
# See LICENSE for details.

"""
Create a new fragment.
"""

from __future__ import absolute_import

import os
import click

from ._settings import load_config_from_options


@click.command(name="create")
@click.pass_context
@click.option("--dir", "directory", default=None)
@click.option("--config", "config", default=None)
@click.option(
    "--edit/--no-edit",
    default=False,
    help="Open an editor for writing the newsfragment content.",
)  # TODO: default should be true
@click.argument("filename")
def _main(ctx, directory, config, filename, edit):
    return __main(ctx, directory, config, filename, edit)


def __main(ctx, directory, config, filename, edit):
    """
    The main entry point.
    """
    base_directory, config = load_config_from_options(directory, config)

    definitions = config["types"] or []
    if len(filename.split(".")) < 2 or (
        filename.split(".")[-1] not in definitions
        and filename.split(".")[-2] not in definitions
    ):
        raise click.BadParameter(
            "Expected filename '{}' to be of format '{{name}}.{{type}}', "
            "where '{{name}}' is an arbitrary slug and '{{type}}' is "
            "one of: {}".format(filename, ", ".join(definitions))
        )

    if config.get("directory"):
        fragments_directory = os.path.abspath(
            os.path.join(base_directory, config["directory"])
        )
    else:
        fragments_directory = os.path.abspath(
            os.path.join(
                base_directory,
                config["package_dir"],
                config["package"],
                "newsfragments",
            )
        )

    if not os.path.exists(fragments_directory):
        os.makedirs(fragments_directory)

    segment_file = os.path.join(fragments_directory, filename)
    if os.path.exists(segment_file):
        raise click.ClickException("{} already exists".format(segment_file))

    if edit:
        content = _get_news_content_from_user()
    else:
        content = "Add your info here"

    if content is None:
        click.echo("Abort creating news fragment.")
        ctx.exit(1)

    with open(segment_file, "w") as f:
        f.write(content)

    click.echo("Created news fragment at {}".format(segment_file))


def _get_news_content_from_user():
    content = click.edit(
        "# Please write your news content. When finished, save the file.\n"
        "# In order to abort, exit without saving.\n"
        "# Lines starting with \"#\" are ignored.\n"
    )
    if content is None:
        return None
    all_lines = content.split("\n")
    lines = [line.rstrip() for line in all_lines if not line.lstrip().startswith("#")]
    return "\n".join(lines)


if __name__ == "__main__":  # pragma: no cover
    _main()
