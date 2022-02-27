import logging
from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils import timezone


def retry_callback(context):
    logging.info(f"{context}")
    logging.error("Cannot call API at this moment. Wait for retrying..")


def failure_callback(context):
    logging.info(f"{context}")
    logging.error("Cannot call API. Plase contact the admin.")


def _get_data_from_api():
    raise ValueError()


default_args = {
    "owner": "zkan",
    "email": ["kan@dataengineercafe.io"],
    "start_date": timezone.datetime(2022, 2, 1),
    "retries": 3,
    "retry_delay": timedelta(seconds=5),
    "on_retry_callback": retry_callback,
    "on_failure_callback": failure_callback,
}
with DAG(
    "demo_retry_and_alert",
    default_args=default_args,
    schedule_interval=None,
) as dag:

    get_data_from_api = PythonOperator(
        task_id="get_data_from_api",
        python_callable=_get_data_from_api,
    )