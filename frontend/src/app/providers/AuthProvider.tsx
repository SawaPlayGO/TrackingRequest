/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useState, type PropsWithChildren } from "react";
import { loginAdmin } from "../../features/auth/api/authApi";

type AuthCredentials = { username: string; password: string };

type AuthContextType = {
  auth: AuthCredentials | null;
  isAdmin: boolean;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: PropsWithChildren) {
  const [auth, setAuth] = useState<AuthCredentials | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const login = async (username: string, password: string) => {
    setIsLoading(true);
    try {
      await loginAdmin({ username, password });
      setAuth({ username, password });
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    setAuth(null);
  };

  const value: AuthContextType = {
    auth,
    isAdmin: auth !== null,
    isLoading,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuthContext() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuthContext must be used within AuthProvider");
  }
  return context;
}
