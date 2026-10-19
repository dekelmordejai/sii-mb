"use client";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { api, Indicator } from "@/lib/api";
import { CalculationPanel } from "@/components/calculation-panel";
import { useSession } from "@/components/auth-gate";
import { workspace } from "@/lib/workspace";

export default function IndicatorDetail() {
  const params = useParams<{ id: string }>();
  const [item, setItem] = useState<Indicator | null>(null);
  const [error, setError] = useState("");
  const { user } = useSession();
  const [relations, setRelations] = useState<
    { id: string; source_id: string; target_id: string; label: string }[]
  >([]);
  useEffect(() => {
    workspace
      .relations(params.id)
      .then(setRelations)
      .catch((e) => setError(e.message));
  }, [params.id]);
  useEffect(() => {
    api
      .get(params.id)
      .then(setItem)
      .catch((err) =>
        setError(err instanceof Error ? err.message : "Error al cargar"),
      );
  }, [params.id]);
  return (
    <div className="page-stack narrow">
      <Link className="back-link" href="/indicadores">
        ← Volver al inventario
      </Link>
      {error ? (
        <div className="error" role="alert">
          {error}
        </div>
      ) : !item ? (
        <p className="muted">Cargando ficha...</p>
      ) : (
        <>
          <div className="page-heading">
            <div>
              <p className="eyebrow mono">{item.code}</p>
              <h1>{item.name}</h1>
              <p className="muted">
                Identificador estable: <span className="mono">{item.id}</span>
              </p>
            </div>
            {user?.role !== "viewer" && (
              <Link
                className="button outline"
                href={`/indicadores/${item.id}/editar`}
              >
                Editar borrador
              </Link>
            )}
          </div>
          <section className="panel">
            <div className="panel-header">
              <h2>Ficha inicial</h2>
              <span className="pill">Borrador</span>
            </div>
            <div className="detail">
              <div>
                <small>Definición</small>
                <p>{item.definition}</p>
              </div>
              <div>
                <small>Dominio</small>
                <p>{item.domain || "Sin clasificar"}</p>
              </div>
              <div>
                <small>Unidad de medida</small>
                <p>{item.unit}</p>
              </div>
              <div>
                <small>Creado (UTC)</small>
                <p>{new Date(item.created_at).toLocaleString("es-MX")}</p>
              </div>
            </div>
          </section>
          <section className="panel form-fields">
            <h2>Configuración y relaciones</h2>
            <p>
              Estado operativo:{" "}
              <strong>{item.active ? "Activo" : "Desactivado"}</strong>. La
              desactivación es reversible y conserva el historial.
            </p>
            {user?.role !== "viewer" && (
              <>
                <button
                  className="button outline"
                  onClick={() =>
                    api
                      .update(item.id, { active: !item.active })
                      .then(setItem)
                      .catch((e) => setError(e.message))
                  }
                >
                  {item.active ? "Desactivar indicador" : "Reactivar indicador"}
                </button>
                <form
                  className="form-fields"
                  onSubmit={(e) => {
                    e.preventDefault();
                    const f = new FormData(e.currentTarget);
                    workspace
                      .relate(
                        item.id,
                        String(f.get("target")),
                        String(f.get("label")),
                      )
                      .then(() => workspace.relations(item.id))
                      .then(setRelations)
                      .catch((e) => setError(e.message));
                  }}
                >
                  <div>
                    <label htmlFor="target">
                      Identificador del indicador relacionado
                    </label>
                    <input id="target" name="target" required maxLength={36} />
                  </div>
                  <div>
                    <label htmlFor="relation-label">
                      Descripción de la relación
                    </label>
                    <input
                      id="relation-label"
                      name="label"
                      required
                      minLength={3}
                      maxLength={100}
                    />
                  </div>
                  <button className="button outline">
                    Vincular indicadores
                  </button>
                </form>
              </>
            )}
            {relations.map((r) => (
              <p key={r.id}>
                {r.label}:{" "}
                <Link
                  href={`/indicadores/${r.source_id === item.id ? r.target_id : r.source_id}`}
                >
                  {r.source_id === item.id ? r.target_id : r.source_id}
                </Link>
              </p>
            ))}
          </section>
          <CalculationPanel indicator={item} />
        </>
      )}
    </div>
  );
}
