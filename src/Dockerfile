# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Set environment variables
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Copy the Django project code and deployment script to the container
COPY . /app/
COPY ./entrypoint.sh /

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install the required dependencies
RUN pip install -r requirements.txt

# Expose the port on which the Django server will run
EXPOSE 8000

# Define entrypoint - migrations, collecstatic, and runserver
ENTRYPOINT ["sh", "/entrypoint.sh"]