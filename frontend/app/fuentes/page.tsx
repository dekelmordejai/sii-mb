"use client";
import { useEffect, useState } from "react";
import { Source, workspace, post } from "@/lib/workspace";
import { useSession } from "@/components/auth-gate";

export default function SourcesPage() {
  const { user } = useSession();
  const [sources, setSources] = useState<Source[]>([]),
    [profile, setProfile] = useState<Source | null>(null);
  const [name, setName] = useState(""),
    [content, setContent] = useState(""),
    [types, setTypes] = useState<Record<string, string>>({});
  const [error, setError] = useState(""),
    [notice, setNotice] = useState(""),
    [busy, setBusy] = useState(false),
    [offset, setOffset] = useState(0),
    [total, setTotal] = useState(0);
  const load = () =>
    workspace
      .sources(offset)
      .then((r) => {
        setSources(r.items);
        setTotal(r.total);
      })
      .catch((e) => setError(e.message));
  useEffect(() => {
    load();
  }, [offset]); // eslint-disable-line react-hooks/exhaustive-deps
  async function inspect(text: string, filename: string) {
    setError("");
    setNotice("");
    setProfile(null);
    setContent("");
    setBusy(true);
    try {
      const p = await post<Source>("/sources/inspect", {
        name: filename,
        content: text,
      });
      setName(filename);
      setContent(text);
      setProfile(p);
      setTypes(Object.fromEntries(p.columns.map((c) => [c.name, c.type])));
    } catch (e) {
      setError(e instanceof Error ? e.message : "CSV inválido");
    } finally {
      setBusy(false);
    }
  }
  async function save() {
    setBusy(true);
    setError("");
    try {
      const item = await workspace.upload(name, content, types);
      setProfile(item);
      setContent("");
      setNotice("Fuente guardada como instantánea inmutable.");
      await load();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error al guardar");
    } finally {
      setBusy(false);
    }
  }
  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <p className="eyebrow">DATOS Y LINAJE</p>
          <h1>Fuentes de datos</h1>
          <p className="muted">
            CSV UTF-8, hasta 1 MB, 10 000 filas y 50 columnas. Cada importación
            conserva su contenido y huella.
          </p>
        </div>
      </div>
      {user?.role !== "viewer" && (
        <section className="panel form-fields">
          <h2>Importar y validar</h2>
          <div>
            <label htmlFor="csv">Archivo CSV sintético</label>
            <input
              id="csv"
              type="file"
              accept=".csv,text/csv"
              disabled={busy}
              onChange={async (e) => {
                const file = e.target.files?.[0];
                if (!file) return;
                if (file.size > 1_000_000) {
                  setError("El archivo supera 1 MB");
                  return;
                }
                await inspect(await file.text(), file.name);
              }}
            />
          </div>
          <button
            className="button outline"
            disabled={busy}
            onClick={() =>
              inspect(
                "fecha,grupo,valor,base\n2026-01-01,A,80,100\n2026-01-01,B,30,50\n2026-01-02,A,90,100\n2026-01-02,B,45,50\n",
                "Demostración sintética",
              )
            }
          >
            Preparar ejemplo sintético
          </button>
          {content && (
            <>
              <div>
                <label htmlFor="source-name">Nombre de fuente</label>
                <input
                  id="source-name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  minLength={3}
                  maxLength={160}
                />
              </div>
              <div className="two-col">
                {profile?.columns.map((c) => (
                  <div key={c.name}>
                    <label htmlFor={`type-${c.name}`}>
                      {c.name} · {c.missing} vacíos
                    </label>
                    <select
                      id={`type-${c.name}`}
                      value={types[c.name]}
                      onChange={(e) =>
                        setTypes({ ...types, [c.name]: e.target.value })
                      }
                    >
                      <option value="text">Texto</option>
                      <option value="number">Número</option>
                      <option value="date">Fecha YYYY-MM-DD</option>
                    </select>
                  </div>
                ))}
              </div>
              <button
                className="button primary"
                disabled={busy || name.trim().length < 3}
                onClick={save}
              >
                {busy ? "Validando…" : "Guardar fuente"}
              </button>
            </>
          )}
        </section>
      )}
      {error && (
        <div className="error" role="alert">
          {error}
        </div>
      )}
      {notice && (
        <p className="notice" role="status">
          {notice}
        </p>
      )}
      {profile && (
        <section className="panel">
          <h2>Vista previa · {profile.row_count} registros</h2>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  {profile.columns.map((c) => (
                    <th key={c.name}>{c.name}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {profile.preview.map((r, i) => (
                  <tr key={i}>
                    {profile.columns.map((c) => (
                      <td key={c.name}>{r[c.name] || "—"}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {profile.sha256 && <p className="mono">SHA-256: {profile.sha256}</p>}
        </section>
      )}
      <section className="panel">
        <h2>Fuentes registradas</h2>
        {sources.length === 0 ? (
          <p className="muted">Todavía no hay fuentes a tu alcance.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Fuente</th>
                <th>Filas</th>
                <th>Columnas</th>
                <th>Consulta</th>
              </tr>
            </thead>
            <tbody>
              {sources.map((s) => (
                <tr key={s.id}>
                  <td>{s.name}</td>
                  <td>{s.row_count}</td>
                  <td>
                    {s.columns.map((c) => `${c.name} (${c.type})`).join(", ")}
                  </td>
                  <td>
                    <button
                      className="button outline small"
                      onClick={() => {
                        setProfile(s);
                        setContent("");
                      }}
                    >
                      Inspeccionar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        <div className="pagination">
          <span>{total} fuentes</span>
          <div>
            <button
              disabled={offset === 0}
              onClick={() => setOffset(Math.max(0, offset - 100))}
            >
              Anterior
            </button>
            <button
              disabled={offset + 100 >= total}
              onClick={() => setOffset(offset + 100)}
            >
              Siguiente
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}
