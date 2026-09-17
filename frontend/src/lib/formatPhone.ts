const NOT_AVAILABLE = '—';

const BRAZILIAN_MOBILE = /^([1-9]{2})(9\d{4})(\d{4})$/;
const BRAZILIAN_LANDLINE = /^([1-9]{2})([2-5]\d{3})(\d{4})$/;

export function formatPhone(digits: string | null): string {
  if (digits === null || digits.length === 0) {
    return NOT_AVAILABLE;
  }

  const match = BRAZILIAN_MOBILE.exec(digits) ?? BRAZILIAN_LANDLINE.exec(digits);
  if (match === null) {
    return digits;
  }

  const [, areaCode, prefix, suffix] = match;
  return `(${areaCode}) ${prefix}-${suffix}`;
}
