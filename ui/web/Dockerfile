FROM node:21.5.0

RUN apt-get update && \
    apt-get install -y htop lsof vim

WORKDIR /app

COPY package*.json /app/
RUN npm ci --no-audit --maxsockets 1

COPY . /app

EXPOSE ${PORT}

# can't use Docker for ios and android
CMD ["./run.sh"]
