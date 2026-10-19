import { defineConfig } from "@playwright/test";
import path from "node:path";

const backend = path.resolve(__dirname, "../backend");
const python =
  process.env.SII_MB_TEST_PYTHON ||
  path.join(
    backend,
    ".venv",
    process.platform === "win32" ? "Scripts/python.exe" : "bin/python",
  );
const db = path
  .join(backend, "data", `e2e-${Date.now()}.db`)
  .replaceAll("\\", "/");
export default defineConfig({
  testDir: "./tests",
  timeout: 60000,
  workers: 1,
  fullyParallel: false,
  use: {
    baseURL: "http://127.0.0.1:3100",
    headless: true,
    channel: process.env.SII_MB_BROWSER_CHANNEL || "msedge",
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
  },
  reporter: [["list"], ["json", { outputFile: "test-results/results.json" }]],
  webServer: [
    {
      command: `"${python}" -m uvicorn app.main:app --host 127.0.0.1 --port 8100`,
      cwd: backend,
      url: "http://127.0.0.1:8100/api/v1/health",
      timeout: 60000,
      reuseExistingServer: false,
      env: {
        SII_MB_DATABASE_URL:
          process.env.SII_MB_TEST_DATABASE_URL || `sqlite+pysqlite:///${db}`,
        SII_MB_ADMIN_PASSWORD: "synthetic-e2e-password-2026",
        SII_MB_UI_ORIGINS: "http://127.0.0.1:3100",
      },
    },
    {
      command: "npm run dev -- --port 3100",
      url: "http://127.0.0.1:3100",
      timeout: 60000,
      reuseExistingServer: false,
      env: {
        NEXT_PUBLIC_API_BASE_URL: "http://127.0.0.1:8100",
        NEXT_TELEMETRY_DISABLED: "1",
      },
    },
  ],
});
