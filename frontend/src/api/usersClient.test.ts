import { afterEach, describe, expect, it, vi } from 'vitest';

import { buildFetchUsersResponseDto } from '../test/factories';
import { ApiError } from './ApiError';
import { fetchUsers } from './usersClient';

function stubFetch(body: unknown, status = 200): ReturnType<typeof vi.fn> {
  const stub = vi.fn(async () => new Response(JSON.stringify(body), { status }));
  vi.stubGlobal('fetch', stub);
  return stub;
}

afterEach(() => {
  vi.unstubAllGlobals();
});

describe('fetchUsers', () => {
  it('envia os ids no contrato do backend e mapeia a resposta para o dominio', async () => {
    const stub = stubFetch(buildFetchUsersResponseDto());

    const result = await fetchUsers([1, 2, 3]);

    const [, init] = stub.mock.calls[0] as [string, RequestInit];
    expect(JSON.parse(String(init.body))).toEqual({ user_ids: [1, 2, 3] });
    expect(result.users.map((user) => user.id)).toEqual([1, 2]);
    expect(result.failed).toEqual([3]);
  });

  it('converte o envelope de erro do backend em ApiError', async () => {
    stubFetch(
      {
        error: {
          code: 'validation_error',
          message: 'Confira os IDs informados.',
          details: [],
          request_id: 'req-1',
        },
      },
      422,
    );

    await expect(fetchUsers([0])).rejects.toBeInstanceOf(ApiError);
  });
});
