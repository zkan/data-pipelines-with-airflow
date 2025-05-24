import time
from datetime import timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils import timezone


def _sleep():
    time.sleep(3)


default_args = {
    "owner": "zkan",
    "email": ["kan@dataengineercafe.io"],
    "start_date": timezone.datetime(2025, 5, 1),
    "sla": timedelta(seconds=5),
}
with DAG(
    "demo_sla",
    default_args=default_args,
    schedule="*/5 * * * *",
    catchup=False,
):

    t1 = PythonOperator(
        task_id="t1",
        python_callable=_sleep,
    )

    t2 = PythonOperator(
        task_id="t2",
        python_callable=_sleep,
        # sla=timedelta(seconds=30),
    )

    t1 >> t2
