# Use Ubuntu as the base image
FROM ubuntu:22.04

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    POETRY_HOME=/opt/poetry \
    PATH="/opt/poetry/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 python3.11-venv python3-pip \
    redis-server \
    curl \
    bash \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3.11 -

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry
RUN poetry install --no-root

# Copy the rest of the application
COPY . .

# expose flask server port 5000
EXPOSE 5000

CMD flask --app server.py run

