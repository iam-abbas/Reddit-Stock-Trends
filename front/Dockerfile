# Set base image (host OS)
FROM node:lts-alpine
WORKDIR /code
# Install dependencies
RUN npm install
RUN npm install -g @vue/cli

# Command to run on container start
CMD [ "sh", "-c", "npm run serve" ]
