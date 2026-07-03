import { describe, expect, it, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { TicketsListPage } from './TicketsListPage';

vi.mock('../../features/tickets/model/useTickets', () => ({
  useTickets: () => ({
    data: {
      items: [
        {
          id: 1,
          title: 'Test ticket',
          description: 'Description',
          status: 'new',
          priority: 'low',
          created_at: '2026-07-03T00:00:00Z',
          updated_at: '2026-07-03T00:00:00Z',
        },
      ],
      total: 1,
      page: 1,
      limit: 20,
      pages: 1,
    },
    isLoading: false,
    isError: false,
    refetch: vi.fn(),
    createTicket: vi.fn(),
    updateStatus: vi.fn(),
    deleteTicket: vi.fn(),
  }),
}));

vi.mock('../../features/auth/model/useAuth', () => ({
  useAuth: () => ({ auth: { username: 'admin', password: 'admin' }, isAdmin: true }),
}));

describe('TicketsListPage', () => {
  it('renders ticket list with a ticket card', () => {
    render(<TicketsListPage />);

    expect(screen.getByText(/Найдено 1 заявок/i)).toBeInTheDocument();
    expect(screen.getByText(/Test ticket/)).toBeInTheDocument();
  });
});
