FROM python:3.11-slim AS backend-runtime

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ /app/backend/
RUN pip install --no-cache-dir -e /app/backend

COPY main.py app.py ./

EXPOSE 8000
CMD ["python", "main.py", "serve"]
