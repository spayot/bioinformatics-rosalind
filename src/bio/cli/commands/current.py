import click

from bio.cli.state import set_current


@click.command()
@click.argument("problem")
def current(problem):
    """Manually set the current problem you are working on."""
    set_current(problem)
    click.secho(f"📍 Current problem set to: {problem}", fg="magenta", bold=True)
