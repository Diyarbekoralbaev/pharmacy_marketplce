# Use the official Python image from the Docker Hub
FROM python:3.12-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

# Copy the Django project code
COPY . /app/

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
