# Intial Docker image for the backend service.
# This will be update when he FastAPI backend implementation is added.

FROM python:3.12-slim

WORKDIR / app

COPY . .

EXPOSE 8000

CMD ["python", "-m", "http.server", "8000"]