# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Build context is repo root (see docker-compose); frontend files live in frontend/
COPY frontend/package.json ./
RUN npm install

COPY frontend/ .

# API URL from browser (host), not from container
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL
RUN npx tsc -b && npx vite build

# Serve stage
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
RUN echo 'server { listen 80; root /usr/share/nginx/html; index index.html; location / { try_files $uri $uri/ /index.html; } }' > /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
