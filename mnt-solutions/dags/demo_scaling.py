import logging

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.utils import timezone


default_args = {
    "owner": "zkan",
    "start_date": timezone.datetime(2022, 2, 1),
}
with DAG(
    "demo_scaling",
    default_args=default_args,
    schedule_interval=None,
) as dag:

    t1 = DummyOperator(task_id="t1")
    t2 = DummyOperator(task_id="t2")
    t3 = DummyOperator(task_id="t3")
    t4 = DummyOperator(task_id="t4")
    t5 = DummyOperator(task_id="t5")

    t1 >> [t2, t3, t4] >> t5