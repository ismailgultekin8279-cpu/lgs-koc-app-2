const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

/**
 * Small helper to create a user-friendly error without leaking raw debug JSON to UI.
 */
function toAppError(message, status, details) {
  const err = new Error(message);
  err.name = "ApiError";
  err.status = status;
  // Keep details for internal handling if needed, but do NOT render raw JSON in UI.
  err.details = details;
  return err;
}

/**
 * apiFetch
 * - Uses Vite proxy via /api
 * - Parses JSON when possible
 * - Throws ApiError with friendly message
 */
export async function apiFetch(path, options = {}) {
  const url = `${API_BASE}${path.startsWith("/") ? path : `/${path}`}`;

  const {
    method = "GET",
    headers = {},
    body,
    timeoutMs = 15000,
    signal,
  } = options;

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  // If caller provides a signal, we combine via a simple approach:
  // caller signal abort will abort this request too.
  if (signal) {
    if (signal.aborted) controller.abort();
    else signal.addEventListener("abort", () => controller.abort(), { once: true });
  }

  // Inject Auth Token
  const token = localStorage.getItem('access_token');
  const authHeaders = {};
  if (token) {
    authHeaders['Authorization'] = `Bearer ${token}`;
  }

  try {
    const res = await fetch(url, {
      method,
      headers: {
        Accept: "application/json",
        ...authHeaders,
        ...headers,
      },
      body,
      signal: controller.signal,
    });

    const contentType = res.headers.get("content-type") || "";
    const isJson = contentType.includes("application/json");

    let data = null;
    if (isJson) {
      // Some endpoints may return empty body; guard against parse errors.
      const text = await res.text();
      data = text ? JSON.parse(text) : null;
    } else {
      // If not JSON, keep as text (rare for our API).
      data = await res.text();
    }

    if (!res.ok) {
      // Friendly default messages
      const status = res.status;

      let message = "Bir sorun oluştu. Lütfen tekrar deneyin.";
      if (status === 400) message = "Gönderilen bilgiler hatalı görünüyor.";
      if (status === 401 || status === 403) message = "Bu işlem için yetkiniz yok.";
      if (status === 404) message = "İstenen kayıt bulunamadı.";
      if (status >= 500) message = "Sunucu hatası oluştu. Lütfen daha sonra tekrar deneyin.";

      throw toAppError(message, status, data);
    }

    return data;
  } catch (e) {
    if (e?.name === "AbortError") {
      throw toAppError("İstek zaman aşımına uğradı. Lütfen tekrar deneyin.", 0, null);
    }
    // If it's already an ApiError, bubble up
    if (e?.name === "ApiError") throw e;

    // Network or unexpected error
    throw toAppError("Ağ hatası oluştu. Bağlantınızı kontrol edin.", 0, null);
  } finally {
    clearTimeout(timeout);
  }
}

/**
 * Convenience helpers
 */
export function apiGet(path, options = {}) {
  return apiFetch(path, { ...options, method: "GET" });
}

export function apiPost(path, jsonBody, options = {}) {
  return apiFetch(path, {
    ...options,
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    body: JSON.stringify(jsonBody ?? {}),
  });
}

export function apiPatch(path, jsonBody, options = {}) {
  return apiFetch(path, {
    ...options,
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    body: JSON.stringify(jsonBody ?? {}),
  });
}
