import type { ReactNode } from 'react';

import { Button } from './Button';
import { cx } from './classNames';

export type AlertVariant = 'error' | 'warning' | 'info';

interface AlertProps {
  variant?: AlertVariant;
  title?: string;
  onRetry?: () => void;
  children: ReactNode;
}

export function Alert({ variant = 'info', title, onRetry, children }: AlertProps) {
  return (
    <div
      className={cx('alert', `alert--${variant}`)}
      role={variant === 'error' ? 'alert' : 'status'}
    >
      {title !== undefined && <strong className="alert__title">{title}</strong>}
      <div className="alert__content">{children}</div>
      {onRetry !== undefined && (
        <Button type="button" variant="secondary" size="sm" onClick={onRetry}>
          Tentar novamente
        </Button>
      )}
    </div>
  );
}
