# Use python:3.12-alpine as base image

FROM python:3.12-alpine

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Install ca-certificates, telnet, jq, curl, mysql-client, iputils-ping, python3.10 with apk

RUN apk update && apk add mysql-client \
    curl \
    busybox-extras \
    jq \
    vim \
    bash \
    ca-certificates


# Create /usr/app directory

RUN mkdir -p /usr/app

# Add container user, create home directory and set permissions for /usr/app

RUN addgroup -S containeruser && adduser -D -S containeruser -G containeruser --no-create-home && \
    chown -R containeruser:containeruser /usr/app

# Grant necessary permissions to containeruser to run busybox commands

RUN chmod u+s /bin/busybox

# Switch to container user

USER containeruser

# Make a directory for the app

WORKDIR /usr/app

# Add PORT 5000 as environment variable

ENV PORT 5000

# Add virtual environment to path

ENV PATH="/usr/app/venv/bin:$PATH"

# Activate virtual environment

RUN python -m venv /usr/app/venv

# Copy all files in container-files to /usr/app

COPY ./container-files/ .

# Install requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000

EXPOSE 5000

# Set environment variable for FLASK_APP

ENV FLASK_APP=app.py

# Start flask and run app.py from /usr/app directory

CMD ["flask", "run", "--host", "0.0.0.0","-p","5000"]
