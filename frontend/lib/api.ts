export type Indicator = {
  id: string;
  code: string;
  name: string;
  definition: string;
  domain: string | null;
  unit: string;
  status: "draft";
  created_at: string;
  updated_at: string;
  active: boolean;
  dimensions: string[];
};

export type IndicatorInput = Pick<Indicator, "name" | "definition" | "domain" | "unit"> & { dimensions?: string[]; active?: boolean };
export type IndicatorPage = { items: Indicator[]; total: number; limit: number; offset: number };

export const BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

export class ApiError extends Error {
  constructor(public status: number, message: string) { super(message); }
}

export async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${BASE}${path}`, { ...init, credentials: "include", cache: "no-store" });
  } catch {
    throw new ApiError(0, "No se pudo conectar con la API local. Verifica que FastAPI esté ejecutándose en 127.0.0.1:8000.");
  }
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    if (response.status === 401 && !path.includes("/auth/login") && typeof window !== "undefined") window.dispatchEvent(new Event("session-expired"));
    const message = typeof err.detail === "string" ? err.detail : Array.isArray(err.detail) ? err.detail.map((e: {loc?: string[]; msg?: string}) => `${e.loc?.slice(1).join(".")}: ${e.msg}`).join("; ") : `Error HTTP ${response.status}`;
    throw new ApiError(response.status, message);
  }
  return response.json() as Promise<T>;
}

export const api = {
  list: (q = "", limit = 30, offset = 0) => request<IndicatorPage>(`/api/v1/indicators?q=${encodeURIComponent(q)}&limit=${limit}&offset=${offset}`),
  get: (id: string) => request<Indicator>(`/api/v1/indicators/${encodeURIComponent(id)}`),
  create: (body: IndicatorInput) => request<Indicator>("/api/v1/indicators", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }),
  update: (id: string, body: Partial<IndicatorInput>) => request<Indicator>(`/api/v1/indicators/${encodeURIComponent(id)}`, { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }),
  health: () => request<{status: string; environment: string; version: string}>("/api/v1/health")
};
