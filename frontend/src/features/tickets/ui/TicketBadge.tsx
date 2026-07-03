import type { ReactNode } from "react";

export function TicketBadge({ children, color }: { children: ReactNode; color: string }) {
  return (
    <span className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${color}`}>
      {children}
    </span>
  );
}
