"use client";
import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { api, IndicatorPage } from "@/lib/api";

const PAGE_SIZE = 20;
export default function IndicatorsPage() {
  const [q, setQ] = useState("");
  const [page, setPage] = useState(0);
  const [result, setResult] = useState<IndicatorPage | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const refresh = useCallback(async () => {
    setLoading(true); setError("");
    try { setResult(await api.list(q, PAGE_SIZE, page * PAGE_SIZE)); }
    catch (err) { setError(err instanceof Error ? err.message : "Error al consultar indicadores"); }
    finally { setLoading(false); }
  }, [q, page]);
  useEffect(() => { const delay = setTimeout(() => { void refresh(); }, 250); return () => clearTimeout(delay); }, [refresh]);
  return <div className="page-stack"><div className="page-heading"><div><p className="eyebrow">ADMINISTRACIÓN</p><h1>Indicadores</h1><p className="muted">Registra y consulta indicadores sin modificar el código de la aplicación.</p></div><Link className="button primary" href="/indicadores/nuevo">＋ Nuevo indicador</Link></div>
    <section className="panel"><div className="panel-header"><h2>Inventario de trabajo</h2><span className="pill">{result?.total ?? 0} registros</span></div>
      <label htmlFor="search">Buscar por nombre, código o dominio</label><input id="search" placeholder="Ej. regularidad, flota, IND-..." value={q} onChange={e => {setQ(e.target.value);setPage(0);}}/>
      {error && <div className="error" role="alert">{error}</div>}
      {loading ? <p className="muted">Consultando indicadores...</p> : result?.items.length ? <div className="table-wrap"><table><thead><tr><th>Código</th><th>Indicador</th><th>Dominio</th><th>Unidad</th><th>Estado</th><th></th></tr></thead><tbody>{result.items.map(item=><tr key={item.id}><td className="mono">{item.code}</td><td><strong>{item.name}</strong></td><td>{item.domain||"—"}</td><td>{item.unit}</td><td><span className="pill">Borrador</span></td><td><Link href={`/indicadores/${item.id}`}>Ver →</Link></td></tr>)}</tbody></table></div> : !error && <div className="empty"><strong>No hay indicadores para mostrar</strong><p className="muted">{q ? "Prueba con otra búsqueda." : "El catálogo inicia vacío. Puedes crear el primer indicador."}</p></div>}
      <div className="pagination"><span className="muted">{result ? `Registros ${result.total ? page*PAGE_SIZE+1 : 0}–${Math.min((page+1)*PAGE_SIZE,result.total)} de ${result.total}` : ""}</span><div><button className="button outline small" disabled={page===0 || loading} onClick={()=>setPage(p=>p-1)}>Anterior</button><button className="button outline small" disabled={loading || !result || (page+1)*PAGE_SIZE >= result.total} onClick={()=>setPage(p=>p+1)}>Siguiente</button></div></div>
    </section>
  </div>;
}
