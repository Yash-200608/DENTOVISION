# Use official Python runtime as a parent image
FROM python:3.12-slim

# Create a non-root user for security
RUN useradd -m -s /bin/bash appuser

# Set working directory
WORKDIR /app

# Install system dependencies for OpenCV, DICOM, and Magic
# libmagic1 is required for python-magic on Linux
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Copy package metadata and install Python dependencies
COPY requirements.txt pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir --no-deps .

# Copy remaining runtime assets (configs, fallback weights)
COPY configs ./configs
COPY yolov8n.pt ./yolov8n.pt

# Set permissions for the non-root user
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Set environment variables
ENV PYTHONPATH=/app/src
ENV API_HOST=0.0.0.0
ENV API_PORT=8000

# Expose port
EXPOSE 8000

# Command to run the application using variables
CMD uvicorn dentovision.api.app:app --host $API_HOST --port $API_PORT
