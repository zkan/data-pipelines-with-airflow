import logging

from airflow.decorators import dag, task
from airflow.utils import timezone


@task.python(task_id="extract")
def extract():
    return [
        {
            "name": "Kan",
            "salary": 30000,
        },
        {
            "name": "John",
            "salary": 25000,
        },
    ]


@task.python()
def transform(salary_data):
    total = 0

    for each in salary_data:
        total += each["salary"]

    return total


@task.python()
def load(total_salary):
    logging.info(f"Total salary is: {total_salary}")


default_args = {
    "owner": "zkan",
    "start_date": timezone.datetime(2022, 2, 1),
}
@dag(
    default_args=default_args,
    schedule_interval=None,
)
def demo_taskflow_api(): 
    salary_data = extract()
    total_salary = transform(salary_data)
    load(total_salary)


dag = demo_taskflow_api()