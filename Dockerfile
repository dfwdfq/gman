FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends postgresql-client && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY req.txt .
RUN pip install --no-cache-dir -r req.txt


COPY . .

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]