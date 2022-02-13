import click
import incremental
import packaging.utils


@click.command()
@click.argument("version")
def cli(version):
    """Canonicalizes the passed version according to incremental."""

    parsed_version = packaging.utils.Version(version)

    release_candidate = None
    if parsed_version.pre is not None:
        if parsed_version.pre[0] == 'rc':
            release_candidate = parsed_version.pre[1]

    incremental_version = incremental.Version(
        package="",
        major=parsed_version.major,
        minor=parsed_version.minor,
        micro=parsed_version.micro,
        release_candidate=release_candidate,
        post=parsed_version.post,
        dev=parsed_version.dev,
    )

    click.echo(incremental_version.public())


if __name__ == "__main__":
    cli()
