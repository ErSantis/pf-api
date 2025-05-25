# Base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt /app/

# Install a lighter version of PyTorch (CPU only) and other dependencies
# Install a lighter version of PyTorch (CPU only) and other dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

# Copy project
COPY . /app/

# Expose port
EXPOSE 8000

# Verify installations
RUN python -c "import numpy; print(f'NumPy version: {numpy.__version__}')" && \
    python -c "import django; print(f'Django version: {django.get_version()}')" && \
    python -c "import torch; print(f'PyTorch version: {torch.__version__}')"

# Run the application with gunicorn for production
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
