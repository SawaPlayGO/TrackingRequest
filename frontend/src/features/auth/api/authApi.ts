import { apiClient } from "../../../shared/api/client";

function getAuthorizationHeader(credentials: { username: string; password: string }) {
  return `Basic ${window.btoa(`${credentials.username}:${credentials.password}`)}`;
}

export async function loginAdmin(credentials: { username: string; password: string }): Promise<void> {
  await apiClient.get("/admin/check", {
    headers: {
      Authorization: getAuthorizationHeader(credentials),
    },
  });
}
