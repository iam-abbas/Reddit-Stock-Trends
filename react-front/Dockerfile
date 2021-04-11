# Set base image (host OS)
FROM node:lts-alpine

WORKDIR /code

# Install dependencies
COPY package*.json .
RUN npm install

# Command to run on container start
CMD [ "sh", "-c", "npm start" ]
