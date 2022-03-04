import logging

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils import timezone


def _hello():
    logging.info("Hello")


default_args = {
    "owner": "zkan",
    "start_date": timezone.datetime(2022, 3, 1),
}
with DAG(
    "demo_scheduling",
    default_args=default_args,
    schedule_interval="@daily",
) as dag:

    hello = PythonOperator(
        task_id="hello",
        python_callable=_hello,
    )
