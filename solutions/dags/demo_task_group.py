from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.utils import timezone
from airflow.utils.task_group import TaskGroup


default_args = {
    "owner": "zkan",
    "start_date": timezone.datetime(2022, 2, 1),
}
with DAG(
    "demo_task_group",
    default_args=default_args,
    schedule_interval=None,
) as dag:

    start = DummyOperator(task_id="start")

    with TaskGroup(group_id="my_group") as my_group:
        t1 = DummyOperator(task_id="t1")
        t2 = DummyOperator(task_id="t2")

        t1 >> t2

    end = DummyOperator(task_id="end")

    start >> my_group >> end