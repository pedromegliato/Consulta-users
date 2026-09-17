import { Badge, EmptyState } from '../../ui';

interface FailedIdsListProps {
  failed: number[];
}

export function FailedIdsList({ failed }: FailedIdsListProps) {
  if (failed.length === 0) {
    return <EmptyState message="Nenhuma falha nesta consulta." />;
  }

  return (
    <ul className="badge-list">
      {failed.map((userId) => (
        <li key={userId}>
          <Badge variant="danger">{userId}</Badge>
        </li>
      ))}
    </ul>
  );
}
