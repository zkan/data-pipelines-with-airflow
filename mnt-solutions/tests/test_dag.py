from airflow import DAG
from airflow.utils.dag_cycle_tester import check_cycle

from my_second_dag import dag as my_second_dag_instance


def test_another_dag_integrity():
    assert isinstance(my_second_dag_instance, DAG)
    check_cycle(my_second_dag_instance)