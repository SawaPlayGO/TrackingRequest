import { TICKET_STATUSES } from "../../../shared/config/enums";
import { TicketBadge } from "./TicketBadge";
import type { TicketResponse } from "../api/types";

const badgeClasses: Record<string, string> = {
  new: "bg-sky-100 text-sky-800",
  in_progress: "bg-amber-100 text-amber-800",
  done: "bg-emerald-100 text-emerald-800",
  low: "bg-slate-100 text-slate-800",
  normal: "bg-indigo-100 text-indigo-800",
  high: "bg-rose-100 text-rose-800",
};

export function TicketCard({
  ticket,
  onStatusChange,
  onDelete,
  isAdmin,
}: {
  ticket: TicketResponse;
  onStatusChange: (status: TicketResponse["status"]) => Promise<void>;
  onDelete?: () => Promise<void>;
  isAdmin: boolean;
}) {
  return (
    <article className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div className="space-y-3">
          <div className="flex flex-wrap gap-2">
            <TicketBadge color={badgeClasses[ticket.status]}>{ticket.status.replace("_", " ")}</TicketBadge>
            <TicketBadge color={badgeClasses[ticket.priority]}>{ticket.priority}</TicketBadge>
          </div>
          <h3 className="text-xl font-semibold text-slate-900">{ticket.title}</h3>
          <p className="text-sm leading-6 text-slate-600">{ticket.description || "Описание отсутствует"}</p>
        </div>

        <div className="flex flex-col gap-3">
          {isAdmin && onDelete ? (
            <button
              type="button"
              onClick={() => onDelete()}
              className="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-2 text-sm font-semibold text-rose-700 transition hover:bg-rose-100"
            >
              Удалить
            </button>
          ) : null}
          <select
            value={ticket.status}
            onChange={(event) => onStatusChange(event.target.value as TicketResponse["status"])}
            className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none"
          >
            {TICKET_STATUSES.map((status) => (
              <option key={status.value} value={status.value}>
                {status.label}
              </option>
            ))}
          </select>
        </div>
      </div>
    </article>
  );
}
