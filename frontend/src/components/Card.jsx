import React from "react";

/**
 * Minimal className merge helper.
 * We keep it local to avoid extra dependencies.
 */
function cx(...classes) {
  return classes.filter(Boolean).join(" ");
}

export function Card({ className, children, ...props }) {
  return (
    <section className={cx("card", className)} {...props}>
      {children}
    </section>
  );
}

export function CardHeader({ className, title, subtitle, right, children, ...props }) {
  return (
    <div className={cx("card-header", className)} {...props}>
      <div className="min-w-0">
        {title ? <div className="card-title">{title}</div> : null}
        {subtitle ? <div className="card-subtitle">{subtitle}</div> : null}
        {children ? <div className="mt-3">{children}</div> : null}
      </div>

      {right ? <div className="shrink-0">{right}</div> : null}
    </div>
  );
}

export function CardBody({ className, children, ...props }) {
  return (
    <div className={cx("card-body", className)} {...props}>
      {children}
    </div>
  );
}

export function InfoBox({ className, title, description, ...props }) {
  return (
    <div
      className={cx(
        "rounded-2xl border border-slate-100 bg-slate-50 p-4",
        className
      )}
      {...props}
    >
      {title ? <div className="text-sm font-medium text-slate-900">{title}</div> : null}
      {description ? (
        <div className="mt-1 text-sm text-slate-600">{description}</div>
      ) : null}
    </div>
  );
}
