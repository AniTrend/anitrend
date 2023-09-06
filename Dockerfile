# Stage 1: Build stage
FROM python:3.11 AS builder

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

# Stage 2: Django Server stage
FROM builder AS django-server

# Run Django's migrations
RUN python manage.py migrate

# Expose the port your Django app will run on
EXPOSE 8800

# Start Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8800"]

# Stage 3: Django Q Cluster stage
FROM builder AS django-q-cluster

# Start Django Q scheduler and worker
CMD ["python", "manage.py", "qcluster"]
