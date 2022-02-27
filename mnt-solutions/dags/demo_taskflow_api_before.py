import logging

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils import timezone


def _extract():
    return [
        {
            "name": "Kan",
            "salary": 30000,
        },
        {
            "name": "John",
            "salary": 25000,
        },
    ]

def _transform(ti):
    salary_data = ti.xcom_pull(task_ids="extract", key="return_value")

    total = 0

    for each in salary_data:
        total += each["salary"]

    return total


def _load(ti):
    total_salary = ti.xcom_pull(task_ids="transform", key="return_value")

    logging.info(f"Total salary is: {total_salary}")


default_args = {
    "owner": "zkan",
    "start_date": timezone.datetime(2022, 2, 1),
}
with DAG(
    "demo_taskflow_api_before",
    default_args=default_args,
    schedule_interval=None,
) as dag:

    extract = PythonOperator(
        task_id="extract",
        python_callable=_extract,
    )

    transform = PythonOperator(
        task_id="transform",
        python_callable=_transform,
    )

    load = PythonOperator(
        task_id="load",
        python_callable=_load,
    )

    extract >> transform >> load