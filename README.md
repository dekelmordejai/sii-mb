# SII-MB · Primera aplicación local (V0.1.0)

**Sistema Integral de Indicadores de Metrobús** · Entregable inicial de código, sin repositorio remoto ni servicios cloud creados.

## Qué está implementado de verdad

- API REST con FastAPI y documentación interactiva (`/docs`).
- Persistencia local con SQLite y modelo separado para una identidad de indicador estable.
- Alta, consulta, búsqueda, paginación y edición de **fichas en borrador**.
- Interfaz en Next.js y TypeScript: inicio, inventario, alta, detalle y edición.
- Validación del lado del servidor; el cliente no puede autoproclamarse aprobado.
- Pruebas automatizadas para la API.
- Base preparada para reemplazar SQLite por PostgreSQL sin acoplar la interfaz al almacenamiento.

**No está implementado:** autenticación, permisos, fuentes de datos, fórmulas, cálculo, aprobación institucional, auditoría integral, observabilidad, gestión de evidencias, notificaciones y despliegue productivo. Los módulos futuros se muestran como *Próximo*, no como botones funcionales.

> **Entorno de desarrollo exclusivamente.** La API no incorpora autenticación. Mantener ambos servicios en `127.0.0.1`, no abrir puertos al exterior, no utilizar datos institucionales, confidenciales o personales.

## Requisitos previos

- Python 3.11 o superior (probado con 3.13).
- Node.js 22 LTS (probado con 22.16 en el entorno de generación).
- npm 10 o superior.
- Git instalado, solo si deseas inicializar un repositorio *local*.

No necesitas Docker, PostgreSQL, cuenta Google Cloud ni conexión a BigQuery para iniciar. `npm install` y la instalación Python sí requieren conseguir las dependencias en tu equipo.

## Iniciar en Windows (PowerShell)

Abre dos terminales en el directorio extraído:

**Terminal 1 · API**

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 · Interfaz**

```powershell
cd frontend
npm install
Copy-Item .env.local.example .env.local
npm run dev
```

Si PowerShell impide activar el entorno, utiliza `backend\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000` desde `backend/` sin cambiar políticas globales.

## Iniciar en macOS / Linux

**Terminal 1 · API**

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 · Interfaz**

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

Abrir:

- **Aplicación:** http://127.0.0.1:3000
- **Documentación API:** http://127.0.0.1:8000/docs
- **Estado API:** http://127.0.0.1:8000/api/v1/health

## Primera prueba de extremo a extremo

1. Abre la aplicación en tu navegador y confirma que la API aparece como **Conectada**.
2. Entra a **Indicadores → Nuevo indicador**.
3. Ingresa un nombre, una definición de al menos 10 caracteres y una unidad.
4. Guarda. Verifica que la aplicación abre la ficha con un código `IND-...`.
5. Regresa al inventario, busca por nombre y edita la ficha.
6. Detén y reinicia la API: la ficha debe seguir existiendo en `backend/data/sii_mb.db`.

**La base arranca vacía**. No es requisito cargar los 46 registros previos: cada indicador puede incorporarse posteriormente desde la interfaz.

## Ejecutar pruebas

En `backend/`, con el entorno activado:

```bash
python -m pytest -q
```

En `frontend/`, tras `npm install`:

```bash
npm run typecheck
npm run build
```

## Ejemplo de uso de API

```bash
curl -X POST http://127.0.0.1:8000/api/v1/indicators \
  -H 'Content-Type: application/json' \
  -d '{"name":"Intervalo observado (prueba)","definition":"Tiempo entre dos pasos consecutivos en una parada.","unit":"min","domain":"Operación"}'
```

```bash
curl 'http://127.0.0.1:8000/api/v1/indicators?q=intervalo'
```

Solo se aceptan campos explícitos. `status` es controlado por el servidor y será `draft`. Las personas usuarias no pueden aprobar un indicador desde esta API.

## Organización

```text
sii-mb-local-v0.1/
├── backend/
│   ├── app/
│   │   ├── main.py              # Aplicación / CORS restringido
│   │   ├── db.py                # Conexión y sesión a DB
│   │   ├── models.py            # Entidad Indicator
│   │   ├── schemas.py           # Contrato de datos
│   │   └── routers/indicators.py
│   ├── tests/
│   └── requirements*.txt
├── frontend/
│   ├── app/                    # Rutas Next.js
│   ├── components/
│   ├── lib/api.ts              # Cliente API tipado
│   └── package.json
├── docs/
│   ├── PLAN_INMEDIATO.md
│   ├── DECISIONES_Y_ALCANCE.md
│   └── CRITERIOS_ACEPTACION.md
└── .gitignore
```

## Base de datos

Se utiliza **SQLite por defecto, únicamente para desarrollo local**. No hay datos ficticios precargados. La identidad del indicador es independiente de su nombre, de su área y de los tableros, conforme al diseño institucional previo.

El código permite indicar `SII_MB_DATABASE_URL` para un motor PostgreSQL mediante SQLAlchemy, si se instala un controlador apropiado. Ese camino aún **no está probado ni desplegado**. Las migraciones con Alembic, los respaldos y el control de versiones metodológicas se incluirán antes de un entorno multiusuario.

## GitHub: ningún recurso externo creado

Este ZIP **no contiene un repositorio remoto** ni credenciales. Si deseas, posteriormente puedes iniciar historial Git localmente:

```bash
git init
git add .
git commit -m "chore: bootstrap sii-mb local v0.1"
```

**No ejecutar `git remote add` ni `git push` todavía.** La creación del repositorio privado en GitHub quedará sujeta a autorización explícita de nombre, propietario y controles de acceso.

## Diseño vs. funcionalidad

Las decisiones institucionales DEC-001 a DEC-051 siguen siendo el marco de referencia; **no** están todas implementadas. Los detalles finos de gobernanza/eventos se posponen y no bloquean el desarrollo del núcleo funcional. Consultar `docs/` para siguiente incremento.
