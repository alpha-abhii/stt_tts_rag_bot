# # Use official Python image
# FROM python:3.10

# # Set working directory
# WORKDIR /app

# # Copy app files
# COPY app/ /app/
# COPY requirements.txt /app/

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Expose port 8080 (Cloud Run uses this port)
# EXPOSE 8080

# # Run the app
# CMD ["python", "main.py"]


# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables (if not using Secret Manager)
# ENV GOOGLE_API_KEY=your_api_key
# ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json

# Expose the port your app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "main.py"]