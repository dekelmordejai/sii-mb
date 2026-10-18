import Link from "next/link";
import { IndicatorForm } from "@/components/indicator-form";
export default function NewIndicator() {
  return <div className="page-stack narrow"><Link href="/indicadores" className="back-link">← Volver al inventario</Link><div className="page-heading"><div><p className="eyebrow">FICHA EN BORRADOR</p><h1>Nuevo indicador</h1><p className="muted">Podrás registrar indicadores nuevos en cualquier momento, sin depender de un catálogo precargado.</p></div></div><section className="panel"><h2>Información inicial</h2><IndicatorForm/></section></div>;
}
