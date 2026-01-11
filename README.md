# Manisa MASKI Water Outage Scraper

Automated scraper for water outage information from Manisa Water and Sewerage Administration (MASKI).

## Data Source

**Official Website:** [https://www.manisasu.gov.tr/su_kesintileri](https://www.manisasu.gov.tr/su_kesintileri)

The scraper extracts water outage information published by MASKI and stores it in a structured JSON format.

## Data File

The scraped data is stored in **`data.json`** file with the following structure:

```json
{
  "count": 2,
  "data": [
    {
      "city": "Manisa",
      "district": "TURGUTLU",
      "neighborhoods": ["ATATÜRK", "CUMHURİYET"],
      "description": "Arıza Giderme Çalışması",
      "start": "10.01.2026 10:10",
      "end": "10.01.2026 12:34"
    }
  ]
}
```

### Data Fields

- **city**: City name (always "Manisa")
- **district**: District name
- **neighborhoods**: Array of affected neighborhood names
- **description**: Reason for the outage
- **start**: Start date and time (DD.MM.YYYY HH:MM format)
- **end**: End date and time (DD.MM.YYYY HH:MM format)

## Update Frequency

The scraper runs automatically **every hour** via GitHub Actions workflow.

- **Schedule**: Every hour at minute 0 (cron: `0 * * * *`)
- **Method**: GitHub Actions automated workflow
- **Manual Trigger**: Can also be triggered manually via workflow_dispatch

## Installation

### Requirements

- Python 3.10+
- Chrome/Chromium browser (for Selenium)

### Setup

1. Clone the repository:

```bash
git clone https://github.com/ramazansancar/manisa-maski-su-kesintisi.git
cd manisa-maski-su-kesintisi
```

1. Install dependencies:

```bash
pip install -r requirements.txt
```

### Dependencies

- `selenium==4.27.1` - Web scraping automation
- `beautifulsoup4==4.12.3` - HTML parsing
- `webdriver-manager==4.0.2` - Automatic ChromeDriver management

## Usage

### Run Manually

```bash
python scraper.py
```

This will:

1. Scrape the MASKI website
2. Parse the water outage information
3. Save the data to `data.json`
4. Display the number of records parsed

### Automated Updates

The repository is configured with GitHub Actions to automatically:

- Run the scraper every hour
- Update `data.json` if changes are detected
- Commit and push the changes

## Technical Details

### Scraper Functions

- **`get_outages()`**: Main function that scrapes the website and returns parsed data
- **`parse_location(text)`**: Parses district and neighborhood information
- **`parse_dates(text)`**: Parses start and end datetime information

### Browser Configuration

The scraper runs in headless mode with optimized settings:

- Headless Chrome
- Images disabled for faster loading
- GPU acceleration disabled

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Disclaimer

This is an unofficial scraper. All data belongs to Manisa Water and Sewerage Administration (MASKI). This tool is provided for informational purposes only.
