import json
import os
import sys

from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.storage.minio_client import upload_json


BASE_URL = "https://api.restcountries.com/countries/v5"
PAGE_SIZE = 100

OUTPUT_PATH = PROJECT_ROOT / "data" / "countries_raw.json"

RESPONSE_FIELDS = [
    "uuid",
    "names.common",
    "names.official",
    "codes.alpha_2",
    "codes.alpha_3",
    "capitals",
    "region",
    "subregion",
    "continents",
    "population",
    "area",
    "coordinates",
    "landlocked",
    "currencies",
    "languages",
    "timezones",
    "borders",
    "calling_codes",
    "tlds",
    "flag.emoji",
    "flag.url_png",
    "flag.url_svg",
    "cars.driving_side",
    "government_type",
    "classification.sovereign",
    "classification.dependency",
    "classification.disputed",
    "classification.un_member",
    "_meta.lastUpdatedTimestamp",
]


def extract_countries(api_key):
    all_countries = []
    offset = 0

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    while True:
        params = {
            "limit": PAGE_SIZE,
            "offset": offset,
            "response_fields": ",".join(RESPONSE_FIELDS),
        }

        response = requests.get(
            BASE_URL,
            headers=headers,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        response_body = response.json()
        data = response_body.get("data", {})

        countries = data.get("objects", [])
        metadata = data.get("meta", {})

        all_countries.extend(countries)

        print(
            f"Fetched {len(countries)} records "
            f"from offset {offset}"
        )

        if not metadata.get("more"):
            break

        if not countries:
            raise RuntimeError(
                "The API reported another page but returned no records."
            )

        offset += len(countries)

    return all_countries


def build_raw_payload(countries):
    return {
        "extracted_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": BASE_URL,
        "record_count": len(countries),
        "countries": countries,
    }


def save_countries_locally(raw_payload):
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(
            raw_payload,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(f"\nSaved {raw_payload['record_count']} records locally:")
    print(OUTPUT_PATH)


def save_countries_to_minio(raw_payload):
    now = datetime.now(timezone.utc)

    object_name = (
        f"countries/"
        f"year={now:%Y}/"
        f"month={now:%m}/"
        f"day={now:%d}/"
        f"countries_raw_{now:%Y%m%dT%H%M%SZ}.json"
    )

    upload_json(
        data=raw_payload,
        object_name=object_name,
    )

    print("Saved raw data to MinIO:")
    print(object_name)


def main():
    load_dotenv(PROJECT_ROOT / ".env")

    api_key = os.getenv("REST_COUNTRIES_API_KEY")

    if not api_key:
        raise ValueError(
            "REST_COUNTRIES_API_KEY was not found in .env"
        )

    countries = extract_countries(api_key)

    raw_payload = build_raw_payload(countries)

    save_countries_locally(raw_payload)
    save_countries_to_minio(raw_payload)


if __name__ == "__main__":
    main()