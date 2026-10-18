# Operación y seguridad

Variables: `SII_MB_DATABASE_URL` (SQLite por defecto o PostgreSQL/psycopg), `SII_MB_UI_ORIGINS` (lista de orígenes permitidos), `NEXT_PUBLIC_API_BASE_URL` (API, definida al compilar), `SII_MB_SECURE_COOKIES=1` (obligatoria con HTTPS institucional; incompatible con demo HTTP).

Bootstrap: `python -m app.manage create-admin` solicita la contraseña sin argumentos ni archivos. Alternativamente `SII_MB_ADMIN_PASSWORD` y `SII_MB_ADMIN_USERNAME` inicializan una base sin usuarios. Nunca reemplazan cuentas existentes. El usuario inicial por defecto es admin. No hay contraseña predeterminada para la aplicación.

## Acceso

Admin: cuentas/auditoría y alcance global. Editor: crear y modificar, importar y calcular en su alcance. Viewer: consultar y exportar dentro de su alcance. Alcances separados de indicadores y fuentes: IDs, `*` o lista vacía sin acceso. Los objetos nuevos del editor se agregan a su alcance. Un resultado exige permisos de ambas entidades.

Sesiones de ocho horas, cookies HttpOnly/SameSite Strict, contraseñas scrypt con sal aleatoria. Cinco fallos bloquean temporalmente el usuario por 15 minutos. Cambiar contraseña/rol/alcance/estado revoca sesiones. Un administrador no puede quitar su propio acceso. Logout elimina sesión y cookie. Tableros personales no amplían los permisos de sus resultados.

Auditoría de accesos, cambios, valores anteriores de fichas, métodos, fuentes, cálculos exitosos/fallidos, tableros, relaciones, usuarios y exportaciones. No hay borrado de auditoría desde API. No es un archivo legalmente inalterable frente a un administrador de infraestructura.

## Persistencia y respaldos

`python -m app.manage migrate` aplica Alembic; también se aplica al iniciar API. No ejecutar migraciones simultáneas. La primera reconoce V0.1; la segunda conserva fichas y añade el núcleo. No se permite downgrade destructivo: restaurar respaldo validado.

SQLite: detener API y copiar backend/data/sii_mb.db a una ubicación protegida fuera de Git, conservando versión de código y lockfiles. PostgreSQL: pg_dump/pg_restore conforme al procedimiento institucional. Respaldar datos, métodos, ejecuciones, usuarios y auditoría. Los respaldos incluyen hashes/sesiones y son información protegida. La restauración completa debe probarse antes de operación institucional.

## Supervisión y límites

Health comprueba el proceso sin exponer datos. Errores de cálculo se muestran al usuario y quedan auditados. Cada CSV registra responsable, huella como detección de cambios y nueva carga manual como alternativa. No se afirma vigilancia automática de sistemas externos.

Antes de datos/usuarios institucionales: ejecutar PostgreSQL/Compose, carga/concurrencia y restauración; configurar HTTPS/SSO/recuperación de cuentas; separar privilegios de migración/aplicación/auditoría; definir retención y monitoreo externo; revisar bloqueo concurrente y abuso; formalizar competencias de aprobación. El cálculo actual es síncrono y acotado, hasta 10 000 filas.

No hay conectores reales BigQuery/API/Excel, trabajos en segundo plano ni despliegue en nube. No se instaló Docker. CI solo manual: publicar commits no ejecuta trabajos. Secretos, bases, cachés y resultados de prueba están excluidos de Git.
