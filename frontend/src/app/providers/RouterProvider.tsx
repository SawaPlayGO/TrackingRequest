/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useEffect, useMemo, useState } from "react";
import type { PropsWithChildren } from "react";

type RouterContextType = {
  route: string;
  navigate: (path: string) => void;
};

const RouterContext = createContext<RouterContextType | null>(null);

export function RouterProvider({ children }: PropsWithChildren) {
  const [route, setRoute] = useState<string>(() => window.location.pathname || "/");

  useEffect(() => {
    const handlePop = () => setRoute(window.location.pathname || "/");
    window.addEventListener("popstate", handlePop);
    return () => window.removeEventListener("popstate", handlePop);
  }, []);

  const navigate = (path: string) => {
    window.history.pushState(null, "", path);
    setRoute(path);
  };

  const value = useMemo(() => ({ route, navigate }), [route]);

  return <RouterContext.Provider value={value}>{children}</RouterContext.Provider>;
}

export function useRouter() {
  const context = useContext(RouterContext);
  if (!context) {
    throw new Error("useRouter must be used within RouterProvider");
  }
  return context;
}
