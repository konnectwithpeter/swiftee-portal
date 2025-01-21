# Use the official Python image
FROM python:3.11-slim

# Set environment variables to optimize Python's behavior
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the container
COPY . .

# Create a startup script to run migrations, background tasks, and the app
RUN echo '#!/bin/bash\n\
python manage.py migrate\n\
python manage.py collectstatic --noinput\n\
python manage.py process_tasks &\n\
gunicorn --bind 0.0.0.0:$PORT --workers 3 <your_project_name>.wsgi:application\n\
' > /app/start.sh

# Make the startup script executable
RUN chmod +x /app/start.sh

# Expose the port that your app runs on
EXPOSE 8000

# Set the default command to run the startup script
CMD ["/app/start.sh"]
