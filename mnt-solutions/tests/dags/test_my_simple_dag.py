from datetime import timedelta

from airflow import DAG
from airflow.utils.dag_cycle_tester import check_cycle

from my_simple_dag import dag as my_simple_dag_instance
from my_second_dag import dag as my_second_dag_instance


def test_dag_integrity():
    assert isinstance(my_simple_dag_instance, DAG)
    check_cycle(my_simple_dag_instance)
    print(dir(my_simple_dag_instance))
    print(my_simple_dag_instance.default_args)

    assert my_simple_dag_instance.catchup is False
    assert my_simple_dag_instance.default_args.get("retries") == 3
    assert my_simple_dag_instance.default_args.get("retry_delay") == timedelta(minutes=3)

    assert isinstance(my_second_dag_instance, DAG)    
    check_cycle(my_second_dag_instance)