# Use an official, lightweight Python base image
FROM python:3.12-slim

# Prevent Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1

# Force Python stdout and stderr to print immediately without buffering
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies without keeping local cache to minimize image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend source code directory structure
COPY backend/ /app/backend/

# Expose the internal port the FastAPI application runs on
EXPOSE 8000

# Set Python Path so backend modules are discoverable
ENV PYTHONPATH=/app

# Command to start the FastAPI application server
CMD ["uvicorn", "backend.api.app:app", "--host", "0.0.0.0", "--port", "8000"]