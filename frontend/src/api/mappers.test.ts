import { describe, expect, it } from 'vitest';

import { nextSortState } from '../domain/pagination';
import { toListUsersQuery } from './mappers';

const BASE_PARAMS = {
  search: '',
  sortBy: 'id',
  sortDirection: 'asc',
  page: 1,
  pageSize: 10,
} as const;

describe('toListUsersQuery', () => {
  it('envia paginacao e ordenacao no formato do backend', () => {
    expect(toListUsersQuery({ ...BASE_PARAMS, page: 3, pageSize: 20 })).toBe(
      'sort_by=id&sort_direction=asc&page=3&page_size=20',
    );
  });

  it('omite a busca quando ela esta vazia', () => {
    expect(toListUsersQuery({ ...BASE_PARAMS, search: '   ' })).not.toContain('search');
  });

  it('inclui a busca sem espacos em branco nas pontas', () => {
    expect(toListUsersQuery({ ...BASE_PARAMS, search: '  ana  ' })).toContain('search=ana');
  });
});

describe('nextSortState', () => {
  it('inverte a direcao ao clicar na mesma coluna', () => {
    expect(nextSortState({ field: 'name', direction: 'asc' }, 'name')).toEqual({
      field: 'name',
      direction: 'desc',
    });
  });

  it('comeca ascendente ao trocar de coluna', () => {
    expect(nextSortState({ field: 'name', direction: 'desc' }, 'email')).toEqual({
      field: 'email',
      direction: 'asc',
    });
  });
});
