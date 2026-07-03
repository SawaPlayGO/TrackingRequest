import { useAuthContext } from "../../../app/providers";

export function useAuth() {
  const auth = useAuthContext();

  return {
    auth: auth.auth,
    login: auth.login,
    logout: auth.logout,
    isAdmin: auth.isAdmin,
    isLoading: auth.isLoading,
  };
}
