export interface ParsedUserIds {
  ids: number[];
  invalidTokens: string[];
}

const SEPARATORS = /[\s,;]+/;

export function parseUserIds(raw: string): ParsedUserIds {
  const ids: number[] = [];
  const invalidTokens: string[] = [];

  for (const token of raw.split(SEPARATORS).filter(Boolean)) {
    const value = Number(token);
    if (!Number.isInteger(value) || value <= 0) {
      invalidTokens.push(token);
    } else if (!ids.includes(value)) {
      ids.push(value);
    }
  }

  return { ids, invalidTokens };
}
