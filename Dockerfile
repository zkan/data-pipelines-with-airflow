FROM --platform=linux/amd64 apache/airflow:3.0.1-python3.9

RUN pip install ccxt==4.4.82 \
  apache-airflow-providers-mongo==5.0.3 \
  airflow-provider-great-expectations==0.3.0
