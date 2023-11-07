# Stage 1: Build stage
FROM python:3.10.12-slim AS builder

# Set the working directory in the container
WORKDIR /usr/src

# Install system dependencies and upgrade pip
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip

# Copy only the dependency files to leverage caching
COPY pyproject.toml poetry.lock /usr/src/

# Install project dependencies
RUN pip install poetry==1.5.0 \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the rest of the project code
COPY . /usr/src/

# Stage 2: Final image
FROM builder AS final

# Define your environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
