import { MissingConfigError } from "./MissingConfigError";


export class AppConfig {
    public finServingLayerHost: string;
    public finServingLayerPort: string;

    constructor() {
        this.finServingLayerHost = this.getFinServingLayerHost();
        this.finServingLayerPort = this.getFinServingLayerPort();
    }

    private getFinServingLayerHost(): string {
        const host: string | undefined = process.env.FIN_SERVING_LAYER_HOST;
        if (host === undefined) {
            throw new MissingConfigError("FIN_SERVING_LAYER_HOST");
        }
        return host;
    }

    private getFinServingLayerPort(): string {
        const port: string | undefined = process.env.FIN_SERVING_LAYER_PORT;
        if (port === undefined) {
            throw new MissingConfigError("FIN_SERVING_LAYER_PORT");
        }
        return port;
    }
}
