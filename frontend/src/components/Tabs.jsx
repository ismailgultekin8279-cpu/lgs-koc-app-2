import React from "react";

function cx(...classes) {
  return classes.filter(Boolean).join(" ");
}

/**
 * Tabs
 * Props:
 * - tabs: [{ key: string, label: string }]
 * - value: active tab key
 * - onChange: (key) => void
 * - className: optional wrapper classes
 */
export default function Tabs({ tabs, value, onChange, className }) {
  return (
    <div className={cx("inline-flex rounded-2xl bg-slate-100 p-1", className)} role="tablist">
      {tabs.map((t) => {
        const isActive = t.key === value;

        return (
          <button
            key={t.key}
            type="button"
            role="tab"
            aria-selected={isActive}
            onClick={() => onChange(t.key)}
            className={cx(
              "px-4 py-2 text-sm font-medium rounded-2xl transition-colors",
              isActive
                ? "bg-white text-slate-900 shadow-sm"
                : "text-slate-600 hover:text-slate-900"
            )}
          >
            {t.label}
          </button>
        );
      })}
    </div>
  );
}
