# Revisión y contribuciones

Las propuestas deben incluir un problema reproducible con datos sintéticos, una descripción del cambio y su validación. Las contribuciones externas están sujetas a revisión y a acordar los permisos de uso del código; el repositorio no incorpora una licencia abierta por defecto.

## Verificaciones

Backend, desde `backend/` con el entorno activado:

```bash
python -m ruff check app tests alembic
python -m pytest -q
```

Frontend, desde `frontend/`:

```bash
npm ci
npm run typecheck
npm run format:check
npm run build
npm run test:e2e
```

Las pruebas E2E utilizan sus propios puertos y base sintética. Las pruebas PostgreSQL requieren una base dedicada y los permisos descritos en la guía. No apuntes la configuración de pruebas a una instalación con datos reales.

Mantén inmutables las fuentes y los métodos existentes, crea migraciones para cambios de esquema y prueba los controles de alcance. Una interfaz no basta para declarar completa una capacidad. No agregues secretos ni datos institucionales a commits, capturas o reportes.
