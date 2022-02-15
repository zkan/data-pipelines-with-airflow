import logging

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils import timezone


def _hello():
    logging.info("Hello")


def _world(**context):
    logging.info(f"{context}")

    ds = context["ds"]
    logging.info(f"World on {ds}")


default_args = {
    "owner": "zkan",
    "start_date": timezone.datetime(2022, 2, 1),
}
with DAG(
    "demo4",
    default_args=default_args,
    schedule_interval="@daily",
) as dag:

    hello = PythonOperator(
        task_id="hello",
        python_callable=_hello,
    )

    world = PythonOperator(
        task_id="world",
        python_callable=_world,
    )

    hello >> world
