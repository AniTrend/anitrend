# Stage 1: Build stage
FROM python:3.12.0-slim AS builder

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install Poetry
RUN pip install poetry==1.5.0

# Copy the poetry.lock and pyproject.toml files to the container
COPY poetry.lock pyproject.toml /usr/src/app/

# Install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the rest of the project code
COPY . /usr/src/app/

RUN mkdir tmp
