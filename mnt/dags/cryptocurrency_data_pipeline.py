import csv
import logging
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils import timezone

import ccxt
import pandas as pd


def _fetch_ohlcv(**context):
    ds = context["ds"]

    exchange = ccxt.binance()

    dt_obj = datetime.strptime(ds, "%Y-%m-%d")
    millisec = int(dt_obj.timestamp() * 1000)

    ohlcv = exchange.fetch_ohlcv("SHIB/USDT", timeframe="1h", since=millisec, limit=30)
    logging.info(ohlcv)

    with open("shib.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(ohlcv)

    s3_hook = S3Hook(aws_conn_id="minio")
    s3_hook.load_file(
        "shib.csv",
        key=f"cryptocurrency/{ds}/shib.csv",
        bucket_name="datalake",
        replace=True,
    )


def _download_file(**context):
    ds = context["ds"]

    s3_hook = S3Hook(aws_conn_id="minio")
    file_name = s3_hook.download_file(
        key=f"cryptocurrency/{ds}/shib.csv",
        bucket_name="datalake",
    )
    return file_name


# def _transform(**context):
#     file_name = context["ti"].xcom_pull(task_ids="download_file", key="return_value")
#     df = pd.read_csv(file_name, header=None)

#     with pd.option_context("display.precision", 10):
#         logging.info(df.info())
#         logging.info(df.head())


def _load_data_into_database(**context):
    postgres_hook = PostgresHook(postgres_conn_id="postgres")
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()

    file_name = context["ti"].xcom_pull(task_ids="download_file", key="return_value")
    # with open(file_name, "r") as f:
    #     cursor.copy_from(f, "cryptocurrency_import", sep=",")
    #     conn.commit()

    postgres_hook.copy_expert(
        """
            COPY
              cryptocurrency_import
            FROM STDIN DELIMITER ',' CSV
        """,
        file_name
    )


default_args = {
    "owner": "zkan",
    "start_date": timezone.datetime(2022, 1, 16),
    "retries": 3,
    "retry_delay": timedelta(minutes=3),
}
with DAG(
    "cryptocurrency_data_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
) as dag:
    start = DummyOperator(task_id="start")

    fetch_ohlcv = PythonOperator(
        task_id="fetch_ohlcv",
        python_callable=_fetch_ohlcv,
    )

    download_file = PythonOperator(
        task_id="download_file",
        python_callable=_download_file,
    )

    # transform = PythonOperator(
    #     task_id="transform",
    #     python_callable=_transform,
    # )

    create_import_table = PostgresOperator(
        task_id="create_import_table",
        postgres_conn_id="postgres",
        sql="""
            CREATE TABLE IF NOT EXISTS cryptocurrency_import (
              timestamp BIGINT,
              open FLOAT,
              highest FLOAT,
              lowest FLOAT,
              closing FLOAT,
              volume FLOAT
            )
        """,
    )

    load_data_into_database = PythonOperator(
        task_id="load_data_into_database",
        python_callable=_load_data_into_database,
    )

    create_final_table = PostgresOperator(
        task_id="create_final_table",
        postgres_conn_id="postgres",
        sql="""
            CREATE TABLE IF NOT EXISTS cryptocurrency (
              timestamp BIGINT PRIMARY KEY,
              open FLOAT,
              highest FLOAT,
              lowest FLOAT,
              closing FLOAT,
              volume FLOAT
            )
        """,
    )

    merge_import_into_final_table = PostgresOperator(
        task_id="merge_import_into_final_table",
        postgres_conn_id="postgres",
        sql="""
            INSERT INTO cryptocurrency (
              timestamp,
              open,
              highest,
              lowest,
              closing,
              volume
            )
            SELECT
              timestamp,
              open,
              highest,
              lowest,
              closing,
              volume
            FROM
              cryptocurrency_import
            ON CONFLICT (timestamp)
            DO UPDATE SET
              open = EXCLUDED.open,
              highest = EXCLUDED.highest,
              lowest = EXCLUDED.lowest,
              closing = EXCLUDED.closing,
              volume = EXCLUDED.volume
        """,
    )

    clear_import_table = PostgresOperator(
        task_id="clear_import_table",
        postgres_conn_id="postgres",
        sql="""
            DELETE FROM cryptocurrency_import
        """,
    )

    end = DummyOperator(task_id="end")

    # start >> fetch_ohlcv >> download_file >> transform >> create_import_table >> load_data_into_database >> create_final_table >> merge_import_into_final_table >> clear_import_table >> end
    start >> fetch_ohlcv >> download_file >> create_import_table >> load_data_into_database >> create_final_table >> merge_import_into_final_table >> clear_import_table >> end
