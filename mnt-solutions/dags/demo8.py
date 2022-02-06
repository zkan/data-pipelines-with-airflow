import logging

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.utils import timezone


def _get_var():
    foo = Variable.get("foo", default_var=None)
    logging.info(foo)

    bar = Variable.get("bar", deserialize_json=True, default_var=None)
    logging.info(bar)


default_args = {
    "owner": "zkan",
    "start_date": timezone.datetime(2022, 2, 1),
}
with DAG(
    "demo8",
    default_args=default_args,
    schedule_interval="@daily",
) as dag:

    get_var = PythonOperator(
        task_id="get_var",
        python_callable=_get_var,
    )
