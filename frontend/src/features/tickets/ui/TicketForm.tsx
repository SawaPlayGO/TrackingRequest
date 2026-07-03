import { useState } from "react";
import { TICKET_PRIORITIES, TICKET_STATUSES } from "../../../shared/config/enums";
import type { TicketCreatePayload } from "../api/types";

export function TicketForm({
  onSubmit,
}: {
  onSubmit: (payload: TicketCreatePayload) => Promise<void>;
}) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [status, setStatus] = useState<string>("new");
  const [priority, setPriority] = useState<string>("normal");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsSubmitting(true);

    await onSubmit({
      title,
      description,
      status: status as TicketCreatePayload["status"],
      priority: priority as TicketCreatePayload["priority"],
    });

    setTitle("");
    setDescription("");
    setStatus("new");
    setPriority("normal");
    setIsSubmitting(false);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <div className="grid gap-4 sm:grid-cols-2">
        <label className="space-y-2">
          <span className="text-sm font-semibold text-slate-700">Название</span>
          <input
            type="text"
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none focus:border-slate-400"
            required
            minLength={3}
          />
        </label>
        <label className="space-y-2">
          <span className="text-sm font-semibold text-slate-700">Статус</span>
          <select
            value={status}
            onChange={(event) => setStatus(event.target.value)}
            className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none"
          >
            {TICKET_STATUSES.map((statusOption) => (
              <option key={statusOption.value} value={statusOption.value}>
                {statusOption.label}
              </option>
            ))}
          </select>
        </label>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <label className="space-y-2">
          <span className="text-sm font-semibold text-slate-700">Приоритет</span>
          <select
            value={priority}
            onChange={(event) => setPriority(event.target.value)}
            className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none"
          >
            {TICKET_PRIORITIES.map((priorityOption) => (
              <option key={priorityOption.value} value={priorityOption.value}>
                {priorityOption.label}
              </option>
            ))}
          </select>
        </label>
      </div>

      <label className="space-y-2">
        <span className="text-sm font-semibold text-slate-700">Описание</span>
        <textarea
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          className="min-h-[120px] w-full rounded-3xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none focus:border-slate-400"
          rows={4}
        />
      </label>

      <div className="flex justify-end">
        <button
          type="submit"
          disabled={isSubmitting}
          className="rounded-2xl bg-slate-900 px-6 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isSubmitting ? "Сохранение..." : "Создать заявку"}
        </button>
      </div>
    </form>
  );
}
