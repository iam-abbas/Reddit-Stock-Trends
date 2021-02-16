# Set base image (host OS)
FROM node:lts-alpine

# Set the working directory in the container
WORKDIR /tmp

# Copy the node requirements to the container
COPY package*.json ./

# Install dependencies
RUN npm install

WORKDIR /code

# Copy the sources files into the image
COPY . .

# Command to run on container start
CMD [ "sh", "-c", "cp -r /tmp/node_modules /code/node_modules && npm run serve" ]