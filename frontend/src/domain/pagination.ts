export type SortDirection = 'asc' | 'desc';

export type UserSortField = 'id' | 'name' | 'username' | 'email';

export interface SortState<TField extends string> {
  field: TField;
  direction: SortDirection;
}

export interface Page<TItem> {
  items: TItem[];
  page: number;
  pageSize: number;
  total: number;
  totalPages: number;
}

export function nextSortState<TField extends string>(
  current: SortState<TField>,
  field: TField,
): SortState<TField> {
  if (current.field !== field) {
    return { field, direction: 'asc' };
  }
  return { field, direction: current.direction === 'asc' ? 'desc' : 'asc' };
}
