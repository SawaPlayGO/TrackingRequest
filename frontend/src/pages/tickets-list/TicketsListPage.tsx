import { useMemo, useState } from "react";
import { useTickets } from "../../features/tickets/model/useTickets";
import { useAuth } from "../../features/auth/model/useAuth";
import { TicketCard } from "../../features/tickets/ui/TicketCard";
import { TicketForm } from "../../features/tickets/ui/TicketForm";
import { TICKET_PRIORITIES, TICKET_STATUSES } from "../../shared/config/enums";

export function TicketsListPage() {
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<string>("");
  const [priorityFilter, setPriorityFilter] = useState<string>("");
  const [sortByDate, setSortByDate] = useState<"asc" | "desc">("desc");
  const [sortByPriority, setSortByPriority] = useState<"asc" | "desc" | "">("");
  const [formOpen, setFormOpen] = useState(false);

  const { auth, isAdmin } = useAuth();
  const { data, isLoading, isError, refetch, createTicket, updateStatus, deleteTicket } = useTickets({
    search: search || undefined,
    status: statusFilter || undefined,
    priority: priorityFilter || undefined,
    sortByDate,
    sortByPriority: sortByPriority || undefined,
  });

  const tickets = data?.items ?? [];

  const totalText = useMemo(() => {
    if (!data) return "";
    return `Найдено ${data.total} заявок`;
  }, [data]);

  return (
    <div className="space-y-6">
      <section className="rounded-3xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
            <label className="space-y-2">
              <span className="text-sm font-semibold text-slate-700">Поиск</span>
              <input
                type="search"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                className="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none transition focus:border-slate-400"
                placeholder="Название или описание"
              />
            </label>

            <label className="space-y-2">
              <span className="text-sm font-semibold text-slate-700">Статус</span>
              <select
                value={statusFilter}
                onChange={(event) => setStatusFilter(event.target.value)}
                className="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none"
              >
                <option value="">Все</option>
                {TICKET_STATUSES.map((status) => (
                  <option key={status.value} value={status.value}>
                    {status.label}
                  </option>
                ))}
              </select>
            </label>

            <label className="space-y-2">
              <span className="text-sm font-semibold text-slate-700">Приоритет</span>
              <select
                value={priorityFilter}
                onChange={(event) => setPriorityFilter(event.target.value)}
                className="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm outline-none"
              >
                <option value="">Все</option>
                {TICKET_PRIORITIES.map((priority) => (
                  <option key={priority.value} value={priority.value}>
                    {priority.label}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <button
              type="button"
              onClick={() => setSortByDate((current) => (current === "desc" ? "asc" : "desc"))}
              className="rounded-2xl bg-slate-900 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
            >
              Сортировать по дате: {sortByDate === "desc" ? "Сначала новые" : "Сначала старые"}
            </button>
            <button
              type="button"
              onClick={() =>
                setSortByPriority((current) => (current === "asc" ? "desc" : "asc"))
              }
              className="rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-semibold text-slate-900 transition hover:border-slate-300"
            >
              Приоритет: {sortByPriority || "не выбран"}
            </button>
            <button
              type="button"
              onClick={() => setFormOpen((open) => !open)}
              className="rounded-2xl bg-slate-900 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
            >
              {formOpen ? "Закрыть форму" : "Новая заявка"}
            </button>
          </div>
        </div>

        {formOpen && (
          <div className="mt-6 rounded-3xl border border-slate-200 bg-slate-50 p-5">
            <TicketForm
              onSubmit={async (payload) => {
                await createTicket(payload);
                refetch();
              }}
            />
          </div>
        )}
      </section>

      <section className="space-y-4">
        <div className="flex items-center justify-between gap-4 rounded-3xl bg-white px-6 py-4 shadow-sm ring-1 ring-slate-200">
          <p className="text-sm text-slate-600">{totalText}</p>
          <button
            type="button"
            onClick={() => refetch()}
            className="rounded-2xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-900 transition hover:border-slate-300"
          >
            Обновить
          </button>
        </div>

        {isLoading ? (
          <div className="rounded-3xl bg-white p-8 text-center text-slate-700 shadow-sm ring-1 ring-slate-200">
            Загружаем заявки...
          </div>
        ) : isError ? (
          <div className="rounded-3xl bg-rose-50 p-8 text-center text-rose-700 shadow-sm ring-1 ring-rose-200">
            Ошибка загрузки заявок. Пожалуйста, попробуйте позже.
          </div>
        ) : tickets.length === 0 ? (
          <div className="rounded-3xl bg-slate-50 p-8 text-center text-slate-700 shadow-sm ring-1 ring-slate-200">
            Список заявок пуст. Создайте первую заявку.
          </div>
        ) : (
          <div className="grid gap-4">
            {tickets.map((ticket) => (
              <TicketCard
                key={ticket.id}
                ticket={ticket}
                isAdmin={isAdmin}
                onStatusChange={async (status) => {
                  await updateStatus(ticket.id, status);
                  refetch();
                }}
                onDelete={isAdmin ? async () => {
                  await deleteTicket(ticket.id, auth ?? undefined);
                  refetch();
                } : undefined}
              />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
