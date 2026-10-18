# Hitos y criterios verificables

Referencia: reglas maestras e instrucciones definitivas entregadas por el usuario. El inventario institucional está expresamente excluido. Fecha: 18/10/2026.

| Hito | Criterio de salida | Estado |
|---|---|---|
| H0 · Revisar V0.1 | Ocho pruebas originales, compilación UI, preservar código de origen | Verificado; commit de base conservado |
| H1 · Infraestructura | Migraciones, arranque vacío, persistencia y conservación de identidades V0.1 | SQLite verificado; Compose/PostgreSQL preparados, pendientes de ejecutar |
| H2 · Indicadores y fuentes | Alta/edición/dimensiones/desactivación/relaciones; inspección CSV, esquema y datos inmutables | Implementado; flujo principal en navegador y API probado |
| H3 · Motor | Operaciones básicas/compuestas seguras, filtros, periodos, faltantes y cero explícitos | Implementado y probado con datos sintéticos |
| H4 · Análisis | Calcular, recuperar, reproducir, versionar, exportar y persistir tableros | Flujo principal verificado en navegador; comparativos disponibles |
| H5 · Identidad | Sesiones, roles y alcance, revocación, administración y auditoría | Casos positivos/negativos en API; login/logout y auditoría en navegador |
| H6 · Preparación institucional | Integración PostgreSQL/Compose, carga, restauración, recuperación de cuentas, TLS/SSO y revisión de seguridad | Pendiente; no apto aún para datos/usuarios institucionales |
| H7 · Gobernanza | Estados EM, autorizaciones, criticidad, cierre, EV, EVT y PO | Diferido explícitamente; no bloquea el núcleo |
| H8 · Conectores reales | Adaptadores y datos aprobados específicamente | Futuro; sin conexiones creadas |

## Revisión de V0.1

- Ocho pruebas originales aprobadas y compilación Next.js verificada en este equipo; el ZIP declaraba pendiente compilar la UI.
- No existían fuentes, cálculo, históricos, autenticación, auditoría ni migraciones. Sus referencias visuales no eran implementaciones.
- Se agregan resoluciones exactas de dependencias Python/npm.
- Alembic reemplaza `create_all` como mecanismo de actualización. Una prueba verifica la adopción de una base V0.1 conservando una identidad existente.
- Métodos, fuentes y ejecuciones se separan en entidades inmutables. Correcciones crean versiones/instantáneas nuevas.
- Lectura, reproducción, exportación y tablero comprueban acceso tanto al indicador como a la fuente.
- E2E detectó y permitió corregir el arranque con una ruta SQLite cuyo directorio no existía.
- Navegación con etiquetas accesibles verificadas en navegador.

H6 exige ejecutar pruebas en un equipo con Docker o PostgreSQL local. Tener sus archivos no equivale a haberlos ejecutado. El sistema integral no se marca terminado por la existencia de sus pantallas.
