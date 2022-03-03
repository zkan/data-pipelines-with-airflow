import logging

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils import timezone


def _hello():
    logging.info("Hello")


def _world():
    logging.info("World")


default_args = {
    "owner": "zkan",
    "start_date": timezone.datetime(2022, 2, 1),
}
with DAG(
    "demo_dependencies",
    default_args=default_args,
    schedule_interval=None,
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
