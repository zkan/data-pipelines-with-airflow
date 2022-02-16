from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils import timezone


default_args = {
    "owner": "zkan",
    "start_date": timezone.datetime(2022, 2, 1),
}
with DAG(
    "demo5",
    default_args=default_args,
    schedule_interval="@daily",
) as dag:

    t1 = BashOperator(
        task_id="t1",
        bash_command="echo {{ ds }}",
    )

    t2 = BashOperator(
        task_id="t2",
        bash_command="echo {{ 1 + 1 }}",
    )

    t3 = BashOperator(
        task_id="t3",
        bash_command="echo {{ data_interval_start }}",
    )

    t4 = BashOperator(
        task_id="t4",
        bash_command="echo {{ data_interval_start | ds }}",
    )

    t5 = BashOperator(
        task_id="t5",
        bash_command="echo {{ macros.ds_add('2022-02-01', 10) }}",
    )

    t6 = BashOperator(
        task_id="t6",
        bash_command="echo {{ macros.ds_format('2022-02-01', '%Y-%m-%d', '%b %d, %Y') }}",
    )