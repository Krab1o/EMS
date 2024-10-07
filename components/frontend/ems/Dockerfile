# Development Dockerfile for React app with hot-reload support
FROM node:18.12.1-alpine as development

WORKDIR /app

# Add node_modules/.bin to PATH
ENV PATH /app/node_modules/.bin:$PATH

# Install dependencies (include devDependencies)
COPY package.json yarn.lock ./
RUN yarn install

# Copy the rest of the app for hot-reload (only for initial build)
COPY . /app

# Expose the React development server's port
EXPOSE 30002

# Start the React app with hot-reload
CMD ["yarn", "start"]
