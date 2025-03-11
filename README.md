# Google-Calendar-Analysis

## Description

Parser and visualization functions to search and analyze events containing specific keywords in their description from your Google Calendar.

## Usage

Enable Google Calendar API from the Google Cloud Console and create Credentials. The script expects a `client_secret.json` file at the root of this project.

Install Python 3.10 and Poetry 1.4.2.

```
# install dependencies
poetry install
# activate the Poetry environment
poetry shell
# parse your Google Calendar for specific events
python calendar_parser.py
# use the visualization functions to analyze your events patterns
jupyter lab
```