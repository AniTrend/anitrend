# Stage 1: Build stage
FROM python:3.12 AS builder

ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy the poetry.lock and pyproject.toml files to the container
COPY poetry.lock pyproject.toml /usr/src/app/

# Install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the rest of the project code
COPY . /usr/src/app/

RUN mkdir tmp

# Expose the port your Django app will run on
EXPOSE 8800
