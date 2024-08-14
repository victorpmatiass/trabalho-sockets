# Dockerfile for server
FROM python:3.11

WORKDIR /app

COPY server.py .

RUN pip install --no-cache-dir flask

CMD ["python", "server.py"]
