# Data Pipeline with Airflow

Before we start, let's create these folders first:

```sh
mkdir -p mnt/dags mnt/tests mnt/logs mnt/plugins
```

Make sure to configure the Airflow user for the docker-compose:

```sh
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

## Starting Airflow

With `SequentialExecutor`

```sh
docker-compose -f sequential.yml up -d
```

With `LocalExecutor`

```sh
docker-compose -f local.yml up -d
```

With `CeleryExecutor`

```sh
docker-compose -f celery.yml up -d
```

## Airflow S3 Connection to MinIO

* Connection Name: `local_minio` or any name you like
* Connection Type: S3
* Extra: a JSON object with the following properties:
  ```json
  {
    "aws_access_key_id":"your_minio_access_key",
    "aws_secret_access_key": "your_minio_secret_key",
    "host": "http://minio:9000"
  }
  ```

## Running Tests

First we need to install pytest:
```sh
pip install pytest
```

Run tests:
```sh
pytest
```

## References

* [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)
* [MinIO Docker Quickstart Guide](https://docs.min.io/docs/minio-docker-quickstart-guide.html)
* [Deploy MinIO on Docker Compose](https://docs.min.io/docs/deploy-minio-on-docker-compose)
