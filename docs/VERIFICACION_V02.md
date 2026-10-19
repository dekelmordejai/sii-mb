# Verificación V0.2 · 18 de octubre de 2026

## Comprobado

| Comprobación final | Resultado |
|---|---|
| Backend PostgreSQL 17.11 | 38 aprobadas, ninguna omitida |
| Backend SQLite | 35 aprobadas, tres específicas de PostgreSQL omitidas |
| Navegador Edge sobre PostgreSQL | Tres aprobadas |
| TypeScript / build Next.js | Aprobados |
| Ruff / formato Prettier | Aprobados |

- Punto de partida: ocho pruebas originales V0.1 aprobadas y compilación Next.js realizada en este equipo.
- SQLite: 35 pruebas aprobadas; tres pruebas específicas de PostgreSQL omitidas explícitamente. Se verifican CSV, esquema/faltantes, valores no finitos, operadores no permitidos, agregaciones, vigencia, filtros, cero, versiones, reproducción, tableros, auditoría, revocación y permisos por alcance.
- PostgreSQL 17.11: batería compartida verificada más integración, respaldo/restauración y concurrencia. Se utiliza una instancia temporal en loopback; ninguna base real ni servicio Windows instalado. La prueba de concurrencia realiza doce altas paralelas con el mismo editor y comprueba que se conserven todos sus alcances.
- Migración de una base sin historial Alembic equivalente a V0.1: conserva una identidad y agrega los nuevos campos sin pérdida.
- TypeScript y compilación Next.js completados sin errores.
- Playwright/Edge con PostgreSQL: tres pruebas aprobadas. El flujo completo comienza vacío, importa CSV, registra un indicador desde UI, calcula 245/300 × 100, grafica, exporta, crea V2 con otra unidad y V3 con expresión compuesta, guarda/recarga un tablero, comprueba móvil sin desbordamiento, consulta auditoría y cierra sesión. Se prueban además acceso obligatorio/error de ingreso y creación de una cuenta viewer desde UI, verificando consulta sin acciones de edición.
- El flujo original de dos pruebas también pasó en SQLite; las tres pruebas actuales se verificaron con PostgreSQL. No se presenta una ejecución anterior como prueba de una variante posterior no ejecutada.
- Respaldo/restauración: pg_dump en formato custom, restauración en otra base sintética y comprobación del login, identidad exacta de una ejecución histórica y reproducción de su resultado.
- Capturas de escritorio y móvil inspeccionadas visualmente.
- npm informó cero vulnerabilidades al resolver dependencias en esta entrega. No sustituye una revisión de seguridad institucional.

Entorno utilizado: Windows, Python 3.12.14, Node 24.21.0, Next.js 16.4.2; versiones exactas en los lockfiles.

## No verificado / no declarado terminado

- Docker Compose: sus archivos están preparados; los contenedores no se ejecutaron porque Docker no está instalado. PostgreSQL sí se ejecutó y probó de forma nativa portable.
- No se probaron despliegues, SSO/TLS institucional, procedimientos institucionales de recuperación, carga general multiusuario ni todas las combinaciones posibles de fórmulas, permisos y visualizaciones. La prueba puntual de doce altas no equivale a una prueba general de carga.
- Los controles institucionales avanzados EM/EV/EVT/PO y criticidad permanecen diferidos conforme a las instrucciones. Los resultados no tienen autorización de uso.
- No se utilizaron datos reales ni se conectaron fuentes institucionales.

Los informes V0.1 se conservan como antecedentes y no describen el alcance de V0.2. Comandos para repetir verificaciones: README.md y scripts/verify.ps1.

Procedencia del motor de base de datos: POSTGRESQL_LOCAL_VERIFICACION.md. Los XML de verificación se entregan por separado y no se suben al repositorio como datos de aplicación. La advertencia de compatibilidad heredada de Starlette/httpx en las pruebas no produjo fallos; las dependencias están fijadas para poder repetir este entorno.
