
# GitHub History Generator

This project is a Python script that generates a commit history pattern for a GitHub repository. It includes functionalities to create commits in random patterns or display custom text in the contribution graph.

## Features

- Generate random commit patterns for specific date ranges.
- Create text patterns in the contribution graph using fixed commit patterns.
- Supports custom configurations like workdays-only commits and average commits per day.
- Automatically initializes and configures a GitHub repository for commit history creation.

## Requirements

- Python 3.x
- Git installed and available in the system PATH

## Installation

1. Clone the repository or download the script.
2. Ensure Python 3.x and Git are installed on your system.

## Usage

Run the script with the following command:

```bash
python3 main.py --gitName "<GitHub Name>" --gitEmail "<GitHub Email>" [options]
```

### Options

- `--commitsPerDay` (float): Average number of commits per day (default: `0.3`).
- `--workdaysOnly`: Only create commits on workdays.
- `--startDate` (string): Start date for the commits (format: `YYYY-MM-DD`).
- `--endDate` (string): End date for the commits (format: `YYYY-MM-DD`).
- `--text` (string): Text to display in the GitHub contribution graph.
- `--year` (int): Year for the text display.
- `--gitName` (string): Git user name (required).
- `--gitEmail` (string): Git user email (required).

## Example

1. Generate random commits:

```bash
python3 main.py --gitName "Your Name" --gitEmail "your-email@example.com" --commitsPerDay 0.5 --startDate 2024-01-01 --endDate 2024-12-31
```

2. Create a text pattern:

```bash
python3 main.py --gitName "Your Name" --gitEmail "your-email@example.com" --text "HELLO" --year 2024
```

## Notes

- The script will create a repository named `my-history` in the current directory.
- Customize the script to change text patterns or commit intensities.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for suggestions or improvements.
