# Use an official Node.js runtime as the base image
FROM node:18

RUN npm install -g http-server

# Set the working directory in the container to /app
WORKDIR /usr/news/news_gui/

# copy both 'package.json' and 'package-lock.json' (if available)
COPY ./package*.json /usr/news/news_gui/

# install project dependencies
RUN npm install

# Copy the rest of the application files to the container
COPY . /usr/news/news_gui/

# Build the Vue.js application in the container
RUN npm run build

# Expose the port used by the application
# EXPOSE 8080

# Set the command to run when the container starts
# CMD [ "npm", "run", "serve"]
# CMD [ "http-server", "dist" ]
