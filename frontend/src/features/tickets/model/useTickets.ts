import { useMutation, useQuery } from "@tanstack/react-query";
import { createTicket, deleteTicket, getTickets, updateTicketStatus } from "../api/ticketsApi";
import type { TicketCreatePayload, TicketStatus, TicketListResponse } from "../api/types";

const DEFAULT_OPTIONS = {
  page: 1,
  limit: 20,
};

type UseTicketsParams = {
  search?: string;
  status?: string;
  priority?: string;
  sortByDate: "asc" | "desc";
  sortByPriority?: "asc" | "desc";
};

export function useTickets(params: UseTicketsParams) {
  const queryKey = ["tickets", params] as const;

  const queryFn = () =>
    getTickets({
      ...DEFAULT_OPTIONS,
      status: params.status,
      priority: params.priority,
      sort_by_date: params.sortByDate,
      sort_by_priority: params.sortByPriority,
      search: params.search,
    });

  const query = useQuery<TicketListResponse, Error>({
    queryKey,
    queryFn,
  });

  const createMutation = useMutation({
    mutationFn: createTicket,
  });

  const statusMutation = useMutation({
    mutationFn: ({ ticketId, status }: { ticketId: number; status: TicketStatus }) =>
      updateTicketStatus(ticketId, { status }),
  });

  const deleteMutation = useMutation({
    mutationFn: ({ ticketId, auth }: { ticketId: number; auth?: { username: string; password: string } }) =>
      deleteTicket(ticketId, auth),
  });

  return {
    ...query,
    createTicket: async (payload: TicketCreatePayload) => await createMutation.mutateAsync(payload),
    updateStatus: async (ticketId: number, status: TicketStatus) => await statusMutation.mutateAsync({ ticketId, status }),
    deleteTicket: async (ticketId: number, auth?: { username: string; password: string }) =>
      await deleteMutation.mutateAsync({ ticketId, auth }),
  };
}
