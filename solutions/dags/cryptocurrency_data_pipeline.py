from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.smtp.operators.smtp import EmailOperator
from airflow.utils import timezone

from etl import (
    _fetch_ohlcv,
    _download_file,
    _load_data_into_database,
)


default_args = {
    "owner": "zkan",
    "start_date": timezone.datetime(2025, 5, 23),
}
with DAG(
    "cryptocurrency_data_pipeline",
    default_args=default_args,
    schedule=None,
):

    fetch_ohlcv = EmptyOperator(
        task_id="fetch_ohlcv",
    )

    download_file = EmptyOperator(
        task_id="download_file",
    )

    create_import_table = EmptyOperator(
        task_id="create_import_table",
    )

    load_data_into_database = EmptyOperator(
        task_id="load_data_into_database",
    )

    create_final_table = EmptyOperator(
        task_id="create_final_table",
    )

    merge_import_into_final_table = EmptyOperator(
        task_id="merge_import_into_final_table",
    )

    clear_import_table = EmptyOperator(
        task_id="clear_import_table",
    )

    notify = EmptyOperator(
        task_id="notify",
    )
