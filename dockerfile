# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /opt/app

# Copy and install Python dependencies
COPY requirements.txt . 
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install system dependencies and Prometheus Node Exporter
RUN apt-get update && \
    apt-get upgrade -yq ca-certificates && \
    apt-get install -yq --no-install-recommends prometheus-node-exporter

# Copy the rest of the application files
COPY . .

# Set environment variables
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV DEBIAN_FRONTEND=noninteractive

# Expose application ports
EXPOSE 7860 8000 9100

# Start Prometheus Node Exporter and the application
CMD ["bash", "-c", "prometheus-node-exporter --web.listen-address=:9100 & python /opt/app/app.py"]
