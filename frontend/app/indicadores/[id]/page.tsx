"use client";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { api, Indicator } from "@/lib/api";

export default function IndicatorDetail() {
  const params = useParams<{id:string}>();
  const [item,setItem] = useState<Indicator|null>(null);
  const [error,setError] = useState("");
  useEffect(()=>{api.get(params.id).then(setItem).catch(err=>setError(err instanceof Error?err.message:"Error al cargar"));},[params.id]);
  return <div className="page-stack narrow"><Link className="back-link" href="/indicadores">← Volver al inventario</Link>{error?<div className="error" role="alert">{error}</div>:!item?<p className="muted">Cargando ficha...</p>:<>
    <div className="page-heading"><div><p className="eyebrow mono">{item.code}</p><h1>{item.name}</h1><p className="muted">Identificador estable: <span className="mono">{item.id}</span></p></div><Link className="button outline" href={`/indicadores/${item.id}/editar`}>Editar borrador</Link></div>
    <section className="panel"><div className="panel-header"><h2>Ficha inicial</h2><span className="pill">Borrador</span></div><div className="detail"><div><small>Definición</small><p>{item.definition}</p></div><div><small>Dominio</small><p>{item.domain||"Sin clasificar"}</p></div><div><small>Unidad de medida</small><p>{item.unit}</p></div><div><small>Creado (UTC)</small><p>{new Date(item.created_at).toLocaleString("es-MX")}</p></div></div></section>
    <div className="notice">Este hito permite administrar la ficha inicial. Las fórmulas, fuentes y resultados se vincularán en las siguientes fases, sin cambiar la identidad del indicador.</div>
  </>}</div>;
}
