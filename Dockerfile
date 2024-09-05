# Use the official Python image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the FastAPI application
CMD ["uvicorn", "hngr.main:app", "--host", "0.0.0.0", "--port", "5000"]
