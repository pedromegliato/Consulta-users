import { ApiError } from '../api/ApiError';

export interface UserFacingError {
  message: string;
  details: string[];
  requestId: string | null;
}

const FALLBACK_BY_STATUS: Record<number, string> = {
  408: 'A consulta demorou mais que o esperado. Tente novamente.',
  429: 'Muitas consultas em pouco tempo. Aguarde alguns segundos e tente de novo.',
  502: 'O serviço está temporariamente indisponível. Tente novamente em instantes.',
  503: 'O serviço está temporariamente indisponível. Tente novamente em instantes.',
  504: 'O serviço demorou para responder. Tente novamente em instantes.',
};

const NETWORK_FAILURE =
  'Não foi possível falar com o servidor. Verifique sua conexão e tente novamente.';

const UNEXPECTED = 'Algo deu errado por aqui. Tente novamente em instantes.';

export function toUserFacingError(error: unknown): UserFacingError {
  if (error instanceof ApiError) {
    return {
      message: error.serverMessage ?? FALLBACK_BY_STATUS[error.status] ?? UNEXPECTED,
      details: error.details,
      requestId: error.requestId,
    };
  }
  if (error instanceof TypeError) {
    return { message: NETWORK_FAILURE, details: [], requestId: null };
  }
  return { message: UNEXPECTED, details: [], requestId: null };
}
