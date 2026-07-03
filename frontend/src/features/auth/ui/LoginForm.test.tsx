import { describe, expect, it, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { LoginForm } from './LoginForm';

vi.mock('../model/useAuth', () => ({
  useAuth: () => ({
    login: vi.fn().mockResolvedValue(undefined),
    isLoading: false,
  }),
}));

describe('LoginForm', () => {
  it('renders login fields and submits credentials', async () => {
    const onSuccess = vi.fn();
    const onError = vi.fn();
    const { container } = render(<LoginForm onSuccess={onSuccess} onError={onError} />);

    expect(screen.getByLabelText(/Имя пользователя/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Пароль/i)).toBeInTheDocument();

    fireEvent.change(screen.getByLabelText(/Имя пользователя/i), { target: { value: 'admin' } });
    fireEvent.change(screen.getByLabelText(/Пароль/i), { target: { value: 'admin' } });

    fireEvent.submit(container.querySelector('form')!);

    await waitFor(() => {
      expect(onSuccess).toHaveBeenCalled();
    });

    expect(onError).not.toHaveBeenCalled();
  });
});
