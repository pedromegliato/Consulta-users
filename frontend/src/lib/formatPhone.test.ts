import { describe, expect, it } from 'vitest';

import { formatPhone } from './formatPhone';

describe('formatPhone', () => {
  it('formata celular brasileiro', () => {
    expect(formatPhone('11987654321')).toBe('(11) 98765-4321');
  });

  it('formata fixo brasileiro', () => {
    expect(formatPhone('1133334444')).toBe('(11) 3333-4444');
  });

  it('nao inventa mascara brasileira para numero estrangeiro', () => {
    expect(formatPhone('17707368031')).toBe('17707368031');
    expect(formatPhone('0106926593')).toBe('0106926593');
  });

  it('devolve os digitos quando o tamanho nao e reconhecido', () => {
    expect(formatPhone('123456789')).toBe('123456789');
  });

  it('indica ausencia quando nao ha telefone', () => {
    expect(formatPhone(null)).toBe('—');
  });
});
