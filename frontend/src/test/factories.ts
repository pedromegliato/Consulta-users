import type { FetchUsersResponseDto, UserDto } from '../api/dto';

export function buildUserDto(overrides: Partial<UserDto> = {}): UserDto {
  const id = overrides.id ?? 1;
  return {
    id,
    name: `User ${id}`,
    username: `user${id}`,
    email: `user${id}@example.com`,
    phone: '11987654321',
    ...overrides,
  };
}

export function buildFetchUsersResponseDto(
  overrides: Partial<FetchUsersResponseDto> = {},
): FetchUsersResponseDto {
  return {
    users: [buildUserDto({ id: 1 }), buildUserDto({ id: 2 })],
    failed: [3],
    ...overrides,
  };
}
