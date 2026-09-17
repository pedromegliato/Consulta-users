import type { Key, ReactNode } from 'react';

import type { SortState } from '../domain/pagination';
import { cx } from './classNames';

export interface Column<TRow, TField extends string = string> {
  header: string;
  render: (row: TRow) => ReactNode;
  sortField?: TField;
}

interface DataTableProps<TRow, TField extends string> {
  columns: Column<TRow, TField>[];
  rows: TRow[];
  rowKey: (row: TRow) => Key;
  sort?: SortState<TField>;
  onSort?: (field: TField) => void;
}

export function DataTable<TRow, TField extends string>({
  columns,
  rows,
  rowKey,
  sort,
  onSort,
}: DataTableProps<TRow, TField>) {
  return (
    <table className="table">
      <thead>
        <tr>
          {columns.map((column) => {
            const field = column.sortField;
            const sorted = field !== undefined && sort?.field === field;

            if (field === undefined || onSort === undefined) {
              return <th key={column.header}>{column.header}</th>;
            }

            return (
              <th key={column.header} aria-sort={ariaSort(sorted, sort?.direction)}>
                <button
                  type="button"
                  className={cx('table__sort', sorted && 'table__sort--active')}
                  onClick={() => onSort(field)}
                >
                  {column.header}
                  <span aria-hidden="true">{sorted ? indicator(sort?.direction) : '↕'}</span>
                </button>
              </th>
            );
          })}
        </tr>
      </thead>
      <tbody>
        {rows.map((row) => (
          <tr key={rowKey(row)}>
            {columns.map((column) => (
              <td key={column.header} data-label={column.header}>
                {column.render(row)}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

function ariaSort(sorted: boolean, direction?: string): 'ascending' | 'descending' | 'none' {
  if (!sorted) {
    return 'none';
  }
  return direction === 'desc' ? 'descending' : 'ascending';
}

function indicator(direction?: string): string {
  return direction === 'desc' ? '↓' : '↑';
}
