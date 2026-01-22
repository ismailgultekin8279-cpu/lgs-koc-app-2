import { QueryClient } from "@tanstack/react-query";

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // Avoid overly frequent refetches during UI navigation
      refetchOnWindowFocus: false,
      refetchOnReconnect: true,
      retry: 1,
      staleTime: 20 * 1000, // 20s
    },
    mutations: {
      retry: 0,
    },
  },
});
