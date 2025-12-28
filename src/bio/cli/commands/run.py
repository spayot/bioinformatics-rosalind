from pathlib import Path
import subprocess

import click
import pyperclip

from bio.cli.state import get_current


@click.command()
@click.argument("mode", type=click.Choice(["test", "prod"]))
@click.option("--problem", help="Override the current problem name")
def run(mode, problem):
    """Run the challenge. In 'test' mode, compares output to expected.txt. Uses 'current' problem if name is not provided."""
    target = problem or get_current()

    if not target:
        click.secho(
            "✘ Error: No problem name provided and no 'current' problem set.", fg="red"
        )
        return

    # Use 'target' for the rest of your logic...
    click.echo(f"🏃 Running {mode} for {target}...")

    folder_path = Path("solutions") / target[:-1] / target
    script_path = folder_path / "__main__.py"

    data_file = folder_path / (
        "test.txt" if mode == "test" else f"rosalind_{target}.txt"
    )

    if not data_file.exists():
        click.secho(f"✘ Error: {data_file} not found.", fg="red")
        return

    try:
        # Capture the output
        result = subprocess.check_output(
            ["python", str(script_path), str(data_file)], text=True
        ).strip()

        click.echo(f"\n--- Output ---\n{result}\n--------------")

        if mode == "test":
            expected_path = folder_path / "expected.txt"
            if expected_path.exists():
                expected = expected_path.read_text().strip()

                if sorted(result.split()) == sorted(expected.split()):
                    click.secho("✅ TEST PASSED!", fg="green", bold=True)
                else:
                    click.secho("❌ TEST FAILED!", fg="red", bold=True)
                    click.echo(f"Expected: {expected}")
            else:
                click.secho("⚠ No expected.txt found to compare.", fg="yellow")

        elif mode == "prod":
            pyperclip.copy(result)
            click.secho("🚀 Result copied to clipboard!", fg="cyan", bold=True)

    except subprocess.CalledProcessError as e:
        click.secho(f"✘ Script crashed:\n{e}", fg="red")
