# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code to the container
COPY . .

# Expose the port on which the Django server will run
EXPOSE 8000

# Run the Django server when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
