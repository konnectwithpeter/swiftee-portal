FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create a script to run both Django and background tasks
RUN echo '#!/bin/bash\n\
python manage.py migrate\n\
python manage.py process_tasks & \n\
gunicorn --bind 0.0.0.0:$PORT --workers 3 myproject.wsgi:application\n\
' > /app/start.sh

RUN chmod +x /app/start.sh

# Command to run the script
CMD ["/app/start.sh"]
