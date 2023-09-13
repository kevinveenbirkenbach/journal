# Use the official Python image from the DockerHub
FROM python:latest

# Set the working directory in docker
WORKDIR /app

# Copy the dependencies file to the working directory
#COPY requirements.txt .

# Copy the content of the local src directory to the working directory
COPY . .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt