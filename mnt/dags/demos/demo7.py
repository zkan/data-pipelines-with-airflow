import logging

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils import timezone


def _push_values_to_xcom(**context):
    context["ti"].xcom_push(key="course", value="Airflow (from XCom push)")

    return "Airflow (from return)"


def _pull_values_from_xcom(**context):
    value1 = context["ti"].xcom_pull(task_ids="t1", key="course")
    value2 = context["ti"].xcom_pull(task_ids="t1", key="return_value")

    logging.info(f"value1: {value1}")
    logging.info(f"value2: {value2}")


default_args = {
    "owner": "zkan",
    "start_date": timezone.datetime(2022, 2, 1),
}
with DAG(
    "demo.demo7",
    default_args=default_args,
    schedule_interval="@daily",
) as dag:

    t1 = PythonOperator(
        task_id="t1",
        python_callable=_push_values_to_xcom,
    )

    t2 = PythonOperator(
        task_id="t2",
        python_callable=_pull_values_from_xcom,
    )

    t1 >> t2
