import type { TicketCreatePayload, TicketListResponse, TicketResponse, TicketStatusUpdatePayload } from "./types";
import { apiClient } from "../../../shared/api/client";

const BASE_URL = "/tickets";

function getAuthorizationHeader(auth: { username: string; password: string }) {
  return `Basic ${window.btoa(`${auth.username}:${auth.password}`)}`;
}

export async function getTickets(params: {
  page: number;
  limit: number;
  status?: string;
  priority?: string;
  sort_by_date: "asc" | "desc";
  sort_by_priority?: "asc" | "desc";
  search?: string;
}): Promise<TicketListResponse> {
  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== "") {
      searchParams.set(key, String(value));
    }
  });
  const response = await apiClient.get<TicketListResponse>(`${BASE_URL}/?${searchParams.toString()}`);
  return response.data;
}

export async function createTicket(payload: TicketCreatePayload): Promise<TicketResponse> {
  const response = await apiClient.post<TicketResponse>(BASE_URL + "/", payload);
  return response.data;
}

export async function updateTicketStatus(ticketId: number, payload: TicketStatusUpdatePayload): Promise<TicketResponse> {
  const response = await apiClient.patch<TicketResponse>(`${BASE_URL}/${ticketId}/status`, payload);
  return response.data;
}

export async function deleteTicket(ticketId: number, auth?: { username: string; password: string }): Promise<void> {
  const headers = auth
    ? { Authorization: getAuthorizationHeader(auth) }
    : undefined;
  await apiClient.delete(`${BASE_URL}/${ticketId}`, {
    headers,
  });
}
