import { useState } from "react";
import { LoginForm } from "../../features/auth/ui/LoginForm";

export function LoginPage() {
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  return (
    <div className="rounded-3xl bg-white p-8 shadow-sm ring-1 ring-slate-200">
      <h2 className="text-2xl font-semibold text-slate-900">Вход администратора</h2>
      <p className="mt-2 text-sm text-slate-600">
        Используйте имя пользователя и пароль администратора для удаления заявок.
      </p>

      <div className="mt-6 max-w-xl">
        <LoginForm
          onSuccess={() => {
            setSuccess(true);
            setError(null);
          }}
          onError={(message) => setError(message)}
        />
      </div>

      {success && (
        <div className="mt-6 rounded-3xl border border-emerald-200 bg-emerald-50 p-4 text-emerald-900">
          Успешный вход. Теперь вы можете удалять заявки через список.
        </div>
      )}
      {error && (
        <div className="mt-6 rounded-3xl border border-rose-200 bg-rose-50 p-4 text-rose-900">
          {error}
        </div>
      )}
    </div>
  );
}
