import { TicketsListPage } from "../../pages/tickets-list";
import { LoginPage } from "../../pages/login";

export const appRoutes = [
  { path: "/", element: <TicketsListPage /> },
  { path: "/login", element: <LoginPage /> },
];
