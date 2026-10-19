import { request, BASE } from "./api";

export type User = {
  id: string;
  username: string;
  role: "admin" | "editor" | "viewer";
  active: boolean;
  scopes: { indicators: string[]; sources: string[] };
};
export type Source = {
  id: string;
  name: string;
  kind: string;
  sha256: string;
  row_count: number;
  columns: { name: string; type: string; missing: number }[];
  preview: Record<string, string>[];
};
export type MethodConfig = {
  operation: string;
  numerator: string | null;
  denominator: string | null;
  multiplier: number;
  unit: string;
  date_column: string | null;
  group_by: string | null;
  granularity: string;
  missing: string;
  valid_from: string | null;
  valid_to: string | null;
  expression: Record<string, unknown> | null;
};
export type Method = {
  id: string;
  indicator_id: string;
  version: number;
  config: MethodConfig;
  created_at: string;
  status: string;
};
export type Point = {
  value: string | null;
  status: string;
  numerator: string | null;
  denominator: string | null;
  rows: number;
  period: string;
  group: string;
};
export type Run = {
  id: string;
  method_id: string;
  source_id: string;
  engine_version: string;
  created_at: string;
  request: {
    filters: Record<string, string>;
    start: string | null;
    end: string | null;
  };
  result: {
    total: Point;
    series: Point[];
    unit: string;
    selected_rows: number;
    source_rows: number;
    source_sha256: string;
    skipped_missing: number;
    result_status: string;
    usage_authorization: string;
  };
};
export type Widget = {
  run_id: string;
  title: string;
  chart: "line" | "bar" | "table" | "kpi";
};
export type Dashboard = { id: string; name: string; widgets: Widget[] };

export const post = <T>(path: string, body: unknown, method = "POST") =>
  request<T>(`/api/v1${path}`, {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
export const workspace = {
  me: () => request<User>("/api/v1/auth/me"),
  login: (username: string, password: string) =>
    post<User>("/auth/login", { username, password }),
  logout: () => post("/auth/logout", {}),
  sources: (offset = 0) =>
    request<{ items: Source[]; total: number }>(
      `/api/v1/sources?limit=100&offset=${offset}`,
    ),
  source: (id: string) => request<Source>(`/api/v1/sources/${id}`),
  upload: (name: string, content: string, types: Record<string, string>) =>
    post<Source>("/sources", { name, content, types }),
  methods: (id: string) =>
    request<Method[]>(`/api/v1/indicators/${id}/methods`),
  method: (id: string, config: MethodConfig) =>
    post<Method>(`/indicators/${id}/methods`, config),
  execute: (body: unknown) => post<Run>("/runs", body),
  runs: (id = "", offset = 0) =>
    request<{ items: Run[]; total: number }>(
      `/api/v1/runs?limit=100&offset=${offset}${id ? `&indicator_id=${id}` : ""}`,
    ),
  run: (id: string) => request<Run>(`/api/v1/runs/${id}`),
  reproduce: (id: string) => post<Run>(`/runs/${id}/reproduce`, {}),
  dashboards: () => request<Dashboard[]>("/api/v1/dashboards"),
  saveDashboard: (name: string, widgets: Widget[], id?: string) =>
    post<Dashboard>(
      `/dashboards${id ? `/${id}` : ""}`,
      { name, widgets },
      id ? "PATCH" : "POST",
    ),
  users: () => request<User[]>("/api/v1/users"),
  audit: (offset = 0) =>
    request<{
      items: {
        id: string;
        actor_id: string;
        action: string;
        object_id: string;
        created_at: string;
        detail: unknown;
      }[];
      total: number;
    }>(`/api/v1/audit?limit=50&offset=${offset}`),
  relations: (id: string) =>
    request<
      { id: string; source_id: string; target_id: string; label: string }[]
    >(`/api/v1/indicators/${id}/relations`),
  relate: (id: string, target_id: string, label: string) =>
    post(`/indicators/${id}/relations`, { target_id, label }),
  export: async (id: string) => {
    const response = await fetch(`${BASE}/api/v1/runs/${id}/export`, {
      credentials: "include",
    });
    if (!response.ok)
      throw new Error("No se pudo exportar; verifica tu sesión y permisos");
    const url = URL.createObjectURL(await response.blob());
    const a = document.createElement("a");
    a.href = url;
    a.download = `sii-mb-${id}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  },
};
