import type { ReactNode } from 'react';

import { cx } from './classNames';

export type CardTone = 'default' | 'muted';

interface CardProps {
  title?: ReactNode;
  footer?: ReactNode;
  tone?: CardTone;
  className?: string;
  children: ReactNode;
}

export function Card({ title, footer, tone = 'default', className, children }: CardProps) {
  return (
    <section className={cx('card', `card--${tone}`, className)}>
      {title !== undefined && <h2 className="card__title">{title}</h2>}
      <div className="card__body">{children}</div>
      {footer !== undefined && <div className="card__footer">{footer}</div>}
    </section>
  );
}
