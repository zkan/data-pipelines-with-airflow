import logging

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils import timezone


# Connection Id: airflow_metastore
# Connection Type: postgres
# Host: postgres
# Schema: airflow
# Login: airflow
# Password: airflow
# Port: 5432


def _query_data():
    pg_hook = PostgresHook(
        postgres_conn_id="airflow_metastore",
        schema="airflow",
    )
    connection = pg_hook.get_conn()
    cursor = connection.cursor()

    sql = """
        SELECT dag_id, owners FROM dag
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    for each in rows:
        logging.info(each)


default_args = {
    "owner": "zkan",
    "start_date": timezone.datetime(2025, 5, 1),
}
with DAG(
    "demo_hooks",
    default_args=default_args,
    schedule=None,
):

    query_data = PythonOperator(
        task_id="query_data",
        python_callable=_query_data,
    )
