"use client";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { api, Indicator, IndicatorInput } from "@/lib/api";
import { useSession } from "./auth-gate";

export function IndicatorForm({ initial }: { initial?: Indicator }) {
  const { user } = useSession();
  const router = useRouter();
  const [values, setValues] = useState<IndicatorInput>({
    name: initial?.name ?? "",
    definition: initial?.definition ?? "",
    domain: initial?.domain ?? "",
    unit: initial?.unit ?? "",
  });
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [dimensions, setDimensions] = useState(
    initial?.dimensions.join(", ") ?? "",
  );
  function change(k: keyof IndicatorInput, v: string) {
    setValues((p) => ({ ...p, [k]: v }));
  }
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBusy(true);
    setError("");
    try {
      const data = {
        ...values,
        domain: values.domain || null,
        dimensions: dimensions
          .split(",")
          .map((v) => v.trim())
          .filter(Boolean),
      };
      const response = initial
        ? await api.update(initial.id, data)
        : await api.create(data);
      router.push(`/indicadores/${response.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al guardar");
    } finally {
      setBusy(false);
    }
  }
  if (user?.role === "viewer")
    return (
      <p className="notice">
        Tu cuenta permite consultar indicadores. Solicita a un administrador el
        permiso de edición si lo necesitas.
      </p>
    );
  return (
    <form onSubmit={submit} className="form-fields">
      <div>
        <label htmlFor="name">Nombre del indicador *</label>
        <input
          id="name"
          required
          minLength={3}
          maxLength={160}
          value={values.name}
          onChange={(e) => change("name", e.target.value)}
          placeholder="Ej. Intervalo observado"
        />
      </div>
      <div>
        <label htmlFor="definition">Definición conceptual *</label>
        <textarea
          id="definition"
          required
          minLength={10}
          maxLength={3000}
          rows={4}
          value={values.definition}
          onChange={(e) => change("definition", e.target.value)}
          placeholder="Describe qué se medirá, sin confundir la definición con la visualización."
        />
      </div>
      <div className="two-col">
        <div>
          <label htmlFor="domain">Dominio temático (opcional)</label>
          <input
            id="domain"
            maxLength={100}
            value={values.domain ?? ""}
            onChange={(e) => change("domain", e.target.value)}
            placeholder="Ej. Operación"
          />
        </div>
        <div>
          <label htmlFor="unit">Unidad de medida *</label>
          <input
            id="unit"
            required
            maxLength={60}
            value={values.unit}
            onChange={(e) => change("unit", e.target.value)}
            placeholder="Ej. min, %, pasajeros"
          />
        </div>
      </div>
      <div>
        <label htmlFor="dimensions">Dimensiones (separadas por coma)</label>
        <input
          id="dimensions"
          value={dimensions}
          onChange={(e) => setDimensions(e.target.value)}
          placeholder="Ej. fecha, grupo"
        />
      </div>
      <p className="form-note">
        Se guardará como <strong>borrador</strong>. Configura sus métodos y
        cálculos desde la ficha. La aprobación institucional requiere un proceso
        separado.
      </p>
      {error && (
        <div className="error" role="alert">
          {error}
        </div>
      )}
      <div className="form-actions">
        <button className="button primary" type="submit" disabled={busy}>
          {busy
            ? "Guardando..."
            : initial
              ? "Guardar cambios"
              : "Registrar indicador"}
        </button>
        <button
          type="button"
          className="button outline"
          onClick={() => router.back()}
        >
          Cancelar
        </button>
      </div>
    </form>
  );
}
