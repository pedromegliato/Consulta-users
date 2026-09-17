import { useCallback, useEffect, useState } from 'react';

import { listUsers } from '../api/usersClient';
import type { Page, SortState, UserSortField } from '../domain/pagination';
import { nextSortState } from '../domain/pagination';
import type { User } from '../domain/user';
import { toUserFacingError } from '../lib/errorMessages';
import type { UserFacingError } from '../lib/errorMessages';
import { useDebouncedValue } from './useDebouncedValue';

export const PAGE_SIZE_OPTIONS = [5, 10, 20, 50];

const SEARCH_DEBOUNCE_MS = 350;
const FIRST_PAGE = 1;
const DEFAULT_PAGE_SIZE = 10;

export type UsersDirectoryState =
  | { status: 'loading' }
  | { status: 'success'; page: Page<User> }
  | { status: 'error'; error: UserFacingError };

export interface UsersDirectoryController {
  state: UsersDirectoryState;
  search: string;
  sort: SortState<UserSortField>;
  pageSize: number;
  changeSearch: (value: string) => void;
  toggleSort: (field: UserSortField) => void;
  changePage: (page: number) => void;
  changePageSize: (pageSize: number) => void;
  refresh: () => void;
}

export function useUsersDirectory(): UsersDirectoryController {
  const [search, setSearch] = useState('');
  const [sort, setSort] = useState<SortState<UserSortField>>({ field: 'id', direction: 'asc' });
  const [page, setPage] = useState(FIRST_PAGE);
  const [pageSize, setPageSize] = useState(DEFAULT_PAGE_SIZE);
  const [reloadToken, setReloadToken] = useState(0);
  const [state, setState] = useState<UsersDirectoryState>({ status: 'loading' });

  const debouncedSearch = useDebouncedValue(search, SEARCH_DEBOUNCE_MS);

  useEffect(() => {
    const controller = new AbortController();
    setState({ status: 'loading' });

    listUsers(
      { search: debouncedSearch, sortBy: sort.field, sortDirection: sort.direction, page, pageSize },
      controller.signal,
    )
      .then((result) => setState({ status: 'success', page: result }))
      .catch((error: unknown) => {
        if (!controller.signal.aborted) {
          setState({ status: 'error', error: toUserFacingError(error) });
        }
      });

    return () => controller.abort();
  }, [debouncedSearch, sort, page, pageSize, reloadToken]);

  const changeSearch = useCallback((value: string) => {
    setSearch(value);
    setPage(FIRST_PAGE);
  }, []);

  const toggleSort = useCallback((field: UserSortField) => {
    setSort((current) => nextSortState(current, field));
    setPage(FIRST_PAGE);
  }, []);

  const changePageSize = useCallback((value: number) => {
    setPageSize(value);
    setPage(FIRST_PAGE);
  }, []);

  const refresh = useCallback(() => setReloadToken((token) => token + 1), []);

  return {
    state,
    search,
    sort,
    pageSize,
    changeSearch,
    toggleSort,
    changePage: setPage,
    changePageSize,
    refresh,
  };
}
