# Simple demo container for Motor Digital Twin
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5050

WORKDIR /app

# Install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir eventlet

# Copy code
COPY . .

EXPOSE 5050

# For demos this is fine; for production consider gunicorn with eventlet worker
CMD ["python", "app.py"]
