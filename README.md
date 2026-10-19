# SII-MB · Núcleo funcional local V0.2

Sistema Integral de Indicadores de Metrobús. Basado en el ZIP V0.1 recibido el 18/10/2026. Solo datos sintéticos; sin catálogo institucional precargado.

## Implementado

- Indicadores dinámicos con identidad estable, dimensiones, edición, búsqueda, desactivación/reactivación y relaciones. Desactivar no es desistir institucionalmente.
- CSV UTF-8: inspección previa, tipos configurables, vista previa, faltantes y validación. Instantáneas inmutables con SHA-256. Hasta 1 MB, 10 000 filas, 50 columnas.
- Métodos inmutables versionados: conteo, suma, promedio, mínimo, máximo, razón de sumas y expresiones compuestas con operadores permitidos. Sin ejecución de código de usuarios.
- Unidad del método, multiplicador, agrupación, granularidad temporal, filtros, periodo, vigencia y política explícita de faltantes/cero.
- Ejecuciones históricas con parámetros, fuente, método, huella y motor. Reproducción como nueva ejecución.
- Gráficas, tablas, rankings, resumen, comparación de ejecuciones, tableros personales persistidos, CSV protegido e impresión de reportes.
- Autenticación por sesiones, roles y alcances independientes de indicadores/fuentes, administración de usuarios, revocación y auditoría.
- Migraciones Alembic, pruebas automatizadas, dependencias resueltas y preparación Docker Compose/PostgreSQL.

**Los métodos son borradores, los resultados son provisionales y no autorizan usos institucionales.** El núcleo local está implementado; la plataforma integral todavía no se declara terminada ni apta para datos reales. [Plan y pendientes](docs/PLAN_IMPLEMENTACION.md).

## Windows: inicio local sin Docker

Requisitos: Python 3.12, Node.js 24, npm; Edge para las pruebas de navegador.

Desde la raíz del proyecto, primera ejecución:

```powershell
.\scripts\start-local.ps1 -Install -CreateAdmin
```

La contraseña se solicita en la terminal, mínimo 12 caracteres; no hay contraseña predeterminada. Usuario inicial: admin. Ejecuciones posteriores:

```powershell
.\scripts\start-local.ps1
```

Abre http://127.0.0.1:3000 . API: http://127.0.0.1:8000/docs . Usa el mismo host para interfaz/API; no mezcles localhost con 127.0.0.1. Ctrl+C detiene los servicios del script. La base vacía se crea en backend/data/sii_mb.db.

### Inicio manual / Linux / macOS

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt
python -m app.manage create-admin
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

En otra terminal:

```bash
cd frontend
npm ci
npm run dev
```

En Windows usa el ejecutable backend\.venv\Scripts\python.exe sin activar el entorno si lo prefieres. Si Python 3.12 no está instalado, instala esa versión o crea el entorno con una versión compatible y vuelve a verificar las dependencias.

## Docker Compose / PostgreSQL

**PostgreSQL 17.11 verificado localmente**, incluidas migraciones, cálculo, navegador y respaldo/restauración. La configuración de contenedores Compose sigue pendiente de ejecución: no se instaló Docker ni se desplegó infraestructura externa.

1. Copia .env.example a .env.
2. Define SII_MB_DB_PASSWORD (aleatoria, caracteres seguros para URL) y SII_MB_ADMIN_PASSWORD (distinta, al menos 12 caracteres).
3. Ejecuta `docker compose up --build`.
4. Abre http://127.0.0.1:3000 . PostgreSQL solo es accesible en la red interna y los puertos web se vinculan a loopback.

Prueba de integración: `docker compose --profile test run --rm test`. Utiliza un esquema temporal propio. Detener: `docker compose down`, conservando el volumen. No uses `down -v` para conservar los datos.

## Primer flujo verificable

1. Inicia sesión; comprueba que Indicadores está vacío.
2. En Fuentes pulsa Preparar ejemplo sintético, revisa tipos y guarda.
3. Crea un indicador ficticio con unidad % y dimensiones fecha, grupo.
4. En su ficha selecciona la fuente, razón de sumas, numerador valor, denominador base, multiplicador 100, fecha fecha y agrupación grupo.
5. Guarda versión y ejecuta: total esperado **81.666666… %**, resultado de 245 / 300 × 100.
6. Filtra grupo = A: **85 %**. Los límites de fecha son inclusivos.
7. Modifica el método y guarda otra versión. Los resultados anteriores conservan su definición y procedencia.
8. En Resultados consulta, compara, reproduce y exporta. En Tableros añade componentes, guarda y recarga.

El ejemplo solo prepara datos en el formulario: nada se precarga al arrancar.

## Pruebas

```powershell
.\scripts\verify.ps1
```

Por separado: `python -m pytest -q` desde backend; `npm run typecheck`, `npm run build`, `npx playwright test` desde frontend. E2E inicia sus propios servidores 8100/3100 y una base sintética independiente.

Linux/Chromium: `npx playwright install chromium` y SII_MB_BROWSER_CHANNEL=chromium. PostgreSQL: SII_MB_TEST_POSTGRES_URL debe apuntar a una base local dedicada a pruebas; cada caso utiliza un esquema test_sii_UUID. Para probar respaldo/restauración define también SII_MB_PG_BIN con el directorio de pg_dump/pg_restore; se crea y elimina exclusivamente una base test_sii_restore_UUID. E2E puede usar SII_MB_TEST_DATABASE_URL hacia una base vacía de pruebas; nunca apuntar a una base de usuarios reales.

GitHub Actions requiere ejecución manual; publicar código no activa trabajos ni despliegues.

## Documentación

[Hitos](docs/PLAN_IMPLEMENTACION.md) · [Verificación](docs/VERIFICACION_V02.md) · [Motor](docs/MOTOR.md) · [Operación](docs/OPERACION.md) · [Reglas originales](docs/REGLAS_MAESTRAS.md) · [Instrucciones originales](docs/INSTRUCCIONES_DESARROLLO.md) · [Trazabilidad DEC](docs/TRAZABILIDAD_DEC.md).

Arquitectura: Next.js/React/TypeScript; FastAPI/SQLAlchemy; Alembic; SQLite y PostgreSQL verificados. Gráficas SVG accesibles sin una biblioteca externa adicional. backend/app/connectors.py define la frontera para adaptadores futuros de confianza.

## Alcance pendiente

Ejecución de contenedores Compose, carga/concurrencia, restauración conforme al procedimiento institucional definitivo, recuperación de cuentas, HTTPS/SSO y revisión de seguridad institucional. La recuperación sintética en PostgreSQL ya fue verificada. Gobernanza avanzada EM/EV/EVT/PO y criticidad se incorporarán progresivamente. Tampoco se incluyen conectores institucionales reales, trabajos asíncronos ni tableros compartidos. El rol técnico admin no confiere autoridad metodológica institucional. No se han usado datos reales ni desplegado servicios en nube.
