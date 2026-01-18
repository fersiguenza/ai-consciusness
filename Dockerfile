FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for matplotlib/networkx
RUN apt-get update && apt-get install -y python3-tk libpng-dev libfreetype6-dev && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Ensure modules/ is on PYTHONPATH for all runs
ENV PYTHONPATH=/app
# Default: run API server on port 5050
CMD ["python", "api/api_server.py"]