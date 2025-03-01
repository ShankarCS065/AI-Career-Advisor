# Use Debian-based Python image for better compatibility with pyarrow
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies needed for pyarrow and other dependencies
RUN apt-get update && apt-get install -y \
    build-essential cmake g++ curl wget unzip \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the port used by Streamlit
EXPOSE 8501

# Command to run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
