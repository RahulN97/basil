import { MissingConfigError } from './MissingConfigError';

const envVars: Record<string, string | undefined> = {
  ENV: process.env.REACT_APP_ENV,
  FIN_SERVING_LAYER_HOST: process.env.REACT_APP_FIN_SERVING_LAYER_HOST,
  FIN_SERVING_LAYER_PORT: process.env.REACT_APP_FIN_SERVING_LAYER_PORT,
  FIREBASE_API_KEY: process.env.REACT_APP_FIREBASE_API_KEY,
  FIREBASE_AUTH_DOMAIN: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
};

export class AppConfig {
  public env: string;
  public finServingLayerHost: string;
  public finServingLayerPort: string;
  public firebaseApiKey: string;
  public firebaseAuthDomain: string;

  private defaultEnv = 'dev';
  private defaultFinServingLayerHost = '0.0.0.0';
  private defaultFinServingLayerPort = '8000';

  constructor() {
    this.env = this.extractEnv();
    this.finServingLayerHost = this.extractFinServingLayerHost();
    this.finServingLayerPort = this.extractFinServingLayerPort();
    this.firebaseApiKey = this.extractFirebaseApiKey();
    this.firebaseAuthDomain = this.extractFirebaseAuthDomain();
  }

  private checkUndefined(varName: string, val: string | undefined, defaultVal?: string): string {
    if (val === undefined) {
      if (defaultVal === undefined) {
        throw new MissingConfigError(varName);
      }
      return defaultVal;
    }
    return val;
  }

  private extractEnv(): string {
    return this.checkUndefined('ENV', envVars.ENV, this.defaultEnv);
  }

  private extractFinServingLayerHost(): string {
    return this.checkUndefined(
      'FIN_SERVING_LAYER_HOST',
      envVars.FIN_SERVING_LAYER_HOST,
      this.defaultFinServingLayerHost,
    );
  }

  private extractFinServingLayerPort(): string {
    return this.checkUndefined(
      'FIN_SERVING_LAYER_PORT',
      envVars.FIN_SERVING_LAYER_PORT,
      this.defaultFinServingLayerPort,
    );
  }

  private extractFirebaseApiKey(): string {
    return this.checkUndefined('FIREBASE_API_KEY', envVars.FIREBASE_API_KEY);
  }

  private extractFirebaseAuthDomain(): string {
    return this.checkUndefined('FIREBASE_AUTH_DOMAIN', envVars.FIREBASE_AUTH_DOMAIN);
  }
}
