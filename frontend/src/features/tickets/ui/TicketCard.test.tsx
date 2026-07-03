import { describe, expect, it, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { TicketCard } from './TicketCard';
import type { TicketResponse } from '../api/types';

const ticket: TicketResponse = {
  id: 1,
  title: 'Test ticket',
  description: 'Test description',
  status: 'new',
  priority: 'low',
  created_at: '2026-07-03T00:00:00Z',
  updated_at: '2026-07-03T00:00:00Z',
};

describe('TicketCard', () => {
  it('renders ticket information and delete button for admin', () => {
    const onStatusChange = vi.fn();
    const onDelete = vi.fn();

    render(<TicketCard ticket={ticket} isAdmin onStatusChange={onStatusChange} onDelete={onDelete} />);

    expect(screen.getByText(/Test ticket/)).toBeInTheDocument();
    expect(screen.getByText(/Test description/)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Удалить/i })).toBeInTheDocument();
  });

  it('does not render delete button for non-admin', () => {
    const onStatusChange = vi.fn();

    render(<TicketCard ticket={ticket} isAdmin={false} onStatusChange={onStatusChange} />);

    expect(screen.queryByRole('button', { name: /Удалить/i })).not.toBeInTheDocument();
  });
});
