FROM python:3.14.2-slim AS base
WORKDIR /usr/src
RUN pip install --upgrade pip poetry==2.2

FROM base AS dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

FROM dependencies AS final
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /usr/src/
RUN chmod +x start.sh
