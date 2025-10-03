"""
Scrape H1B visa sponsorship data from h1bdata.info.

This module scrapes the list of top H1B sponsoring companies and saves
the data to a CSV file for further analysis and job search targeting.
"""

import logging
import csv
from pathlib import Path
from typing import List, Optional
import requests
from bs4 import BeautifulSoup

from src.models.scraping import H1BCompany

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Default source URL
DEFAULT_URL = "https://h1bdata.info/topcompanies.php"


class H1BCompanyScraper:
    """
    Scraper for H1B visa sponsorship company data.

    This class provides methods to scrape and parse H1B company information
    from h1bdata.info, including company rankings, filing statistics, and
    other relevant data for job seekers.

    Attributes:
        url: Source URL for H1B company data
        timeout: Request timeout in seconds
    """

    def __init__(self, url: str = DEFAULT_URL, timeout: int = 10):
        """
        Initialize H1B company scraper.

        Args:
            url: Source URL for scraping (default: h1bdata.info topcompanies)
            timeout: HTTP request timeout in seconds
        """
        self.url = url
        self.timeout = timeout
        logger.info(f"Initialized H1B scraper for URL: {url}")

    def fetch_page(self) -> BeautifulSoup:
        """
        Fetch and parse the H1B companies webpage.

        Returns:
            BeautifulSoup object with parsed HTML

        Raises:
            requests.RequestException: If HTTP request fails
        """
        logger.info(f"Fetching data from: {self.url}")
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            logger.info(f"✓ Successfully fetched page (status: {response.status_code})")
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            logger.error(f"Failed to fetch page: {e}")
            raise

    def parse_table(self, soup: BeautifulSoup) -> tuple[List[str], List[List[str]]]:
        """
        Parse H1B company table from HTML.

        Args:
            soup: BeautifulSoup object with parsed HTML

        Returns:
            Tuple of (header_row, data_rows)

        Raises:
            ValueError: If table not found or malformed
        """
        logger.info("Parsing H1B company table")

        table = soup.find('table', {'class': 'table'})
        if not table:
            raise ValueError("Could not find H1B company table on page")

        rows = table.find_all("tr")
        if not rows:
            raise ValueError("No table rows found")

        # Extract header
        header = [cell.get_text(strip=True) for cell in rows[0].find_all("th")]

        # Extract data rows (skip header row)
        data = [
            [cell.get_text(strip=True) for cell in row.find_all("td")]
            for row in rows[1:]
            if row.find_all("td")  # Skip empty rows
        ]

        logger.info(f"✓ Parsed {len(data)} companies with {len(header)} columns")
        return header, data

    def scrape(self) -> tuple[List[str], List[List[str]]]:
        """
        Scrape H1B company data from the web.

        Returns:
            Tuple of (header, data_rows)
        """
        soup = self.fetch_page()
        return self.parse_table(soup)

    def save_to_csv(
        self,
        output_path: str = "companies.csv",
        include_header: bool = True
    ) -> Path:
        """
        Scrape H1B data and save to CSV file.

        Args:
            output_path: Path for output CSV file
            include_header: Whether to include header row

        Returns:
            Path to the created CSV file

        Example:
            >>> scraper = H1BCompanyScraper()
            >>> csv_path = scraper.save_to_csv("h1b_companies.csv")
            >>> print(f"Data saved to: {csv_path}")
        """
        header, data = self.scrape()

        output = Path(output_path)
        logger.info(f"Saving data to: {output}")

        with open(output, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Write header if requested
            if include_header:
                writer.writerow(header)

            # Write data rows
            writer.writerows(data)

        logger.info(f"✓ Successfully saved {len(data)} companies to {output}")
        return output


def main():
    """
    Main function to scrape H1B companies and save to CSV.

    This function creates a scraper instance, fetches H1B company data,
    and saves it to a CSV file for further analysis.
    """
    print("=== H1B Company Scraper ===\n")

    try:
        scraper = H1BCompanyScraper()
        output_file = scraper.save_to_csv("companies.csv")

        print(f"✓ H1B company data saved to: {output_file}")
        print(f"  Use this data to identify companies sponsoring H1B visas.")

    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        print(f"\n⚠️  Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
