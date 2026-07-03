export type TicketStatus = "new" | "in_progress" | "done";
export type TicketPriority = "low" | "normal" | "high";

export type TicketResponse = {
  id: number;
  title: string;
  description?: string | null;
  status: TicketStatus;
  priority: TicketPriority;
  created_at: string;
  updated_at: string;
};

export type TicketListResponse = {
  items: TicketResponse[];
  total: number;
  page: number;
  limit: number;
  pages: number;
};

export type TicketCreatePayload = {
  title: string;
  description?: string;
  status: TicketStatus;
  priority: TicketPriority;
};

export type TicketStatusUpdatePayload = {
  status: TicketStatus;
};
