import logging

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils import timezone


def _greeting(greeting, name):
    logging.info(f"{greeting}, {name}")


default_args = {
    "owner": "zkan",
    "start_date": timezone.datetime(2025, 5, 1),
}
with DAG(
    "demo_custom_operator",
    default_args=default_args,
    schedule=None,
):

    greeting1 = PythonOperator(
        task_id="greeting1",
        python_callable=_greeting,
        op_kwargs={
            "greeting": "Hello",
            "name": "World"
        },
    )

    greeting2 = PythonOperator(
        task_id="greeting2",
        python_callable=_greeting,
        op_kwargs={
            "greeting": "Hey",
            "name": "Skooldio"
        },
    )

    greeting1 >> greeting2