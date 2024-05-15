# Vulnerability Checker

## Description

This project is a REST API service that provides information about vulnerable package versions.

## Features

- Fetches vulnerability data from the OSV (Open Source Vulnerabilities) database
- Aggregates affected versions from Debian and Ubuntu ecosystems
- Provides a list of unique affected versions for a given package
- Returns the result as a JSON response

## Installation

1. Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2. Install the required packages using pip:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the application, execute the following command:
```bash
uvicorn main:app --host 0.0.0.0 --port 80
