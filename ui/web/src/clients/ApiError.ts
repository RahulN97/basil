export class ApiError extends Error {
  constructor(error: string) {
    const message = `Request to fin-serving-layer failed: ${error}`;
    super(message);
    this.name = 'ApiError';
    Object.setPrototypeOf(this, ApiError.prototype);
  }
}
