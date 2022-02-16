import logging

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils import timezone


def _get_context(**context):
    logging.info(f"{context}")

    ds = context["ds"]
    data_interval_start = context["data_interval_start"]

    logging.info(f"ds: {ds}")
    logging.info(f"data_interval_start: {data_interval_start}")


default_args = {
    "owner": "zkan",
    "start_date": timezone.datetime(2022, 2, 1),
}
with DAG(
    "demo4",
    default_args=default_args,
    schedule_interval="@daily",
) as dag:

    get_context = PythonOperator(
        task_id="get_context",
        python_callable=_get_context,
    )
