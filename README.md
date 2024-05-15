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
    git clone https://github.com/torogeldiiev/python.git
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
```

This is the sample requests:
```bash
http://127.0.0.1/versions?name=openssl
http://127.0.0.1/versions?name=xz-utils
http://127.0.0.1/versions?name=sudo
```

