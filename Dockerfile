# Base image with Python
FROM python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED=1

ENV PYTHONPATH "${PYTHONPATH}:/code"
ENV PYTHONHASHSEED=1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt .

RUN apt-get update                             \
 && apt-get install -y --no-install-recommends \
    ca-certificates curl firefox-esr           \
 && rm -fr /var/lib/apt/lists/*

RUN python -m pip install --no-cache-dir --upgrade pip
RUN pip install -r requirements.txt


# Copy project
COPY . .

# Collect static files

RUN python manage.py collectstatic --no-input


# Install Nginx
RUN apt-get update && \
    apt-get install -y nginx

# Expose port 80 for Nginx
EXPOSE 80

EXPOSE 8000

# Start Gunicorn and Nginx
CMD ["sh", "-c", "./wait-for-it.sh -t 60 db:5432 -- gunicorn --bind 0.0.0.0:8000 evaluationApplication.wsgi:application --access-logfile /dev/stdout --error-logfile /dev/stderr --forwarded-allow-ips=172.18.0.2 --access-logformat '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\"' & nginx -g 'daemon off;'"]