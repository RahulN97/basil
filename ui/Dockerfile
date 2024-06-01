FROM node:21.5.0

WORKDIR /app

COPY package*.json ./
RUN npm ci --no-audit --maxsockets 1

COPY . .

EXPOSE ${EXPO_DEVTOOLS_PORT}
EXPOSE ${EXPO_LOCAL_SERVER_PORT}
EXPOSE ${EXPO_LAN_PORT}
EXPOSE ${EXPO_METRO_BUNDLER_PORT}
EXPOSE ${EXPO_WEB_PORT}

# can't use Docker for ios and android
CMD ["./run.sh"]
