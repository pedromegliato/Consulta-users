import type { SortDirection, UserSortField } from '../domain/pagination';

export interface ListUsersParams {
  search: string;
  sortBy: UserSortField;
  sortDirection: SortDirection;
  page: number;
  pageSize: number;
}
