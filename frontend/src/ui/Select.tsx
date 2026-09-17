import { useId } from 'react';
import type { ReactNode, SelectHTMLAttributes } from 'react';

interface SelectProps extends Omit<SelectHTMLAttributes<HTMLSelectElement>, 'id'> {
  label: string;
  children: ReactNode;
}

export function Select({ label, children, ...rest }: SelectProps) {
  const selectId = useId();

  return (
    <div className="select">
      <label className="select__label" htmlFor={selectId}>
        {label}
      </label>
      <select id={selectId} className="select__control" {...rest}>
        {children}
      </select>
    </div>
  );
}
