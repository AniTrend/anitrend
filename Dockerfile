FROM python:3.13.7-slim AS base
WORKDIR /usr/src

FROM base AS scaffold
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip

FROM scaffold AS dependencies
COPY pyproject.toml poetry.lock ./
RUN pip install poetry==2.2 \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

FROM dependencies AS final
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /usr/src/
RUN chmod +x start.sh