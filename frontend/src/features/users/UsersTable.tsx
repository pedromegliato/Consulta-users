import type { User } from '../../domain/user';
import { formatPhone } from '../../lib/formatPhone';
import { DataTable, EmptyState } from '../../ui';
import type { Column } from '../../ui';

const COLUMNS: Column<User>[] = [
  { header: 'ID', render: (user) => user.id },
  { header: 'Nome', render: (user) => user.name },
  { header: 'Usuário', render: (user) => user.username },
  { header: 'E-mail', render: (user) => user.email },
  { header: 'Telefone', render: (user) => formatPhone(user.phone) },
];

interface UsersTableProps {
  users: User[];
}

export function UsersTable({ users }: UsersTableProps) {
  if (users.length === 0) {
    return <EmptyState message="Nenhum usuário foi retornado pelo provider." />;
  }
  return <DataTable columns={COLUMNS} rows={users} rowKey={(user) => user.id} />;
}
