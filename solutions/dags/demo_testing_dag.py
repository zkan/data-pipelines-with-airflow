import logging
from datetime import timedelta

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
    "retries": 3,
    "retry_delay": timedelta(minutes=3),
}
with DAG(
    "demo_testing_dag",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
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
