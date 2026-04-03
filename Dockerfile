# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY requirements-railway.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements-railway.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput --clear || true

# Expose port
EXPOSE 8080

# Run gunicorn
CMD ["gunicorn", "onehub.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "4", "--timeout", "120"]
