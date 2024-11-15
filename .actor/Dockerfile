FROM python:3.9-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ=Etc/UTC

# Update package lists and install necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set the timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs

# Verify Node.js and npm installation
RUN node --version && npm --version

# Create a user called 'myuser'
RUN useradd -m myuser

# Switch to the new user
USER myuser

# Set the working directory in the user's home directory
WORKDIR /home/myuser

# Copy application code
COPY . .

# Install Python dependencies if you have any
RUN pip install --no-cache-dir -r requirements.txt  # Make sure requirements.txt exists

# Install Node.js dependencies if you have a package.json
RUN npm install  # Make sure package.json exists in the root

# Set CMD to run the Python application
CMD ["python3", "main.py"]