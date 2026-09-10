import sys

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.storage.snowflake_client import get_snowflake_connection


connection = get_snowflake_connection()

cursor = connection.cursor()

try:
    cursor.execute("SELECT CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_WAREHOUSE()")

    result = cursor.fetchone()

    print("Connected to Snowflake successfully.")
    print(f"Database: {result[0]}")
    print(f"Schema: {result[1]}")
    print(f"Warehouse: {result[2]}")

finally:
    cursor.close()
    connection.close()