import logging

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sdk import Variable
from airflow.utils import timezone


def _get_var():
    foo = Variable.get("foo", default=None)
    logging.info(foo)

    bar = Variable.get("bar", deserialize_json=True, default=None)
    logging.info(bar)


default_args = {
    "owner": "zkan",
    "start_date": timezone.datetime(2025, 5, 1),
}
with DAG(
    "demo_variables",
    default_args=default_args,
    schedule=None,
):

    get_var = PythonOperator(
        task_id="get_var",
        python_callable=_get_var,
    )
