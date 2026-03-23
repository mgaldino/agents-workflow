#!/usr/bin/env python3
"""
Download tariff-related replication datasets from Harvard Dataverse.

Harvard Dataverse provides a REST API for accessing and downloading datasets.
This script downloads specific replication packages that contain tariff data
relevant to OECD trade research.

Usage:
    pip install requests pandas
    python download_harvard_dataverse.py

Output:
    harvard_dataverse_downloads/ (directory with downloaded files)

API Documentation:
    https://guides.dataverse.org/en/latest/api/
"""

import requests
import os
import json
import time

# Harvard Dataverse API
DATAVERSE_API = "https://dataverse.harvard.edu/api"

# Datasets with tariff/trade data that may cover OECD countries 2000-2010
DATASETS = [
    {
        "name": "Tariff Passthrough at the Border and at the Store",
        "doi": "doi:10.7910/DVN/JV7FCH",
        "description": "US tariff passthrough micro data. May contain OECD partner tariff data.",
    },
    {
        "name": "Trade Policy and Global Sourcing: A Rationale for Tariff Escalation",
        "doi": "doi:10.7910/DVN/10RLRZ",
        "description": "Cross-country tariff escalation data.",
    },
    {
        "name": "The Environmental Bias of Trade Policy",
        "doi": "doi:10.7910/DVN/CTUS2E",
        "description": "Cross-country trade policy data including tariff measures.",
    },
    {
        "name": "Economic Crises and Trade Policy Competition",
        "doi": "doi:10.7910/DVN/SVWMB5",
        "description": "Trade policy competition data across countries.",
    },
    {
        "name": "Asset Specificity, Corporate Protection and Trade Policy",
        "doi": "doi:10.7910/DVN/1WZRY2",
        "description": "Firm-level evidence from antidumping petitions in 19 jurisdictions.",
    },
]


def search_dataverse(query: str, dataverse: str = "harvard") -> dict:
    """
    Search Harvard Dataverse for datasets matching a query.

    Parameters
    ----------
    query : str
        Search terms
    dataverse : str
        Dataverse to search within (default: 'harvard')

    Returns
    -------
    dict
        API response with search results
    """
    url = f"{DATAVERSE_API}/search"
    params = {
        "q": query,
        "type": "dataset",
        "per_page": 20,
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def get_dataset_metadata(doi: str) -> dict:
    """
    Get metadata for a specific dataset by DOI.

    Parameters
    ----------
    doi : str
        Persistent identifier (e.g., 'doi:10.7910/DVN/JV7FCH')

    Returns
    -------
    dict
        Dataset metadata including file listings
    """
    url = f"{DATAVERSE_API}/datasets/:persistentId/"
    params = {"persistentId": doi}
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def list_dataset_files(doi: str) -> list:
    """
    List all files in a dataset.

    Parameters
    ----------
    doi : str
        Persistent identifier

    Returns
    -------
    list
        List of file metadata dicts
    """
    url = f"{DATAVERSE_API}/datasets/:persistentId/versions/:latest/files"
    params = {"persistentId": doi}
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data.get("data", [])


def download_file(file_id: int, output_path: str):
    """
    Download a specific file from Harvard Dataverse by file ID.

    Parameters
    ----------
    file_id : int
        Dataverse file ID
    output_path : str
        Local path to save the file
    """
    url = f"{DATAVERSE_API}/access/datafile/{file_id}"
    response = requests.get(url, stream=True, timeout=120)
    response.raise_for_status()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"  Downloaded: {output_path} ({os.path.getsize(output_path)} bytes)")


def main():
    output_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "harvard_dataverse_downloads"
    )
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Search for tariff-related datasets
    print("=" * 60)
    print("Harvard Dataverse -- Tariff Data Search & Download")
    print("=" * 60)

    print("\n--- Step 1: Searching for tariff datasets ---")
    try:
        results = search_dataverse("tariff OECD trade protection")
        items = results.get("data", {}).get("items", [])
        print(f"Found {len(items)} datasets matching 'tariff OECD trade protection'")

        # Save search results
        search_path = os.path.join(output_dir, "search_results.json")
        with open(search_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Search results saved to {search_path}")

        for item in items[:10]:
            print(f"  - {item.get('name', 'N/A')}")
            print(f"    DOI: {item.get('global_id', 'N/A')}")
            print(f"    Published: {item.get('published_at', 'N/A')}")
            print()
    except Exception as e:
        print(f"Search failed: {e}")

    # Step 2: Inspect and download known datasets
    print("\n--- Step 2: Inspecting known tariff datasets ---")
    for dataset in DATASETS:
        print(f"\nDataset: {dataset['name']}")
        print(f"DOI: {dataset['doi']}")
        print(f"Description: {dataset['description']}")

        try:
            files = list_dataset_files(dataset["doi"])
            print(f"Files ({len(files)}):")

            for file_info in files:
                df = file_info.get("dataFile", {})
                filename = df.get("filename", "unknown")
                filesize = df.get("filesize", 0)
                file_id = df.get("id", None)
                content_type = df.get("contentType", "unknown")

                print(f"  - {filename} ({filesize/1024:.1f} KB, {content_type})")

                # Download CSV/TSV/Stata files (likely data files)
                data_extensions = (".csv", ".tsv", ".dta", ".xlsx", ".xls", ".rds", ".rda")
                if any(filename.lower().endswith(ext) for ext in data_extensions):
                    dataset_dir = os.path.join(
                        output_dir,
                        dataset["doi"].replace(":", "_").replace("/", "_")
                    )
                    file_path = os.path.join(dataset_dir, filename)
                    print(f"    -> Downloading data file...")
                    download_file(file_id, file_path)

        except Exception as e:
            print(f"  Error: {e}")

        time.sleep(2)

    print("\n--- Done ---")
    print(f"All downloads saved to: {output_dir}")


if __name__ == "__main__":
    main()
