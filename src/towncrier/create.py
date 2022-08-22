# Copyright (c) Stephen Finucane, 2019
# See LICENSE for details.

"""
Create a new fragment.
"""

import os

import click

from ._settings import config_option_help, load_config_from_options


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
    default=False,
    help="Open an editor for writing the newsfragment content.",
)  # TODO: default should be true
@click.option(
    "-c",
    "--content",
    type=str,
    default="Add your info here",
    help="Sets the content of the new fragment.",
)
@click.argument("filename")
def _main(ctx, directory, config, filename, edit, content):
    """
    Create a new news fragment.

    Create a new news fragment called FILENAME or pass the full path for a file.
    Towncrier has a few standard types of news fragments, signified by the file extension.

    \b
    These are:
    * .feature - a new feature
    * .bugfix - a bug fix
    * .doc - a documentation improvement,
    * .removal - a deprecation or removal of public API,
    * .misc - a ticket has been closed, but it is not of interest to users.
    """
    return __main(ctx, directory, config, filename, edit, content)


def __main(ctx, directory, config, filename, edit, content):
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
        raise click.ClickException(f"{segment_file} already exists")

    if edit:
        content = _get_news_content_from_user(content)

    if content is None:
        click.echo("Abort creating news fragment.")
        ctx.exit(1)

    with open(segment_file, "w") as f:
        f.write(content)

    click.echo(f"Created news fragment at {segment_file}")


def _get_news_content_from_user(message):
    initial_content = (
        "# Please write your news content. When finished, save the file.\n"
        "# In order to abort, exit without saving.\n"
        '# Lines starting with "#" are ignored.\n'
    )
    if message is not None:
        initial_content += "\n" "{message}\n".format(message=message)
    content = click.edit(initial_content)
    if content is None:
        return None
    all_lines = content.split("\n")
    lines = [line.rstrip() for line in all_lines if not line.lstrip().startswith("#")]
    return "\n".join(lines)


if __name__ == "__main__":  # pragma: no cover
    _main()
