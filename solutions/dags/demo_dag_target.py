import logging

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils import timezone


def _run_this(**context):
    dag_run = context["dag_run"]
    logging.info(f"Remotely received value: {dag_run.conf.get('message')}")


default_args = {
    "owner": "zkan",
    "start_date": timezone.datetime(2022, 2, 1),
}
with DAG(
    "demo_dag_target",
    default_args=default_args,
    schedule_interval=None,
) as dag:

    run_this = PythonOperator(
        task_id="run_this",
        python_callable=_run_this,
    )
