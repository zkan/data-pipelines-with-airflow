from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils import timezone


default_args = {
    "owner": "zkan",
    "start_date": timezone.datetime(2022, 2, 1),
}
with DAG(
    "demo_dag_trigger",
    default_args=default_args,
    schedule_interval=None,
) as dag:

    trigger = TriggerDagRunOperator(
        task_id="trigger",
        trigger_dag_id="demo_dag_target",
        conf={"message": "Hello World"},
    )