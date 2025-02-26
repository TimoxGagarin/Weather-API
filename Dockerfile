FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

WORKDIR /app

COPY ./api /app/api

COPY uv.lock pyproject.toml /app/
RUN uv sync
ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]