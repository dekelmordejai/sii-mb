"""Deterministic allowlisted engine. No eval, SQL, code or expression interpreter."""
import csv
import io
from collections import defaultdict
from datetime import date
from decimal import Decimal, InvalidOperation, localcontext
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

ENGINE_VERSION = "decimal-1"
MAX_BYTES = 1_000_000
MAX_ROWS = 10_000


class MethodConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    operation: Literal["count", "sum", "mean", "min", "max", "ratio_of_sums", "expression"]
    numerator: str | None = Field(default=None, min_length=1, max_length=100)
    denominator: str | None = Field(default=None, min_length=1, max_length=100)
    multiplier: Literal[1, 100] = 1
    unit: str = Field(min_length=1, max_length=60)
    date_column: str | None = Field(default=None, min_length=1, max_length=100)
    group_by: str | None = Field(default=None, min_length=1, max_length=100)
    granularity: Literal["day", "month", "year"] = "day"
    missing: Literal["error", "skip", "zero"] = "error"
    valid_from: date | None = None
    valid_to: date | None = None
    expression: dict | None = None

    @model_validator(mode="after")
    def valid_operation(self):
        if self.operation not in ("count", "expression") and not self.numerator:
            raise ValueError("Selecciona la columna numérica")
        if self.operation == "ratio_of_sums" and not self.denominator:
            raise ValueError("Selecciona el denominador")
        if self.operation == "count" and (self.numerator or self.denominator):
            raise ValueError("El conteo no admite columnas numéricas")
        if self.operation != "ratio_of_sums" and self.denominator:
            raise ValueError("El denominador solo aplica a razón de sumas")
        if self.operation == "expression":
            validate_expression(self.expression)
        elif self.expression:
            raise ValueError("La expresión solo aplica al operador de expresión")
        if self.valid_from and self.valid_to and self.valid_from > self.valid_to:
            raise ValueError("Vigencia invertida")
        if (self.valid_from or self.valid_to) and not self.date_column:
            raise ValueError("La vigencia requiere columna de fecha")
        return self


def validate_expression(node, depth=0, budget=None):
    budget = budget if budget is not None else [0]
    budget[0] += 1
    if depth > 8 or budget[0] > 64 or not isinstance(node, dict):
        raise ValueError("Expresión inválida o demasiado compleja (64 nodos, profundidad 8)")
    op = node.get("op")
    if op == "literal" and set(node) == {"op", "value"}:
        number(str(node["value"]))
    elif op in ("sum", "mean", "min", "max", "count"):
        if set(node) - {"op", "column", "where"}:
            raise ValueError("Campos desconocidos en agregación")
        if op != "count" and (not isinstance(node.get("column"), str) or not 1 <= len(node["column"]) <= 100):
            raise ValueError("Columna requerida en agregación")
        if op == "count" and "column" in node:
            raise ValueError("El conteo cuenta filas, sin columna numérica")
        if "where" in node:
            rule = node["where"]
            if not isinstance(rule, dict) or set(rule) != {"column", "eq"} or not all(isinstance(v, str) and 0 < len(v) <= 100 for v in rule.values()):
                raise ValueError("Condición inválida: usa column y eq")
    elif op in ("add", "subtract", "multiply", "divide") and set(node) == {"op", "args"}:
        if not isinstance(node["args"], list) or len(node["args"]) != 2:
            raise ValueError("La operación requiere dos argumentos")
        for child in node["args"]:
            validate_expression(child, depth + 1, budget)
    else:
        raise ValueError("Operador no permitido")


def expression_columns(node):
    columns = {node["column"]} if node.get("column") else set()
    if node.get("where"):
        columns.add(node["where"]["column"])
    for child in node.get("args", []):
        columns |= expression_columns(child)
    return columns


def expression_numeric_columns(node):
    columns = {node["column"]} if node.get("op") in ("sum", "mean", "min", "max") else set()
    for child in node.get("args", []):
        columns |= expression_numeric_columns(child)
    return columns


def evaluate(node, rows, missing):
    op = node["op"]
    if op == "literal":
        return number(str(node["value"]))
    if op in ("sum", "mean", "min", "max", "count"):
        if "where" in node:
            rule = node["where"]
            rows = [r for r in rows if r[rule["column"]] == rule["eq"]]
        if op == "count":
            return Decimal(len(rows))
        values = [number(r[node["column"]] or "0") for r in rows]
        if not values:
            return None
        if op == "sum":
            return sum(values, Decimal(0))
        if op == "mean":
            return sum(values, Decimal(0)) / len(values)
        return min(values) if op == "min" else max(values)
    a, b = (evaluate(c, rows, missing) for c in node["args"])
    if a is None or b is None:
        return None
    if op == "add":
        return a + b
    if op == "subtract":
        return a - b
    if op == "multiply":
        return a * b
    return None if b == 0 else a / b


class RunInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    method_id: str = Field(max_length=36)
    source_id: str = Field(max_length=36)
    filters: dict[str, str] = Field(default_factory=dict, max_length=10)
    start: date | None = None
    end: date | None = None

    @model_validator(mode="after")
    def ordered_dates(self):
        if self.start and self.end and self.start > self.end:
            raise ValueError("El inicio debe ser anterior al fin")
        if any(len(k) > 100 or len(v) > 200 for k, v in self.filters.items()):
            raise ValueError("Filtro demasiado largo")
        return self


def number(value: str) -> Decimal:
    if not value or len(value) > 60:
        raise ValueError("Número faltante o demasiado largo")
    try:
        result = Decimal(value)
    except InvalidOperation:
        raise ValueError(f"Número inválido: {value[:40]}") from None
    if not result.is_finite() or result.copy_abs() > Decimal("1e18") or result.as_tuple().exponent < -12:
        raise ValueError("Número fuera de rango o precisión (máximo 12 decimales)")
    return result


def iso_date(value: str) -> str:
    parsed = date.fromisoformat(value)
    if parsed.isoformat() != value:
        raise ValueError("Usa fechas YYYY-MM-DD")
    return value


def parse_csv(content: str):
    if len(content.encode("utf-8")) > MAX_BYTES or "\x00" in content:
        raise ValueError("CSV inválido o superior a 1 MB")
    stream = io.StringIO(content.lstrip("\ufeff"), newline="")
    reader = csv.reader(stream, strict=True)
    try:
        columns = next(reader)
        if not 1 <= len(columns) <= 50 or any(not c.strip() or len(c) > 100 for c in columns):
            raise ValueError("Se requieren entre 1 y 50 encabezados de hasta 100 caracteres")
        if len(set(columns)) != len(columns) or any(c != c.strip() for c in columns):
            raise ValueError("Encabezados duplicados o con espacios exteriores")
        rows = []
        for index, values in enumerate(reader, 2):
            if not values:
                continue
            if len(values) != len(columns):
                raise ValueError(f"Fila {index}: número incorrecto de columnas")
            if len(rows) >= MAX_ROWS:
                raise ValueError("Máximo 10000 filas")
            rows.append(dict(zip(columns, (v.strip() for v in values))))
    except (csv.Error, StopIteration) as exc:
        raise ValueError("CSV vacío o mal formado") from exc
    if not rows:
        raise ValueError("El CSV no contiene registros")
    profile = []
    for col in columns:
        values = [r[col] for r in rows if r[col]]
        kind = "text"
        try:
            if values:
                for v in values:
                    number(v)
                kind = "number"
        except ValueError:
            try:
                for v in values:
                    iso_date(v)
                kind = "date"
            except ValueError:
                pass
        profile.append({"name": col, "type": kind, "missing": len(rows) - len(values)})
    return rows, {"columns": profile, "row_count": len(rows), "preview": rows[:5]}


def calculate(content: str, method: MethodConfig, request: RunInput):
    rows, profile = parse_csv(content)
    columns = {c["name"] for c in profile["columns"]}
    required = {c for c in (method.numerator, method.denominator, method.date_column, method.group_by) if c}
    if method.expression:
        required |= expression_columns(method.expression)
    if not (required | set(request.filters)).issubset(columns):
        raise ValueError("La fuente no contiene todas las columnas del método y filtros")
    if (request.start or request.end) and not method.date_column:
        raise ValueError("El método no tiene columna de fecha")
    selected = []
    skipped = 0
    for index, row in enumerate(rows, 2):
        if any(row[k] != v for k, v in request.filters.items()):
            continue
        try:
            if method.date_column:
                day = date.fromisoformat(iso_date(row[method.date_column]))
                if (request.start and day < request.start) or (request.end and day > request.end):
                    continue
                if (method.valid_from and day < method.valid_from) or (method.valid_to and day > method.valid_to):
                    continue
            numeric_columns = {c for c in (method.numerator, method.denominator) if c}
            if method.expression:
                numeric_columns |= expression_numeric_columns(method.expression)
            if any(not row[c] for c in numeric_columns) and method.missing == "skip":
                skipped += 1
                continue
            for col in numeric_columns:
                if col:
                    number(row[col] or ("0" if method.missing == "zero" else ""))
                    if not row[col] and method.missing == "zero":
                        row[col] = "0"
            if method.group_by and not row[method.group_by]:
                raise ValueError("Grupo faltante")
        except ValueError as exc:
            raise ValueError(f"Fila {index}: {exc}") from exc
        selected.append(row)
    if not selected:
        raise ValueError("No hay filas para los filtros seleccionados")

    def aggregate(group):
        with localcontext() as ctx:
            ctx.prec = 50
            numerator = Decimal(len(group)) if method.operation in ("count", "expression") else sum((number(r[method.numerator]) for r in group), Decimal(0))
            denominator = sum((number(r[method.denominator]) for r in group), Decimal(0)) if method.operation == "ratio_of_sums" else None
            value = numerator
            if method.operation in ("mean", "min", "max"):
                values = [number(r[method.numerator]) for r in group]
                value = numerator / len(group) if method.operation == "mean" else min(values) if method.operation == "min" else max(values)
            if method.operation == "expression":
                value = evaluate(method.expression, group, method.missing)
            if denominator is not None:
                value = None if denominator == 0 else numerator / denominator
            return {"value": str(value * method.multiplier) if value is not None else None,
                    "status": "undefined" if value is None and method.operation == "expression" else "zero_denominator" if value is None else "ok",
                    "numerator": str(numerator) if method.operation != "expression" else None, "denominator": str(denominator) if denominator is not None else None,
                    "rows": len(group)}

    groups = defaultdict(list)
    for row in selected:
        period = row[method.date_column] if method.date_column else "Total"
        if method.date_column:
            period = period[:7] if method.granularity == "month" else period[:4] if method.granularity == "year" else period
        key = (period, row[method.group_by] if method.group_by else "Todas")
        groups[key].append(row)
    return {"total": aggregate(selected), "series": [{"period": key[0], "group": key[1], **aggregate(group)} for key, group in sorted(groups.items())],
            "unit": method.unit, "selected_rows": len(selected), "source_rows": len(rows), "skipped_missing": skipped,
            "result_status": "provisional", "usage_authorization": "none"}
