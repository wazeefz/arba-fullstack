# Use an official Node.js runtime as the base image
FROM node:18

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock) first to install dependencies
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend code into the container
COPY . .

# Expose the port that your frontend will run on
EXPOSE 3000

# Run the Vue.js app in development mode
CMD ["npm", "run", "dev"]
