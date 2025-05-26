import csv
import logging

from datetime import datetime

from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook

import ccxt


def _fetch_ohlcv(**context):
    ds = context["ds"]

    # Choose Binance exchange
    exchange = ccxt.binance()

    # Fetch data from exchange
    dt_obj = datetime.strptime(ds, "%Y-%m-%d")
    millisec = int(dt_obj.timestamp() * 1000)
    ohlcv = exchange.fetch_ohlcv("SHIB/USDT", timeframe="1h", since=millisec, limit=24)
    logging.info(f"OHLCV of SHIB/USDT value. [ohlcv={ohlcv}]")

    # Write OHLCV data to CSV file
    with open(f"shib-{ds}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(ohlcv)

    # Store CSV file in S3
    s3_hook = S3Hook(aws_conn_id="minio")
    s3_hook.load_file(
        f"shib-{ds}.csv",
        key=f"cryptocurrency/{ds}/shib.csv",
        bucket_name="datalake",
        replace=True,
    )


def _download_file(**context):
    ds = context["ds"]

    # Download file from S3
    s3_hook = S3Hook(aws_conn_id="minio")
    file_name = s3_hook.download_file(
        key=f"cryptocurrency/{ds}/shib.csv",
        bucket_name="datalake",
    )

    return file_name


def _load_data_into_database(**context):
    postgres_hook = PostgresHook(postgres_conn_id="postgres")
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()

    # Get file name from XComs
    file_name = context["ti"].xcom_pull(task_ids="download_file", key="return_value")

    # Copy file to database
    postgres_hook.copy_expert(
        """
            COPY
                cryptocurrency_import
            FROM STDIN DELIMITER ',' CSV
        """,
        file_name,
    )
