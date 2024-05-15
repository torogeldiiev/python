import requests
import logging
from concurrent.futures import ThreadPoolExecutor
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_versions_debian(package_name):
    query = {
        "package": {
            "name": package_name,
            "ecosystem": "Debian"
        }
    }
    logger.info(f"Fetching versions for package {package_name} from Debian ecosystem.")
    response = requests.post("https://api.osv.dev/v1/query", json=query)
    if response.status_code == 200:
        data = response.json()
        affected_versions = []
        for vuln in data.get('vulns', []):
            for affected in vuln.get('affected', []):
                if 'ranges' in affected:  # For Debian
                    for range_data in affected['ranges']:
                        if 'events' in range_data:
                            for event in range_data['events']:
                                if 'fixed' in event:
                                    affected_versions.append(event['fixed'])
                elif 'binaries' in affected['ecosystem_specific']:  # For Ubuntu
                    for binary, version in affected['ecosystem_specific']['binaries'][0].items():
                        affected_versions.append(version)
        logger.info(f"Fetched versions for package {package_name} from Debian ecosystem")
        return affected_versions
    else:
        error_message = f"Failed to fetch vulnerability data for package {package_name} from Debian ecosystem. Actual error: {response.text}"
        logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)


def fetch_versions_ubuntu(package_name):
    query = {
        "package": {
            "name": package_name,
            "ecosystem": "Ubuntu"
        }
    }
    logger.info(f"Fetching versions for package {package_name} from Ubuntu ecosystem.")
    response = requests.post("https://api.osv.dev/v1/query", json=query)
    if response.status_code == 200:
        data = response.json()
        affected_versions = []
        for vuln in data.get('vulns', []):
            for affected in vuln.get('affected', []):
                if 'binaries' in affected['ecosystem_specific']:
                    for binary, version in affected['ecosystem_specific']['binaries'][0].items():
                        affected_versions.append(version)
        logger.info(f"Fetched versions for package {package_name} from Ubuntu ecosystem")
        return affected_versions
    else:
        error_message = f"Failed to fetch vulnerability data for package {package_name} from Ubuntu ecosystem. Actual error: {response.text}"
        logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)


def get_package_versions(package_name):
    with ThreadPoolExecutor(max_workers=2) as executor:
        debian_future = executor.submit(fetch_versions_debian, package_name)
        ubuntu_future = executor.submit(fetch_versions_ubuntu, package_name)

        debian_versions = debian_future.result()
        ubuntu_versions = ubuntu_future.result()

    unique_versions = sorted(set(debian_versions + ubuntu_versions))
    return unique_versions
