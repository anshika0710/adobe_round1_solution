FROM --platform=linux/amd64 python:3.9-slim

# Set working directory
WORKDIR /app

# Prevents Python from writing .pyc files to disk and ensures UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Optional: Pre-download HuggingFace models into cache (uncomment if allowed)
# RUN python -c "from transformers import pipeline; pipeline('summarization', model='sshleifer/distilbart-cnn-12-6')"

# Copy all project files
COPY . .

# Entrypoint
ENTRYPOINT ["python", "app.py"]

