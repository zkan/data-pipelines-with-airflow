import logging

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils import timezone


default_args = {
    "owner": "zkan",
    "start_date": timezone.datetime(2025, 5, 1),
}
with DAG(
    "demo_scaling",
    default_args=default_args,
    schedule=None,
):

    t1 = BashOperator(
        task_id="t1",
        bash_command="echo 't1'",
    )
    t2 = BashOperator(
        task_id="t2",
        bash_command="echo 't2'",
    )
    t3 = BashOperator(
        task_id="t3",
        bash_command="echo 't3'",
    )
    t4 = BashOperator(
        task_id="t4",
        bash_command="echo 't4'",
    )
    t5 = BashOperator(
        task_id="t5",
        bash_command="echo 't5'",
    )

    t1 >> [t2, t3, t4] >> t5
