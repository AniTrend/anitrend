FROM python:3.13.0-slim AS base
WORKDIR /usr/src
COPY . /usr/src/

FROM base AS scaffold
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip

FROM scaffold AS dependencies
RUN pip install poetry==1.5.0 \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

FROM dependencies AS final
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN chmod +x start.sh
