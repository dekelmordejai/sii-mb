"use client";
import { Run, workspace } from "@/lib/workspace";
import { useState } from "react";

export function valueLabel(value:string|null) {
  if(value===null) return "Sin resultado";
  const n = Number(value);
  return Number.isFinite(n)?n.toLocaleString("es-MX",{maximumFractionDigits:6}):value;
}

export function ResultView({run,chart="line"}:{run:Run;chart?:string}) {
  const [error,setError] = useState("");
  const points = run.result.series;
  const values = points.map(p=>Number(p.value)).filter(Number.isFinite);
  const low = Math.min(0,...values), high = Math.max(1,...values);
  const y = (v:number) => 230 - ((v-low)/(high-low))*195;
  const periods = [...new Set(points.map(p=>p.period))];
  const x = (period:string)=>60+(periods.indexOf(period)/Math.max(1,periods.length-1))*640;
  const groups = [...new Set(points.map(p=>p.group))];
  const colors = ["#7c48a3","#24765f","#c17a2e","#3876ac","#b53f6c"];
  return <div className="result-view"><div className="panel-header"><div><strong className="result-number">{valueLabel(run.result.total.value)} <small>{run.result.unit}</small></strong><p className="muted">{run.result.selected_rows} filas · {run.result.skipped_missing} omitidas · {run.result.total.status}</p></div><span className="pill">Provisional · Sin autorización de uso</span></div>
    {(chart==="line"||chart==="bar")&&points.length<=1000&&<figure className="chart"><svg viewBox="0 0 760 290" role="img" aria-label={`Gráfica de resultados, ${points.length} puntos. Tabla disponible debajo.`}><line x1="50" y1={y(0)} x2="720" y2={y(0)} stroke="#c9c4d4"/><text x="5" y="32">{valueLabel(String(high))}</text><text x="5" y="235">{valueLabel(String(low))}</text>
      {groups.map((g,i)=><g key={g}>{chart==="line"&&<polyline fill="none" stroke={colors[i%colors.length]} strokeWidth="3" points={points.filter(p=>p.group===g&&p.value!==null&&Number.isFinite(Number(p.value))).map(p=>`${x(p.period)},${y(Number(p.value))}`).join(" ")}/>} {points.filter(p=>p.group===g&&p.value!==null&&Number.isFinite(Number(p.value))).map((p,j)=>chart==="bar"?<rect key={j} x={x(p.period)-14+i*8} y={Math.min(y(0),y(Number(p.value)))} width="8" height={Math.max(1,Math.abs(y(0)-y(Number(p.value))))} fill={colors[i%colors.length]}><title>{p.period} · {g}: {p.value}</title></rect>:<circle key={j} cx={x(p.period)} cy={y(Number(p.value))} r="4" fill={colors[i%colors.length]}><title>{p.period} · {g}: {p.value}</title></circle>)}</g>)}
      {periods.filter((_,i)=>i%Math.max(1,Math.ceil(periods.length/6))===0).map(p=><text key={p} x={x(p)} y="265" textAnchor="middle" fontSize="12">{p}</text>)}</svg><figcaption>{groups.map((g,i)=><span key={g} style={{color:colors[i%colors.length]}}>● {g} </span>)}</figcaption></figure>}
    {chart!=="kpi"&&<div className="table-wrap"><table><caption className="sr-only">Serie calculada con valores decimales exactos</caption><thead><tr><th>Periodo</th><th>Grupo</th><th>Valor exacto</th><th>Estado</th><th>Filas</th></tr></thead><tbody>{points.slice(0,100).map((p,i)=><tr key={i}><td>{p.period}</td><td>{p.group}</td><td className="mono">{p.value??"—"}</td><td>{p.status}</td><td>{p.rows}</td></tr>)}</tbody></table>{points.length>100&&<p className="muted">Vista de 100 filas; la exportación incluye toda la serie.</p>}</div>}
    <details><summary>Procedencia y reproducción</summary><dl className="detail"><div><dt>Ejecución</dt><dd className="mono">{run.id}</dd></div><div><dt>Método / Fuente</dt><dd className="mono">{run.method_id}<br/>{run.source_id}</dd></div><div><dt>Huella de fuente</dt><dd className="mono">{run.result.source_sha256}</dd></div><div><dt>Motor / Fecha</dt><dd>{run.engine_version} · {new Date(run.created_at).toLocaleString("es-MX")}</dd></div></dl></details>
    <button className="button outline small" onClick={()=>workspace.export(run.id).catch(e=>setError(e.message))}>Exportar CSV</button>{error&&<p className="error" role="alert">{error}</p>}</div>;
}
