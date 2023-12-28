FROM --platform=linux/amd64 apache/airflow:2.8.0

RUN pip install ccxt==4.1.100 \
  apache-airflow-providers-mongo==3.5.0 \
  airflow-provider-great-expectations==0.2.7
