FROM python:3.12.4-slim

RUN apt-get update && \
    apt-get install -y htop lsof vim curl && \
    curl -sSL https://install.python-poetry.org | python3 -

ENV PATH "/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-root

COPY . /app

# Streams python service logs to docker
ENV PYTHONUNBUFFERED 1

EXPOSE ${SERVICE_PORT}

CMD ["./run.sh"]
