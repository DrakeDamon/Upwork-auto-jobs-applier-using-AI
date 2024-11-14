FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ=Etc/UTC

# Update package lists and install necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends     tzdata     curl     && rm -rf /var/lib/apt/lists/*

# Set the timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Create a user called 'myuser'
RUN useradd -m myuser

# Switch to the new user
USER myuser

# Set the working directory in the user's home directory
WORKDIR /home
CMD npm start -silent