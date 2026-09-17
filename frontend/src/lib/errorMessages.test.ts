import { describe, expect, it } from 'vitest';

import { ApiError } from '../api/ApiError';
import { toUserFacingError } from './errorMessages';

describe('toUserFacingError', () => {
  it('usa a mensagem que o backend ja entrega pronta para o usuario', () => {
    const error = new ApiError(
      'validation_error',
      422,
      'Confira os IDs informados.',
      ['user_ids: too short'],
      'req-1',
    );

    expect(toUserFacingError(error)).toEqual({
      message: 'Confira os IDs informados.',
      details: ['user_ids: too short'],
      requestId: 'req-1',
    });
  });

  it('cai no fallback local quando a resposta nao traz envelope', () => {
    expect(toUserFacingError(new ApiError('unknown_error', 503)).message).toContain(
      'temporariamente indisponível',
    );
  });

  it('trata falha de rede sem expor detalhe tecnico', () => {
    const result = toUserFacingError(new TypeError('Failed to fetch'));

    expect(result.message).toContain('Verifique sua conexão');
    expect(result.details).toEqual([]);
  });
});
