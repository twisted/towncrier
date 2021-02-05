import click
import packaging.utils


@click.command()
@click.argument("version")
def cli(version):
    """Canonicalizes the passed version according to PEP 517."""
    canonicalized_version = packaging.utils.canonicalize_version(version)

    click.echo(canonicalized_version)


if __name__ == "__main__":
    cli()
