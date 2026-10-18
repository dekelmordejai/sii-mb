# Plan inmediato de implementación · SII-MB

**Principio de ejecución:** entregar funciones utilizables en pequeños incrementos; no bloquear desarrollo por carga del inventario de indicadores. Todos los registros, fórmulas y fuentes se administrarán dinámicamente.

| Hito | Entregable verificable | Dependencia | Estado |
|---|---|---|---|
| M0 · Base local | Proyecto organizado, API, UI, base local, pruebas | Python / Node | **Incluido V0.1** |
| M1 · Alta dinámica | Crear, listar, buscar, ver y editar ficha en borrador | M0 | **Incluido V0.1** |
| M2 · Fuentes | Adjuntar CSV de prueba, inspeccionar columnas y tipos, reportar problemas | M1 | Pendiente |
| M3 · Motor mínimo | Operaciones declarativas seguras (conteo, suma, cociente de sumas); resultado, unidad y validación | M2 | Pendiente |
| M4 · Visualización | Tabla, gráfico sencillo, filtros permitidos y exportación de demostración | M3 | Pendiente |
| M5 · Identidad y control | Inicio de sesión, permisos RBAC por alcance; controles de modificaciones y registro auditable | M1-M4 | Pendiente |
| M6 · Preparación de integración | PostgreSQL, migraciones, pruebas E2E, conexión BigQuery de solo lectura con datos autorizados | M5 | Pendiente |

## Criterios de diseño imprescindibles

1. **Configuración desde la aplicación:** no codificar a mano cada indicador nuevo.
2. **Identidad estable:** nombre, dominio y presentación no son claves primarias institucionales.
3. **Fórmulas seguras:** en M3 se ofrecerá un conjunto permitido de operadores; nunca ejecutar Python/SQL arbitrario cargado por un usuario.
4. **Versionado futuro:** métodos, datos y ejecuciones referenciados por identificadores distintos; no confundir fichas con resultados.
5. **Entorno protegido:** M0-M4 se prueban SOLO en localhost y con datos sintéticos. No se usan datos reales mientras no existan controles de acceso y aprobación institucional.
6. **Aprobación separada:** el estado `draft` no equivale a una metodología vigente ni a autorización de publicación.
7. **No asumir tecnología definitiva:** SQLite permite validación rápida local; PostgreSQL queda como destino de aplicación multiusuario. No hay Cloud Run ni BigQuery conectado.

## Siguiente entrega recomendada: M2 + primer cálculo M3

Un caso vertical completo:

- Cargar un CSV sintético con `fecha`, `linea`, `km_programado`, `km_realizado`.
- Registrar un indicador genérico desde UI.
- Seleccionar `razón de sumas`: `SUM(km_realizado) / SUM(km_programado) × 100`.
- Validar columnas, ceros, faltantes, agregación y período.
- Guardar versión declarativa del cálculo y resultado trazable.
- Mostrar la serie con filtro por línea y exportación de prueba.

La operación sintética ilustra el motor, **no** declara fórmula institucional aprobada para cumplimiento de kilómetros.

## Qué NO es condición previa

- Homologar los 46 registros de `Indicadores - Matriz.csv`.
- Aprobar uno por uno los 51 acuerdos anteriores.
- Comprar infraestructura o disponer de datos institucionales.
- Crear un repositorio remoto.
