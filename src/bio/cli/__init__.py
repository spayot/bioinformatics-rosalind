import click
from .commands import create, run, download, current


@click.group()
def main():
    """Bio DevX CLI for Rosalind challenges."""
    pass


# Register subcommands
main.add_command(create.create)
main.add_command(run.run)
main.add_command(download.download)
main.add_command(current.current)
