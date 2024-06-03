import { MissingConfigError } from "./MissingConfigError";


export class AppConfig {
    public env: string;
    public finServingLayerHost: string;
    public finServingLayerPort: string;

    constructor() {
        this.env = this.extractEnv();
        this.finServingLayerHost = this.extractFinServingLayerHost();
        this.finServingLayerPort = this.extractFinServingLayerPort();
    }

    private checkUndefined(val: string | undefined, varName: string): string {
        if (val === undefined) {
            throw new MissingConfigError(varName);
        }
        return val;
    }

    private extractEnv(): string {
        return this.checkUndefined(process.env.ENV, "ENV");
    }

    private extractFinServingLayerHost(): string {
        return this.checkUndefined(process.env.FIN_SERVING_LAYER_HOST, "FIN_SERVING_LAYER_HOST");
    }

    private extractFinServingLayerPort(): string {
        return this.checkUndefined(process.env.FIN_SERVING_LAYER_PORT, "FIN_SERVING_LAYER_PORT");
    }
}
