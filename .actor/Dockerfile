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

# Additional step to install Node.js and npm
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get install -y nodejs npm

# Create a user called 'myuser'
RUN useradd -m myuser

# Switch to the new user
USER myuser

# Set the working directory in the user's home directory
WORKDIR /home/myuser

# Install Python dependencies if you have any
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js dependencies if you have a package.json
COPY package.json package-lock.json ./
RUN npm install

# Copy application code
COPY . .

FROM builder AS final

# Set CMD to run npm start
CMD ["npm", "start", "-s"]