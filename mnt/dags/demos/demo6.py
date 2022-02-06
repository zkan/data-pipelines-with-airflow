from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils import timezone


default_args = {
    "owner": "zkan",
    "start_date": timezone.datetime(2022, 2, 1),
}
with DAG(
    "demo.demo6",
    default_args=default_args,
    schedule_interval="@daily",
) as dag:

    t1 = BashOperator(
        task_id="t1",
        bash_command="echo {{ ds }}",
    )
