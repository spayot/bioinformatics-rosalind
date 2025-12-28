from bs4 import BeautifulSoup
import click
import requests


class RosalindScraper:
    def __init__(self, problem: str):
        self.problem_url = f"https://rosalind.info/problems/{problem}/"

        try:
            response = requests.get(self.problem_url)
            if response.status_code == 200:
                self.soup = BeautifulSoup(response.text, "html.parser")

        except Exception as e:
            click.secho(f"✘ Scraper Error: {e}", fg="red")

    def scrape_sample_dataset(self) -> str | None:
        # 1. Target the specific ID Rosalind uses for the Sample Dataset header
        sample_header = self.soup.find("h2", id="sample-dataset")

        if sample_header:
            # 2. Find the div with class 'codehilite' that follows the header
            code_container = sample_header.find_next_sibling("div", class_="codehilite")

            if code_container and code_container.pre:
                sample_data = code_container.pre.get_text().strip()
                return sample_data
            else:
                click.secho(
                    "⚠ Found header but couldn't find <div class='codehilite'><pre> block.",
                    fg="yellow",
                )
        else:
            # Fallback: some older problems use <h3> or just text
            click.secho(
                "⚠ 'h2#sample-dataset' not found, trying fallback...", fg="yellow"
            )
            fallback = self.soup.find(
                lambda tag: tag.name in ["h2", "h3"] and "Sample Dataset" in tag.text
            )
            if fallback:
                # Look for the first 'pre' tag that appears after this header
                code_block = fallback.find_next("pre")
                if code_block:
                    return code_block.get_text().strip()

    def scrape_sample_output(self) -> str | None:
        output_header = self.soup.find("h2", id="sample-output")
        if output_header:
            output_container = output_header.find_next_sibling(
                "div", class_="codehilite"
            )
            if output_container and output_container.pre:
                expected_data = output_container.pre.get_text().strip()
                return expected_data
