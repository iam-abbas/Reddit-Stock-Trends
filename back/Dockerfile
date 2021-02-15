# Set base image (host OS)
FROM python:3.8

# Set the working directory in the container
WORKDIR /code

# Copy the pip requirements to the container
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Clean the workspace
RUN rm requirements.txt

# Copy the sources files into the image
COPY . .

# Command to run on container start
CMD [ "python", "./wsgi.py" ]