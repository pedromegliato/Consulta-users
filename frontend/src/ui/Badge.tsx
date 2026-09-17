import type { ReactNode } from 'react';

import { cx } from './classNames';

export type BadgeVariant = 'neutral' | 'success' | 'danger' | 'warning';

interface BadgeProps {
  variant?: BadgeVariant;
  children: ReactNode;
}

export function Badge({ variant = 'neutral', children }: BadgeProps) {
  return <span className={cx('badge', `badge--${variant}`)}>{children}</span>;
}
