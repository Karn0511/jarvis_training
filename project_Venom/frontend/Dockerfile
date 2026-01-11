# Frontend Dockerfile for Venom UI
FROM node:20-alpine AS build

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Build production bundle
RUN npm run build

# Production stage - Nginx
FROM nginx:alpine

# Copy built assets from build stage
COPY --from=build /app/dist/venom-dashboard/browser /usr/share/nginx/html

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
