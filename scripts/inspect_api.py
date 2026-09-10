import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


BASE_URL = "https://api.restcountries.com/countries/v5"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = PROJECT_ROOT / "data" / "sample_response.json"


def main():
    load_dotenv(PROJECT_ROOT / ".env")

    api_key = os.getenv("REST_COUNTRIES_API_KEY")

    if not api_key:
        raise ValueError(
            "REST_COUNTRIES_API_KEY was not found in the .env file."
        )

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    params = {
        "limit": 3,
        "offset": 0
    }

    response = requests.get(
        BASE_URL,
        headers=headers,
        params=params,
        timeout=30
    )

    response.raise_for_status()
    response_body = response.json()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(
            response_body,
            file,
            indent=2,
            ensure_ascii=False
        )

    data = response_body.get("data", {})
    countries = data.get("objects", [])
    metadata = data.get("meta", {})

    print(f"Request status: {response.status_code}")
    print(f"Countries returned: {len(countries)}")
    print(f"Total countries available: {metadata.get('total')}")
    print(f"More pages available: {metadata.get('more')}")
    print(f"Response saved to: {OUTPUT_PATH}")

    if countries:
        first_country = countries[0]

        print("\nFirst country:")
        print(f"Name: {first_country.get('names', {}).get('common')}")
        print(f"Top-level fields: {sorted(first_country.keys())}")


if __name__ == "__main__":
    main()