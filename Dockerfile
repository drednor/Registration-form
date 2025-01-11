# Use an official Python runtime as base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . /app/

# Expose the port your Flask app runs on
EXPOSE 5000

ENV PYTHONUNBUFFERED=1

# Set the default command to run the app
CMD ["flask", "run", "--host=0.0.0.0"]
