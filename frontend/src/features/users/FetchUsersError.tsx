import type { UserFacingError } from '../../lib/errorMessages';
import { Alert } from '../../ui';

interface FetchUsersErrorProps {
  error: UserFacingError;
  onRetry: () => void;
}

export function FetchUsersError({ error, onRetry }: FetchUsersErrorProps) {
  return (
    <Alert variant="error" title="Não foi possível consultar" onRetry={onRetry}>
      <p className="alert__message">{error.message}</p>

      {error.details.length > 0 && (
        <details className="alert__details">
          <summary>Detalhes técnicos</summary>
          <ul>
            {error.details.map((detail) => (
              <li key={detail}>{detail}</li>
            ))}
          </ul>
        </details>
      )}

      {error.requestId !== null && (
        <p className="alert__reference">Código de referência: {error.requestId}</p>
      )}
    </Alert>
  );
}
