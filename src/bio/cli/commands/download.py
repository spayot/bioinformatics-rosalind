import os
from pathlib import Path
import click
import requests
from dotenv import load_dotenv
from bio.cli.state import get_current

load_dotenv()


@click.command()
@click.option("--problem", help="Override the current problem name")
def download(problem):
    """Download dataset. Uses 'current' problem if `problem` is not provided."""
    problem = problem or get_current()

    if not problem:
        click.secho("✘ Error: No problem set.", fg="red")
        return

    username = os.getenv("ROSALIND_USERNAME")
    password = os.getenv("ROSALIND_PASSWORD")

    if not username or not password:
        click.secho("✘ Credentials missing in .env", fg="red")
        return

    base_url = "https://rosalind.info"
    login_url = f"{base_url}/accounts/login/"
    # The actual download trigger URL
    dataset_url = f"{base_url}/problems/{problem}/dataset/"
    target_path = Path("solutions") / problem[:-1] / problem / f"rosalind_{problem}.txt"

    with requests.Session() as session:
        # Set a User-Agent to look like a browser
        session.headers.update({"User-Agent": "Mozilla/5.0", "Referer": login_url})

        # 1. Get the login page to initialize the session and get CSRF token
        _ = session.get(login_url)
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
        click.echo(f"📥 Downloading dataset for {problem}...")
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
