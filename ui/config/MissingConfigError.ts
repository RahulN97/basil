
export class MissingConfigError extends Error {
    constructor(missingConfig: string) {
        const message: string = `Missing config ${missingConfig}. Make sure this env variable is set.`
        super(message);
        this.name = 'MissingConfigError';
        Object.setPrototypeOf(this, MissingConfigError.prototype);
    }
}
