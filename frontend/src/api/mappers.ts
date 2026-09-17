import type { Page } from '../domain/pagination';
import type { FetchUsersResult, User } from '../domain/user';
import type {
  FetchUsersRequestDto,
  FetchUsersResponseDto,
  UserDto,
  UserPageDto,
} from './dto';
import type { ListUsersParams } from './params';

export function toFetchUsersRequest(userIds: number[]): FetchUsersRequestDto {
  return { user_ids: userIds };
}

export function toUser(dto: UserDto): User {
  return {
    id: dto.id,
    name: dto.name,
    username: dto.username,
    email: dto.email,
    phone: dto.phone ?? null,
  };
}

export function toFetchUsersResult(dto: FetchUsersResponseDto): FetchUsersResult {
  return { users: dto.users.map(toUser), failed: dto.failed };
}

export function toUserPage(dto: UserPageDto): Page<User> {
  return {
    items: dto.items.map(toUser),
    page: dto.page,
    pageSize: dto.page_size,
    total: dto.total,
    totalPages: dto.total_pages,
  };
}

export function toListUsersQuery(params: ListUsersParams): string {
  const query = new URLSearchParams({
    sort_by: params.sortBy,
    sort_direction: params.sortDirection,
    page: String(params.page),
    page_size: String(params.pageSize),
  });

  const search = params.search.trim();
  if (search.length > 0) {
    query.set('search', search);
  }
  return query.toString();
}
