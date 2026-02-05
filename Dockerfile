FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy only requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port (Render will set PORT env variable)
EXPOSE 8000

# Use uvicorn for production
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}