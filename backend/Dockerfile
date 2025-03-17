# FROM python:3.9

# WORKDIR /app

# COPY requirements.txt /app/
# RUN pip install --no-cache-dir -r requirements.txt

# RUN pip install --no-cache-dir numpy==1.23.5 thinc==8.1.7
# RUN python -m spacy download en_core_web_sm


# COPY . /app/

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


FROM python:3.9-slim

# Set a longer timeout for pip
ENV PIP_DEFAULT_TIMEOUT=100

# Use a different PyPI mirror if needed
RUN pip config set global.index-url https://pypi.org/simple

# Set working directory
WORKDIR /app

# Install system dependencies needed for building some Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy the rest of the application files
COPY . .

# Expose the port used by FastAPI
EXPOSE 8000

# Command to run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]