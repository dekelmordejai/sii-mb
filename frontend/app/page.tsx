"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function Home() {
  const [count, setCount] = useState<number | null>(null);
  const [status, setStatus] = useState<"loading"|"connected"|"offline">("loading");
  useEffect(() => {
    Promise.all([api.health(), api.list("", 1, 0)])
      .then(([health, results]) => { setStatus(health.status === "ok" ? "connected" : "offline"); setCount(results.total); })
      .catch(() => setStatus("offline"));
  }, []);
  return <div className="page-stack">
    <div className="page-heading"><div><p className="eyebrow">PANEL DE CONTROL</p><h1>Bienvenido al SII-MB</h1><p className="muted">La base de una plataforma de indicadores configurables, preparada para crecer por módulos.</p></div><Link className="button primary" href="/indicadores/nuevo">＋ Crear indicador</Link></div>
    <div className="stat-grid">
      <div className="stat-card"><p>Indicadores registrados</p><strong>{count === null ? "—" : count}</strong><small>Todos son borradores en este hito</small></div>
      <div className="stat-card"><p>API local</p><strong className={status === "connected" ? "good" : "not-ready"}>{status === "connected" ? "Conectada" : status === "loading" ? "..." : "Sin conexión"}</strong><small>{status === "offline" ? "Inicia el servidor FastAPI" : "127.0.0.1:8000"}</small></div>
      <div className="stat-card"><p>Hito actual</p><strong>M0–M1</strong><small>Administración básica de indicadores</small></div>
    </div>
    <section className="panel"><div className="panel-header"><div><h2>Primer flujo disponible</h2><p className="muted">Crear, consultar, buscar y editar fichas en borrador.</p></div></div>
      <div className="steps"><div><b>01</b><span>Crear una ficha de indicador</span></div><div><b>02</b><span>Guardar en la base local</span></div><div><b>03</b><span>Consultar y actualizar</span></div></div>
      <Link className="button outline" href="/indicadores">Abrir indicadores →</Link>
    </section>
    <div className="notice"><strong>Alcance del prototipo:</strong> no hay autenticación, cargas de fuentes, fórmulas ejecutables ni cálculos en esta versión. No utilices información institucional real o confidencial.</div>
  </div>;
}
