import { useState } from "react";
import { useAuth } from "../model/useAuth";

export function LoginForm({
  onSuccess,
  onError,
}: {
  onSuccess: () => void;
  onError: (message: string) => void;
}) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { login, isLoading } = useAuth();

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
      await login(username, password);
      onSuccess();
    } catch {
      onError("Неверное имя пользователя или пароль.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5 rounded-3xl border border-slate-200 bg-slate-50 p-6">
      <label className="space-y-2">
        <span className="text-sm font-semibold text-slate-700">Имя пользователя</span>
        <input
          type="text"
          value={username}
          onChange={(event) => setUsername(event.target.value)}
          className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none focus:border-slate-400"
          required
        />
      </label>
      <label className="space-y-2">
        <span className="text-sm font-semibold text-slate-700">Пароль</span>
        <input
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          className="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm outline-none focus:border-slate-400"
          required
        />
      </label>
      <div className="flex justify-end">
        <button
          type="submit"
          disabled={isLoading}
          className="rounded-2xl bg-slate-900 px-6 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isLoading ? "Входим..." : "Войти"}
        </button>
      </div>
    </form>
  );
}
