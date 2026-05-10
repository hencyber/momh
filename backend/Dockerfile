# Intial Docker image for the backend service.
# This will be update when the FastAPI backend implementation is added.

FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir uv

RUN uv sync --frozen

ENV PYTHONPATH=/app/src

EXPOSE 8000