FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl

# Copy source code
COPY . ./metrics_service

# Expose port (used internally, not published outside)
EXPOSE 8001

# Start service
#CMD ["uvicorn", "metrics_service.main:app", "--host", "0.0.0.0", "--port", "8001"]

