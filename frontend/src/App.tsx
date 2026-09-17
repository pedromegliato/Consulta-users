import { FetchUsersError } from './features/users/FetchUsersError';
import { FetchUsersResults } from './features/users/FetchUsersResults';
import { UserIdsForm } from './features/users/UserIdsForm';
import { UsersDirectory } from './features/users/UsersDirectory';
import { useFetchUsers } from './hooks/useFetchUsers';
import { useUsersDirectory } from './hooks/useUsersDirectory';
import { Spinner } from './ui';

export function App() {
  const directory = useUsersDirectory();
  const { state, run, retry } = useFetchUsers(directory.refresh);

  return (
    <main className="page">
      <header className="page__header">
        <h1>Consulta de usuários</h1>
        <p>Informe os IDs e consulte vários usuários de uma vez.</p>
      </header>

      <UserIdsForm loading={state.status === 'loading'} onSubmit={run} />

      <div aria-live="polite">
        {state.status === 'loading' && <Spinner label="Consultando usuários..." />}

        {state.status === 'error' && <FetchUsersError error={state.error} onRetry={retry} />}

        {state.status === 'success' && <FetchUsersResults result={state.result} />}
      </div>

      <UsersDirectory controller={directory} />
    </main>
  );
}
