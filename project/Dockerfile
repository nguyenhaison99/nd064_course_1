# Use an official Python 3.8 base image from Docker Hub
FROM python:3.8

# Set the maintainer label to indicate who maintains this Dockerfile
LABEL maintainer="SonNH65"

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the contents of the local 'techtrends' directory to the /app directory in the container
COPY techtrends .

# Install the Python packages listed in requirements.txt using pip
RUN pip3 install -r requirements.txt

# Run the init_db.py script to initialize the database
RUN python3 init_db.py

# Expose port 3111, which is the port your Flask application will listen on
EXPOSE 3111

# Define the command to run when the container starts, which is to run 'app.py' using Python
CMD ["python", "app.py"]
