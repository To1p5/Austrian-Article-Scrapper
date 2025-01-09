# Article Scraper for FEE.org and Mises.org

This project contains web scrapers for collecting recent articles from FEE.org and Mises.org. The scrapers collect articles from the last 60 days and save them to text files.

## Features

- Scrapes articles from FEE.org's archive page
- Scrapes articles from Mises.org's wire section
- Collects article titles and publication dates
- Handles pagination and infinite scroll
- Saves results in chronological order
- Uses Selenium for web automation

## Requirements

- Python 3.x
- Selenium WebDriver
- Chrome Browser
- Required Python packages (see requirements.txt)

## Installation

1. Clone this repository
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To scrape articles from FEE.org:
```bash
python fee_titles.py
```

To scrape articles from Mises.org:
```bash
python mises_titles.py
```

The results will be saved in `fee_recent_articles.txt` and `mises_recent_articles.txt` respectively.

## Output Format

The output files contain:
- Date range of collected articles
- List of articles with dates in YYYY-MM-DD format
- Articles sorted by date (newest first) 