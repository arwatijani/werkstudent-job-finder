# Werkstudent Job Finder

A Python script that finds IT working-student (Werkstudent) jobs in Germany using the free Arbeitnow API.

## Features

- Fetches job listings from the Arbeitnow API (5 pages)
- Keeps only Werkstudent jobs in Darmstadt, Frankfurt, Mainz, Mannheim or remote
- Keeps only IT-related jobs (software, data, Python, Java...)
- Removes duplicate listings
- Prints the results and saves them to a CSV file

## Technologies

- Python 3
- requests (HTTP requests to a REST API)
- csv and time (standard library)

## How to run

    pip install requests
    python3 jobs.py

## Example output

    Found 3 matching jobs

    Werkstudent*in Data Analytics (m/w/d) - ZDF Digital Medienproduktion GmbH (Mainz oder Berlin)
    https://www.arbeitnow.com/jobs/companies/...

## Possible improvements

- Send an e-mail when a new job appears
- Let the user choose keywords and cities from the command line
- Add more job sources
