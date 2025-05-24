from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.utils import timezone
from airflow.utils.task_group import TaskGroup


default_args = {
    "owner": "zkan",
    "start_date": timezone.datetime(2025, 5, 1),
}
with DAG(
    "demo_task_group",
    default_args=default_args,
    schedule=None,
):

    start = EmptyOperator(task_id="start")

    with TaskGroup(group_id="my_group") as my_group:
        t1 = EmptyOperator(task_id="t1")
        t2 = EmptyOperator(task_id="t2")

        t1 >> t2

    end = EmptyOperator(task_id="end")

    start >> my_group >> end
