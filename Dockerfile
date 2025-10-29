FROM python:3.11-slim

WORKDIR /app

# Install postgres driver dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev

# Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
