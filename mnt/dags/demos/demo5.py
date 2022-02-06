import logging

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils import timezone


def _get_context(**context):
    ds = context["ds"]
    prev_ds = context["prev_ds"]

    logging.info(f"ds: {ds}")
    logging.info(f"prev_ds: {prev_ds}")


default_args = {
    "owner": "zkan",
    "start_date": timezone.datetime(2022, 2, 1),
}
with DAG(
    "demo.demo5",
    default_args=default_args,
    schedule_interval="@daily",
) as dag:

    t1 = PythonOperator(
        task_id="t1",
        python_callable=_get_context,
    )
