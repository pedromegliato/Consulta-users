export class ApiError extends Error {
  constructor(
    readonly code: string,
    readonly status: number,
    readonly serverMessage: string | null = null,
    readonly details: string[] = [],
    readonly requestId: string | null = null,
  ) {
    super(`${code} (HTTP ${status})`);
    this.name = 'ApiError';
  }
}
