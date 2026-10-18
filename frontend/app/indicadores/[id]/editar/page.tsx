"use client";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { api, Indicator } from "@/lib/api";
import { IndicatorForm } from "@/components/indicator-form";

export default function EditIndicator() {
  const params = useParams<{id:string}>();
  const [item,setItem] = useState<Indicator|null>(null);
  const [error,setError] = useState("");
  useEffect(()=>{api.get(params.id).then(setItem).catch(err=>setError(err instanceof Error?err.message:"Error al cargar"));},[params.id]);
  return <div className="page-stack narrow"><Link href={`/indicadores/${params.id}`} className="back-link">← Volver al indicador</Link><div className="page-heading"><div><p className="eyebrow">EDICIÓN DE BORRADOR</p><h1>Editar ficha</h1></div></div><section className="panel">{error?<div className="error" role="alert">{error}</div>:!item?<p className="muted">Cargando ficha...</p>:<IndicatorForm initial={item}/>}</section></div>;
}
