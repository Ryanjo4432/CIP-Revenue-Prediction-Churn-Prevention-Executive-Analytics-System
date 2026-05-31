FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 0.0.0.0 exposes the service outside the container
CMD ["uvicorn", "ml_service:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
