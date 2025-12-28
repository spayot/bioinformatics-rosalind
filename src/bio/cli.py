import os
import subprocess
from pathlib import Path
import shutil

import click
from dotenv import load_dotenv
import pyperclip
import requests


load_dotenv()


@click.group()
def main():
    """Bio DevX CLI for Rosalind challenges."""
    pass


# Get the directory where cli.py is located
TEMPLATE_DIR = Path(__file__).parent / "templates"


@main.command()
@click.argument("name")
def create(name):
    """Setup a new challenge folder by copying templates."""
    target_path = Path("solutions") / name
    target_path.mkdir(parents=True, exist_ok=True)

    # 1. Copy the __main__.py from templates
    source_main = TEMPLATE_DIR / "main_template.py"
    if source_main.exists():
        shutil.copy(source_main, target_path / "__main__.py")
    else:
        click.secho(f"⚠ Template not found at {source_main}", fg="yellow")

    # 2. Create the empty test file (or copy a template if you prefer)
    test_file = target_path / "test.txt"
    test_file.touch()  # Creates empty file

    click.echo(f"✔ Created folder: {target_path}")


@main.command()
@click.argument("name")
def download(name):
    """Download the dataset for a given problem."""
    username = os.getenv("ROSALIND_USERNAME")
    password = os.getenv("ROSALIND_PASSWORD")

    if not username or not password:
        click.secho("✘ Credentials missing in .env", fg="red")
        return

    base_url = "https://rosalind.info"
    login_url = f"{base_url}/accounts/login/"
    # The actual download trigger URL
    dataset_url = f"{base_url}/problems/{name}/dataset/"
    target_path = Path("solutions") / name / f"rosalind_{name}.txt"

    with requests.Session() as session:
        # Set a User-Agent to look like a browser
        session.headers.update({"User-Agent": "Mozilla/5.0", "Referer": login_url})

        # 1. Get the login page to initialize the session and get CSRF token
        # get_resp = session.get(login_url)
        csrf_token = session.cookies.get("csrftoken")

        if not csrf_token:
            click.secho("✘ Could not find CSRF token.", fg="red")
            return

        # 2. Log in
        login_data = {
            "username": username,
            "password": password,
            "csrfmiddlewaretoken": csrf_token,
        }

        # Post to login. Rosalind usually redirects on success.
        post_resp = session.post(login_url, data=login_data)

        if post_resp.status_code != 200 or "Log out" not in post_resp.text:
            click.secho("✘ Login failed. Check your username and password.", fg="red")
            return

        # 3. Download the dataset
        click.echo(f"📥 Downloading dataset for {name}...")
        ds_resp = session.get(dataset_url)

        # 4. Final Validation: If we get HTML, we didn't get the file
        content_type = ds_resp.headers.get("Content-Type", "")
        if "text/html" in content_type or ds_resp.status_code != 200:
            click.secho(
                "✘ Download failed. Is the problem active/accessible?", fg="red"
            )
            # Debug: Print first 100 chars if it's HTML
            return

        # Save the file
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(ds_resp.text.strip())
        click.secho(f"✔ Dataset saved to {target_path}", fg="green")


@main.command()
@click.argument("folder")
@click.argument("mode", type=click.Choice(["test", "prod"]))
def run(folder, mode):
    """Run the challenge. In 'prod' mode, the result is copied to clipboard."""
    folder_path = Path("solutions") / folder
    script_path = folder_path  # / "__main__.py"

    if mode == "test":
        data_file = folder_path / "test.txt"
    else:
        data_file = folder_path / f"rosalind_{folder}.txt"

    if not data_file.exists():
        click.echo(f"✘ Error: {data_file} not found.", err=True)
        return

    # Use check_output to capture the print statements from your script
    try:
        # We run the script and capture 'stdout' (what you print)
        result = subprocess.check_output(
            ["python3", str(script_path), str(data_file)], text=True
        ).strip()

        # Print the result to the console so you can see it
        click.echo(f"--- Execution Output ---\n{result}\n------------------------")

        # Logic for clipboard (only on prod)
        if mode == "prod":
            pyperclip.copy(result)
            click.secho("🚀 Result copied to clipboard!", fg="green", bold=True)

    except subprocess.CalledProcessError as e:
        click.secho(f"✘ Script crashed with error:\n{e}", fg="red")


if __name__ == "__main__":
    main()
