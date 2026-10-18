# Verificación V0.2 · 18 de octubre de 2026

## Comprobado

- Punto de partida: ocho pruebas originales V0.1 aprobadas y compilación Next.js realizada en este equipo.
- Backend: 31 pruebas aprobadas con SQLite y una prueba PostgreSQL omitida explícitamente por falta de servidor, incluidas validación de CSV, tipos/faltantes, números no finitos, operadores no permitidos, vigencia, filtros, denominador cero, versiones, reproducción, tableros, auditoría, revocación y permisos por alcance.
- Migración de una base sin historial Alembic equivalente a V0.1: conserva una identidad y agrega los nuevos campos sin pérdida.
- TypeScript y compilación Next.js completados sin errores.
- Playwright/Edge: dos pruebas aprobadas. El flujo completo comienza con catálogo vacío; importa una fuente sintética, registra un indicador desde UI, calcula la razón 245/300 × 100, grafica, exporta CSV, crea V2 con multiplicador 1 y otra unidad, guarda un tablero, recarga y comprueba persistencia, verifica vista móvil sin desbordamiento, consulta auditoría y cierra sesión. La segunda verifica acceso obligatorio y error de ingreso inválido.
- Capturas de escritorio y móvil inspeccionadas visualmente.
- npm informó cero vulnerabilidades al resolver dependencias en esta entrega. No sustituye una revisión de seguridad institucional.

Entorno utilizado: Windows, Python 3.12.14, Node 24.21.0, Next.js 16.4.2; versiones exactas en los lockfiles.

## No verificado / no declarado terminado

- Docker Compose y PostgreSQL: Docker no está instalado en este equipo. Existe una prueba de integración optativa y configuración ejecutable; no se cuenta como aprobada sin ejecución.
- No se probaron despliegues, SSO/TLS institucional, restauración completa, carga multiusuario ni todas las combinaciones posibles de fórmulas, permisos y visualizaciones.
- Los controles institucionales avanzados EM/EV/EVT/PO y criticidad permanecen diferidos conforme a las instrucciones. Los resultados no tienen autorización de uso.
- No se utilizaron datos reales ni se conectaron fuentes institucionales.

Los informes V0.1 se conservan como antecedentes y no describen el alcance de V0.2. Comandos para repetir verificaciones: README.md y scripts/verify.ps1.
