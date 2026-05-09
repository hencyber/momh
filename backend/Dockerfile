# Intial Docker image for the backend service.
# This will be update when the FastAPI backend implementation is added.

FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install uv

RUN uv sync

EXPOSE 8000

# Henke
# CMD ["uv", "run", "python", "-m", "momh.backend.app.aterbetalning.api"]

# Mona
# CMD ["uv", "run", "python", "-m", "momh.backend.app.main"]

# Orhan
CMD ["uv", "run", "python", "-m", "momh.backend.app.studiestod.main"]