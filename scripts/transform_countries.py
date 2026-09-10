import json
import os
import sys

from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.storage.minio_client import upload_json
from src.transformation.countries_transformer import transform_countries


RAW_PATH = PROJECT_ROOT / "data" / "countries_raw.json"
OUTPUT_PATH = PROJECT_ROOT / "data" / "countries_cleaned.json"


def load_raw_countries():
    with RAW_PATH.open("r", encoding="utf-8") as file:
        raw_payload = json.load(file)

    countries = raw_payload.get("countries", [])

    if not countries:
        raise ValueError(
            "No country records were found in the raw dataset."
        )

    print(f"Loaded {len(countries)} raw country records.")

    return countries


def validate_cleaned_countries(countries):
    if not countries:
        raise ValueError("The transformed dataset is empty.")

    missing_names = [
        country
        for country in countries
        if not country.get("country_name")
    ]

    if missing_names:
        raise ValueError(
            f"{len(missing_names)} countries are missing country_name."
        )

    print(f"Validated {len(countries)} cleaned country records.")


def build_cleaned_payload(countries):
    return {
        "processed_at_utc": datetime.now(timezone.utc).isoformat(),
        "record_count": len(countries),
        "countries": countries,
    }


def save_cleaned_countries_locally(cleaned_payload):
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(
            cleaned_payload,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"Saved {cleaned_payload['record_count']} cleaned records locally:"
    )
    print(OUTPUT_PATH)


def save_cleaned_countries_to_minio(cleaned_payload):
    bucket_name = os.getenv("MINIO_SILVER_BUCKET")

    if not bucket_name:
        raise ValueError(
            "MINIO_SILVER_BUCKET was not found in .env"
        )

    now = datetime.now(timezone.utc)

    object_name = (
        f"countries/"
        f"year={now:%Y}/"
        f"month={now:%m}/"
        f"day={now:%d}/"
        f"countries_cleaned_{now:%Y%m%dT%H%M%SZ}.json"
    )

    upload_json(
        data=cleaned_payload,
        object_name=object_name,
        bucket_name=bucket_name,
    )

    print("Saved cleaned data to MinIO:")
    print(f"{bucket_name}/{object_name}")


def main():
    load_dotenv(PROJECT_ROOT / ".env")

    raw_countries = load_raw_countries()

    cleaned_countries = transform_countries(raw_countries)

    validate_cleaned_countries(cleaned_countries)

    cleaned_payload = build_cleaned_payload(cleaned_countries)

    save_cleaned_countries_locally(cleaned_payload)

    save_cleaned_countries_to_minio(cleaned_payload)


if __name__ == "__main__":
    main()