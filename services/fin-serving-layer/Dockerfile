FROM python:3.8-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Streams python service logs to docker
ENV PYTHONUNBUFFERED 1

EXPOSE ${SERVICE_PORT}

CMD ["./run.sh"]
