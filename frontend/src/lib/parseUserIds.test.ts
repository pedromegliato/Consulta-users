import { describe, expect, it } from 'vitest';

import { parseUserIds } from './parseUserIds';

describe('parseUserIds', () => {
  it('aceita separadores mistos e remove duplicados', () => {
    expect(parseUserIds('1, 2;3 4 2')).toEqual({ ids: [1, 2, 3, 4], invalidTokens: [] });
  });

  it('separa tokens que nao sao ids positivos', () => {
    expect(parseUserIds('1 abc -2 0 3.5')).toEqual({
      ids: [1],
      invalidTokens: ['abc', '-2', '0', '3.5'],
    });
  });

  it('retorna listas vazias para entrada em branco', () => {
    expect(parseUserIds('   ')).toEqual({ ids: [], invalidTokens: [] });
  });
});
