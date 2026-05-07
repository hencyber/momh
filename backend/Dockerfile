# Intial Docker image for the backend service.
# This will be update when he FastAPI backend implementation is added.

FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install uv

RUN uv sync

EXPOSE 8000

CMD ["uv", "run", "python", "-m", "momh.backend.app.aterbetalning.api"]