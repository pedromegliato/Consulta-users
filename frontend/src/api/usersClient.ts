import type { Page } from '../domain/pagination';
import type { FetchUsersResult, User } from '../domain/user';
import { ApiError } from './ApiError';
import type { ApiErrorDto, FetchUsersResponseDto, UserPageDto } from './dto';
import { toFetchUsersRequest, toFetchUsersResult, toListUsersQuery, toUserPage } from './mappers';
import type { ListUsersParams } from './params';

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '';

export async function fetchUsers(
  userIds: number[],
  signal?: AbortSignal,
): Promise<FetchUsersResult> {
  const response = await request('/api/users/fetch', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(toFetchUsersRequest(userIds)),
    signal: signal ?? null,
  });
  return toFetchUsersResult((await response.json()) as FetchUsersResponseDto);
}

export async function listUsers(
  params: ListUsersParams,
  signal?: AbortSignal,
): Promise<Page<User>> {
  const response = await request(`/api/users?${toListUsersQuery(params)}`, {
    method: 'GET',
    signal: signal ?? null,
  });
  return toUserPage((await response.json()) as UserPageDto);
}

async function request(path: string, init: RequestInit): Promise<Response> {
  const response = await fetch(`${BASE_URL}${path}`, init);
  if (!response.ok) {
    throw await toApiError(response);
  }
  return response;
}

async function toApiError(response: Response): Promise<ApiError> {
  try {
    const { error } = (await response.json()) as ApiErrorDto;
    return new ApiError(error.code, response.status, error.message, error.details, error.request_id);
  } catch {
    return new ApiError('unknown_error', response.status);
  }
}
