import pino from 'pino';

const logger = pino({
    level: 'info',
    transport: {
        target: 'pino-pretty',
        options: {
            colorize: true
        },
    },
    browser: {
        asObject: false,
    },
});

export default logger;
