# Use an official Python runtime as a parent image
FROM python:3.7-slim

# Set the working directory to /webapp
WORKDIR /webapp

# Copy the current directory contents into the container at /webapp
COPY . /webapp

# Install any needed packages specified in requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 5006
