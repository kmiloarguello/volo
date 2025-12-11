# Scripts Dockerfile for running test and data generation scripts
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements (same as backend since scripts need similar dependencies)
COPY requirements.txt .

# Install Python dependencies (with trusted host to handle SSL issues in restricted environments)
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Copy scripts
COPY . .

# Default command (can be overridden)
CMD ["bash"]
