import { AuthProvider } from "./providers/AuthProvider";
import { QueryProvider } from "./providers/QueryProvider";
import { RouterProvider, useRouter } from "./providers/RouterProvider";
import { appRoutes } from "./routes/routes";

function AppContent() {
  const { route, navigate } = useRouter();
  const currentRoute = appRoutes.find((item) => item.path === route) ?? appRoutes[0];

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b border-slate-200 bg-white shadow-sm">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">
              Tracking Request
            </p>
            <h1 className="text-2xl font-semibold text-slate-900">Список заявок</h1>
          </div>
          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              onClick={() => navigate("/")}
              className={`rounded-xl border px-4 py-2 text-sm transition ${
                route === "/" ? "border-slate-900 bg-slate-900 text-white" : "border-slate-200 bg-white text-slate-700 hover:border-slate-300"
              }`}
            >
              Заявки
            </button>
            <button
              type="button"
              onClick={() => navigate("/login")}
              className={`rounded-xl border px-4 py-2 text-sm transition ${
                route === "/login" ? "border-slate-900 bg-slate-900 text-white" : "border-slate-200 bg-white text-slate-700 hover:border-slate-300"
              }`}
            >
              Вход администратора
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <div className="space-y-6">{currentRoute.element}</div>
      </main>
    </div>
  );
}

export default function App() {
  return (
    <QueryProvider>
      <AuthProvider>
        <RouterProvider>
          <AppContent />
        </RouterProvider>
      </AuthProvider>
    </QueryProvider>
  );
}
