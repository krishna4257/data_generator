# Use an official Python runtime as base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first (for caching)
COPY requirements.txt /app/

# Update pip and install dependencies
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

# Copy all project files into the container
COPY . /app/

# Set the entrypoint command
CMD ["python", "generator.py"]
