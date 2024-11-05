# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /opt/app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && \
    apt-get upgrade -yq ca-certificates && \
    apt-get install -yq --no-install-recommends \
    prometheus-node-exporter

# Copy the rest of the application files into the container
COPY . .

ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV DEBIAN_FRONTEND noninteractive

# Expose the port your application runs on
EXPOSE 7860
EXPOSE 8000
EXPOSE 9100

# Run the application
CMD ["python", "app.py"]
