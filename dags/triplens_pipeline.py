from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="triplens_pipeline",
    start_date=datetime(2026, 9, 7),
    schedule="@weekly",
    catchup=False,
    tags=["triplens"],
) as dag:

    extract_countries = BashOperator(
    task_id="extract_countries",
    bash_command=(
        "MINIO_ENDPOINT=host.docker.internal:9000 "
        "python /usr/local/airflow/scripts/extract_countries.py"
    ),
    )

    transform_countries = BashOperator(
    task_id="transform_countries",
    bash_command=(
        "MINIO_ENDPOINT=host.docker.internal:9000 "
        "python /usr/local/airflow/scripts/transform_countries.py"
    ),
    )

    load_to_snowflake = BashOperator(
        task_id="load_to_snowflake",
        bash_command="python /usr/local/airflow/scripts/load_countries_to_snowflake.py",
    )

    dbt_run = BashOperator(
    task_id="dbt_run",
    bash_command=(
        "cd /usr/local/airflow/include/dbt/triplens_dbt && "
        "dbt run --profiles-dir ."
    ),
    )

    dbt_test = BashOperator(
    task_id="dbt_test",
    bash_command=(
        "cd /usr/local/airflow/include/dbt/triplens_dbt && "
        "dbt test --profiles-dir ."
    ),
    )

    (
        extract_countries
        >> transform_countries
        >> load_to_snowflake
        >> dbt_run
        >> dbt_test
    )