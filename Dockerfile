# Use an official Python runtime with Alpine Linux as a parent image
FROM python:3.11-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install build dependencies
RUN apk add --no-cache \
    build-base \
    libffi-dev \
    mysql-dev \
    && pip install --upgrade pip

# Install poetry
RUN pip install poetry

# Set the working directory in the container
WORKDIR /team-1-Backend-DN

# Copy just the poetry-related files to the container
COPY pyproject.toml poetry.lock /team-1-Backend-DN/

# Install poetry dependencies (this allows caching)
RUN poetry install --no-root --no-interaction

# Copy the rest of the application code
COPY . /team-1-Backend-DN/

# Copy the start script
COPY start.sh /team-1-Backend-DN/

# Make the start script executable
RUN chmod +x /team-1-Backend-DN/start.sh

EXPOSE 8000

CMD ["sh", "start.sh", "poetry"]
