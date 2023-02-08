FROM apache/airflow:2.2.2

RUN pip install ccxt==2.7.60 \
  apache-airflow-providers-mongo==2.3.0 \
  airflow-provider-great-expectations==0.1.3
