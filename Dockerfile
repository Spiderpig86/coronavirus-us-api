FROM python:3.8

# Environment settings
ENV PYTHONUNBUFFERD 1
ENV PYTHONDONTWRITEBYTECODE 1

# Image directory for api
WORKDIR /api

# Setup dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . /