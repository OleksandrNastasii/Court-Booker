# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app/project

# Copy your project folder into the container
COPY . /app

# Install dependencies (if you have a requirements.txt in your project)
RUN pip install --no-cache-dir -r /app/requirements.txt

# Ensure we're at the correct level (in the parent folder)
WORKDIR /app

# Run the project as a module
CMD ["python", "main.py"]
