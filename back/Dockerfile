# Set base image (host OS)
FROM python:3.8

# Set the working directory in the container
WORKDIR /code

# Copy the pip requirements to the container
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Command to run on container start
CMD [ "python", "./wsgi.py" ]