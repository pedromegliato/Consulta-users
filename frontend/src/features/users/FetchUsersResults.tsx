import type { FetchUsersResult } from '../../domain/user';
import { Card } from '../../ui';
import { FailedIdsList } from './FailedIdsList';
import { UsersTable } from './UsersTable';

interface FetchUsersResultsProps {
  result: FetchUsersResult;
}

export function FetchUsersResults({ result }: FetchUsersResultsProps) {
  return (
    <div className="results">
      <Card title={`Encontrados (${result.users.length})`}>
        <UsersTable users={result.users} />
      </Card>
      <Card title={`Falharam (${result.failed.length})`} tone="muted">
        <FailedIdsList failed={result.failed} />
      </Card>
    </div>
  );
}
