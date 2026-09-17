import { useMemo, useState } from 'react';
import type { FormEvent } from 'react';

import { parseUserIds } from '../../lib/parseUserIds';
import { Button, Card, TextField } from '../../ui';

interface UserIdsFormProps {
  loading: boolean;
  onSubmit: (userIds: number[]) => void;
}

export function UserIdsForm({ loading, onSubmit }: UserIdsFormProps) {
  const [value, setValue] = useState('1, 2, 3, 4');
  const { ids, invalidTokens } = useMemo(() => parseUserIds(value), [value]);

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    onSubmit(ids);
  };

  return (
    <Card title="IDs para consulta">
      <form onSubmit={handleSubmit}>
        <TextField
          label="IDs de usuários"
          value={value}
          onChange={(event) => setValue(event.target.value)}
          placeholder="1, 2, 3"
          inputMode="numeric"
          autoComplete="off"
          invalid={invalidTokens.length > 0}
          hint={buildHint(ids.length, invalidTokens)}
        />
        <Button type="submit" loading={loading} disabled={ids.length === 0} fullWidth>
          {loading ? 'Consultando...' : 'Consultar'}
        </Button>
      </form>
    </Card>
  );
}

function buildHint(validCount: number, invalidTokens: string[]): string {
  const base = `Separe por vírgula, espaço ou ponto e vírgula. ${validCount} ID(s) válido(s).`;
  if (invalidTokens.length === 0) {
    return base;
  }
  return `${base} Ignorados: ${invalidTokens.join(', ')}.`;
}
