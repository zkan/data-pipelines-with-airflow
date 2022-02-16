import logging

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils import timezone


def _push_values_to_xcom(**context):
    context["ti"].xcom_push(key="course", value="Airflow (from XCom push)")

    return "Airflow (from return)"


def _pull_values_from_xcom(**context):
    value1 = context["ti"].xcom_pull(task_ids="push_values_to_xcom", key="course")
    value2 = context["ti"].xcom_pull(task_ids="push_values_to_xcom", key="return_value")

    logging.info(f"value1: {value1}")
    logging.info(f"value2: {value2}")


default_args = {
    "owner": "zkan",
    "start_date": timezone.datetime(2022, 2, 1),
}
with DAG(
    "demo6",
    default_args=default_args,
    schedule_interval="@daily",
) as dag:

    push_values_to_xcom = PythonOperator(
        task_id="push_values_to_xcom",
        python_callable=_push_values_to_xcom,
    )

    pull_values_from_xcom = PythonOperator(
        task_id="pull_values_from_xcom",
        python_callable=_pull_values_from_xcom,
    )

    push_values_to_xcom >> pull_values_from_xcom
