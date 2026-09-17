import type { UserSortField } from '../../domain/pagination';
import type { User } from '../../domain/user';
import type { UsersDirectoryController } from '../../hooks/useUsersDirectory';
import { PAGE_SIZE_OPTIONS } from '../../hooks/useUsersDirectory';
import { formatPhone } from '../../lib/formatPhone';
import {
  Alert,
  Button,
  Card,
  DataTable,
  EmptyState,
  Pagination,
  Select,
  Spinner,
  TextField,
} from '../../ui';
import type { Column } from '../../ui';

const COLUMNS: Column<User, UserSortField>[] = [
  { header: 'ID', render: (user) => user.id, sortField: 'id' },
  { header: 'Nome', render: (user) => user.name, sortField: 'name' },
  { header: 'Usuário', render: (user) => user.username, sortField: 'username' },
  { header: 'E-mail', render: (user) => user.email, sortField: 'email' },
  { header: 'Telefone', render: (user) => formatPhone(user.phone) },
];

const SORTABLE_COLUMNS = COLUMNS.filter((column) => column.sortField !== undefined);

interface UsersDirectoryProps {
  controller: UsersDirectoryController;
}

export function UsersDirectory({ controller }: UsersDirectoryProps) {
  const { state, search, sort, pageSize, toggleSort } = controller;

  return (
    <Card title="Usuários armazenados">
      <TextField
        label="Buscar"
        type="search"
        value={search}
        onChange={(event) => controller.changeSearch(event.target.value)}
        placeholder="ID, nome, usuário, e-mail ou telefone"
        hint="Busca em qualquer campo. Busca, ordenação e paginação são resolvidas no servidor."
      />

      <div className="sort-controls">
        <Select
          label="Ordenar por"
          value={sort.field}
          onChange={(event) => toggleSort(event.target.value as UserSortField)}
        >
          {SORTABLE_COLUMNS.map((column) => (
            <option key={column.header} value={column.sortField}>
              {column.header}
            </option>
          ))}
        </Select>
        <Button
          type="button"
          variant="secondary"
          size="sm"
          onClick={() => toggleSort(sort.field)}
          aria-label={`Inverter ordenação, atualmente ${directionLabel(sort.direction)}`}
        >
          {directionLabel(sort.direction)}
        </Button>
      </div>

      {state.status === 'loading' && <Spinner label="Carregando usuários..." />}

      {state.status === 'error' && <Alert variant="error">{state.error.message}</Alert>}

      {state.status === 'success' && (
        <>
          {state.page.items.length === 0 ? (
            <EmptyState message="Nenhum usuário armazenado corresponde à busca." />
          ) : (
            <DataTable
              columns={COLUMNS}
              rows={state.page.items}
              rowKey={(user) => user.id}
              sort={sort}
              onSort={toggleSort}
            />
          )}

          <Pagination
            page={state.page.page}
            pageSize={pageSize}
            total={state.page.total}
            totalPages={state.page.totalPages}
            pageSizeOptions={PAGE_SIZE_OPTIONS}
            onPageChange={controller.changePage}
            onPageSizeChange={controller.changePageSize}
          />
        </>
      )}
    </Card>
  );
}

function directionLabel(direction: string): string {
  return direction === 'asc' ? 'Crescente ↑' : 'Decrescente ↓';
}
