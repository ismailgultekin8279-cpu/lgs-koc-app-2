import React from "react";
import ReactDOM from "react-dom/client";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "./lib/queryClient";
import { StudentProvider } from "./context/StudentContext";
import App from "./App.jsx";
import "./index.css";

import ErrorBoundary from './components/ErrorBoundary';

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <StudentProvider>
          <App />
        </StudentProvider>
      </QueryClientProvider>
    </ErrorBoundary>
  </React.StrictMode>
);
