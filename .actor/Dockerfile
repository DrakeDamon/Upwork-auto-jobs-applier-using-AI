# Use Python 3.9 slim as the base image for a lightweight and secure container
FROM python:3.9-slim

# Set environment variables for Python to run without writing bytecode and unbuffered output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Ensure the package lists are updated and necessary system packages are installed
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set the timezone to UTC for consistency across different environments
ENV TZ=Etc/UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Create and set the working directory to /home/myuser as suggested by Apify
WORKDIR /home/myuser

# Create a directory for application code and set appropriate permissions
RUN mkdir -p /home/myuser/app \
    && chown -R myuser:myuser /home/myuser/app

# Copy the requirements file into the container, and then install dependencies
COPY --chown=myuser:myuser requirements.txt /home/myuser/app/
WORKDIR /home/myuser/app
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY --chown=myuser:myuser . /home/myuser/app/

# Switch back to the app directory and set the user to myuser for runtime
WORKDIR /home/myuser/app
USER myuser

# Set the command to run when the container starts
CMD ["python", "main.py"]

# Expose port if needed (e.g., for web interfaces or APIs)
# EXPOSE 8000