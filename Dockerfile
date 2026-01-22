# Build Frontend
FROM node:18 as frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Build Backend
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY backend/requirements.txt .
# Add gunicorn to requirements if not there (we installed it manually)
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn whitenoise django-cors-headers

# Copy backend code
COPY backend/ .

# Copy built frontend assets to Django static
# We need to collect them. For now, let's copy them to a specific folder
# and ensure Django collects them.
COPY --from=frontend-builder /app/frontend/dist /app/frontend_build

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False

# Collect static files
# We need to tell Django where to find the React build files to collect them
# OR we serve them via WhiteNoise. WhiteNoise serves 'staticfiles' (STATIC_ROOT).
# We need to manually move React build to staticfiles or configure STATICFILES_DIRS.
# Easier: Start script moves them.

# Expose port
EXPOSE 8000

# Copy startup script
COPY docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

CMD ["/app/docker-entrypoint.sh"]
