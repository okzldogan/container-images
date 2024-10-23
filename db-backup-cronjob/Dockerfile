
# Use python:3.12-alpine as base image

FROM python:3.12-alpine

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Install ca-certificates, jq, curl, mysql-client

RUN apk update && apk add mysql-client \
    curl \
    jq \
    vim \
    bash \
    ca-certificates


# Create /usr/job directory

RUN mkdir -p /usr/job

# Add container user, create home directory and set permissions for /usr/job

RUN addgroup -S containeruser && adduser -D -S containeruser -G containeruser --no-create-home && \
    chown -R containeruser:containeruser /usr/job

# Switch to container user

USER containeruser

# Make a directory for the app

WORKDIR /usr/job

# Add virtual environment to path

ENV PATH="/usr/job/venv/bin:$PATH"

# Activate virtual environment

RUN python -m venv /usr/job/venv

# Copy all files in container-files to /usr/job

COPY ./container-files/ .

# Install requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

