import { useId } from 'react';
import type { InputHTMLAttributes, ReactNode } from 'react';

import { cx } from './classNames';

interface TextFieldProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'id'> {
  label: string;
  hint?: ReactNode;
  invalid?: boolean;
}

export function TextField({ label, hint, invalid = false, className, ...rest }: TextFieldProps) {
  const inputId = useId();
  const hintId = `${inputId}-hint`;

  return (
    <div className="field">
      <label className="field__label" htmlFor={inputId}>
        {label}
      </label>
      <input
        id={inputId}
        className={cx('field__input', invalid && 'field__input--invalid', className)}
        aria-describedby={hint !== undefined ? hintId : undefined}
        aria-invalid={invalid || undefined}
        {...rest}
      />
      {hint !== undefined && (
        <p id={hintId} className={cx('field__hint', invalid && 'field__hint--invalid')}>
          {hint}
        </p>
      )}
    </div>
  );
}
