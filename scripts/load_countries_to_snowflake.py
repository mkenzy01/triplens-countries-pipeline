import json
import sys

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.storage.snowflake_client import get_snowflake_connection


CLEANED_PATH = PROJECT_ROOT / "data" / "countries_cleaned.json"


def load_cleaned_countries():
    with CLEANED_PATH.open("r", encoding="utf-8") as file:
        payload = json.load(file)

    countries = payload.get("countries", [])

    if not countries:
        raise ValueError(
            "No cleaned country records were found."
        )

    print(f"Loaded {len(countries)} cleaned records.")

    return countries


def prepare_row(country):
    return (
        country.get("uuid"),
        country.get("country_name"),
        country.get("official_name"),
        country.get("alpha_2"),
        country.get("alpha_3"),
        country.get("capital"),
        country.get("capital_latitude"),
        country.get("capital_longitude"),
        country.get("region"),
        country.get("subregion"),

        json.dumps(country.get("continents") or []),

        country.get("population"),
        country.get("area_km2"),
        country.get("area_miles2"),
        country.get("latitude"),
        country.get("longitude"),
        country.get("landlocked"),

        json.dumps(country.get("currencies") or []),
        json.dumps(country.get("languages") or []),
        json.dumps(country.get("timezones") or []),
        json.dumps(country.get("borders") or []),
        json.dumps(country.get("calling_codes") or []),
        json.dumps(country.get("tlds") or []),

        country.get("flag_emoji"),
        country.get("flag_png"),
        country.get("flag_svg"),
        country.get("driving_side"),
        country.get("government_type"),
        country.get("is_sovereign"),
        country.get("is_dependency"),
        country.get("is_disputed"),
        country.get("is_un_member"),
    )


def load_to_snowflake(countries):
    connection = get_snowflake_connection()
    cursor = connection.cursor()

    insert_sql = """
        INSERT INTO COUNTRIES (
            UUID,
            COUNTRY_NAME,
            OFFICIAL_NAME,
            ALPHA_2,
            ALPHA_3,
            CAPITAL,
            CAPITAL_LATITUDE,
            CAPITAL_LONGITUDE,
            REGION,
            SUBREGION,
            CONTINENTS,
            POPULATION,
            AREA_KM2,
            AREA_MILES2,
            LATITUDE,
            LONGITUDE,
            LANDLOCKED,
            CURRENCIES,
            LANGUAGES,
            TIMEZONES,
            BORDERS,
            CALLING_CODES,
            TLDS,
            FLAG_EMOJI,
            FLAG_PNG,
            FLAG_SVG,
            DRIVING_SIDE,
            GOVERNMENT_TYPE,
            IS_SOVEREIGN,
            IS_DEPENDENCY,
            IS_DISPUTED,
            IS_UN_MEMBER
        )
        SELECT
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            PARSE_JSON(%s),
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            PARSE_JSON(%s),
            PARSE_JSON(%s),
            PARSE_JSON(%s),
            PARSE_JSON(%s),
            PARSE_JSON(%s),
            PARSE_JSON(%s),
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
    """

    try:
        # Prevent duplicate rows when rerunning the loader.
        cursor.execute("TRUNCATE TABLE COUNTRIES")

        rows = [
            prepare_row(country)
            for country in countries
        ]

        for row in rows:
            cursor.execute(
                insert_sql,
                row,
        )

        connection.commit()

        print(
            f"Successfully loaded {len(rows)} countries "
            "into Snowflake."
        )

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def main():
    countries = load_cleaned_countries()
    load_to_snowflake(countries)


if __name__ == "__main__":
    main()