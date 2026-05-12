FROM ghcr.io/mlflow/mlflow:v2.12.1

EXPOSE 5000

CMD ["mlflow", "ui", "--host", "0.0.0.0", "--port", "5000"]