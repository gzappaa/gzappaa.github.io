# Use official Python 3.13 image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Declare volume for PDF and Excel outputs
VOLUME ["/app/data"]

# Default command to run main.py
CMD ["python", "-m", "src.main"]