# Get the directory where cli.py is located
from pathlib import Path
import shutil
import click

from bio.cli.scraper import RosalindScraper
from bio.cli.state import set_current


TEMPLATE_DIR = Path(__file__).parent / "templates"


@click.command()
@click.argument("problem", required=False)  # Make name optional
def create(problem):
    """Setup folder and scrape sample dataset from the problem page."""
    target_path = Path("solutions") / problem[:-1] / problem
    target_path.mkdir(parents=True, exist_ok=True)

    # 1. Copy the __main__.py template
    source_main = TEMPLATE_DIR / "main_template.py"
    if source_main.exists():
        shutil.copy(source_main, target_path / "__main__.py")

    # 2. Scrape Sample Dataset
    click.echo(f"🔍 Fetching sample dataset for {problem}...")
    scraper = RosalindScraper(problem)

    sample_dataset = scraper.scrape_sample_dataset()
    if sample_dataset:
        test_file = target_path / "test.txt"
        test_file.write_text(sample_dataset)
        click.secho(f"✔ Sample data saved to {test_file}", fg="green")

    # scrape Sample Output and save to expected.txt
    expected_data = scraper.scrape_sample_output()
    if expected_data:
        (target_path / "expected.txt").write_text(expected_data)
        click.secho(f"✔ Sample Output saved to expected.txt", fg="green")

    # set this problem as current
    set_current(problem)
    click.echo(f"🚀 Project {problem} ready and set as current!")
