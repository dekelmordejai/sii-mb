# SII-MB — Instrucciones definitivas de desarrollo

## Objetivo principal

Desarrolla integralmente el **Sistema Integral de Indicadores de Metrobús (SII-MB)**, incluyendo su aplicación web, backend, bases de datos, motor de cálculo, visualizaciones, administración, seguridad, pruebas y repositorio de GitHub.

**La prioridad absoluta es construir el sistema completo. Los indicadores particulares se registrarán posteriormente, una vez que exista la plataforma.**

No quiero continuar con la clasificación o documentación de indicadores específicos ni realizar otro levantamiento extenso de requisitos.

## 1. Exclusión explícita del inventario de indicadores

Durante la construcción:

- NO analizar el archivo `Indicadores - Matriz.csv`.
- NO utilizar el inventario de 46 indicadores.
- NO homologar, clasificar ni normalizar indicadores existentes.
- NO diseñar módulos alrededor de indicadores particulares de Metrobús.
- NO precargar indicadores institucionales.
- NO condicionar el desarrollo a disponer de fórmulas, fuentes o definiciones reales.
- NO considerar la integración de indicadores existentes como un hito necesario para terminar el sistema.

Las estructuras de datos para crear y administrar indicadores sí son necesarias. **Lo que queda fuera es el contenido del inventario actual, no la funcionalidad para registrar indicadores dinámicamente.**

Para desarrollar y probar la plataforma, utiliza únicamente indicadores ficticios y datos sintéticos creados específicamente para las pruebas.

## 2. Comportamiento esperado del sistema terminado

Una vez desarrollado, el SII-MB deberá permitir a sus usuarios autorizados:

1. Crear indicadores nuevos desde la interfaz.
2. Definir su nombre, descripción, unidad y dimensiones.
3. Configurar metodologías y fórmulas.
4. Vincular fuentes de información.
5. Establecer reglas de cálculo y agregación.
6. Ejecutar cálculos.
7. Generar y consultar resultados.
8. Crear gráficas y tableros.
9. Analizar información con filtros y comparativos.
10. Consultar resultados históricos.
11. Administrar versiones y cambios.
12. Gestionar usuarios y permisos.
13. Exportar información y reportes.
14. Configurar nuevos indicadores sin intervención de desarrolladores.

El sistema deberá ser capaz de admitir indicadores de diferentes naturalezas: porcentajes, razones, tasas, conteos, sumas, promedios, índices compuestos, series temporales y otros cálculos que se incorporen mediante un mecanismo extensible y seguro.

## 3. Arquitectura de referencia

Construye una aplicación web utilizando preferentemente:

- **Frontend:** Next.js, React y TypeScript.
- **Backend:** FastAPI y Python.
- **Base de datos:** PostgreSQL.
- **Migraciones:** Alembic.
- **Motor de cálculo:** motor propio de expresiones controladas, con procesamiento analítico según corresponda.
- **Visualizaciones:** Plotly o biblioteca equivalente.
- **Entorno local:** Docker Compose.
- **Repositorio:** GitHub privado.
- **Pruebas:** Pytest, pruebas de frontend y Playwright.

La arquitectura debe permitir futuras conexiones con BigQuery, API, archivos CSV, Excel y otras fuentes de datos.

Puedes modificar las tecnologías propuestas cuando exista una justificación técnica sólida.

## 4. Módulos que deben desarrollarse

### Módulo A. Aplicación institucional

Diseña una interfaz profesional, responsiva y moderna, con navegación completa, formularios, tablas, buscadores y paneles de administración.

### Módulo B. Gestión dinámica de indicadores

Construye la funcionalidad para crear, consultar, modificar, versionar, desactivar y relacionar indicadores desde la aplicación.

El sistema debe comenzar sin indicadores institucionales precargados.

### Módulo C. Administración de fuentes

Permite registrar fuentes, importar archivos, explorar sus campos, definir tipos de datos, validar información y administrar conexiones.

Prepara una arquitectura extensible para futuras integraciones.

### Módulo D. Motor semántico y de cálculo

Implementa un sistema configurable para definir expresiones, variables, operaciones matemáticas, agregaciones, filtros, condiciones y temporalidad.

Las fórmulas deben evaluarse de forma segura, sin permitir ejecución arbitraria de código.

### Módulo E. Ejecución e históricos

Desarrolla mecanismos para ejecutar cálculos, registrar parámetros, conservar resultados históricos, consultar ejecuciones anteriores y permitir reproducibilidad.

### Módulo F. Visualizaciones y tableros

Implementa herramientas para generar gráficas, tablas, series temporales, rankings, indicadores resumen, comparativos y tableros configurables.

Los usuarios deberán poder construir visualizaciones a partir de los indicadores que declaren.

### Módulo G. Usuarios, permisos y auditoría

Implementa autenticación, roles, controles de autorización, protección de información, registros de actividad y administración de usuarios.

### Módulo H. Administración y operación

Incluye configuración del sistema, supervisión de ejecuciones, manejo de errores, documentación técnica, pruebas y herramientas necesarias para mantener la plataforma.

## 5. Repositorio privado de GitHub

El proyecto deberá administrarse mediante un repositorio privado.

Nombre propuesto: `dekelmordejai/sii-mb`.

Antes de crearlo, solicita confirmación de la cuenta, el nombre y los permisos necesarios.

El repositorio deberá contener el código completo, las pruebas, las configuraciones, las migraciones, la documentación y los archivos necesarios para ejecutar localmente la aplicación.

Utiliza la V0.1 de código entregada anteriormente como punto de partida, revisándola y modificándola según sea necesario.

No publiques datos institucionales ni credenciales.

## 6. Orden de ejecución

Trabaja en este orden:

**Primera etapa:**
Construir y verificar la infraestructura, la aplicación web, el backend y la base de datos.

**Segunda etapa:**
Implementar la gestión dinámica de indicadores y fuentes.

**Tercera etapa:**
Implementar el motor configurable de cálculo.

**Cuarta etapa:**
Incorporar resultados, históricos, gráficas y tableros.

**Quinta etapa:**
Completar autenticación, permisos, auditoría y administración.

**Sexta etapa:**
Realizar integración, pruebas de extremo a extremo, correcciones y preparación para despliegue.

No interpretes estas etapas como proyectos independientes. Deben desarrollarse sobre una arquitectura común y un repositorio único.

## 7. Pruebas funcionales

Para verificar el sistema se utilizarán datos e indicadores completamente sintéticos.

Deberá demostrarse al menos el siguiente flujo:

1. Iniciar el sistema sin indicadores precargados.
2. Registrar una fuente de datos sintética.
3. Crear un indicador ficticio desde la interfaz.
4. Configurar su fórmula.
5. Ejecutar el cálculo.
6. Comprobar que el resultado es correcto.
7. Crear una gráfica.
8. Guardar el resultado.
9. Consultar el historial.
10. Modificar la metodología y comprobar el funcionamiento del versionado.

Estos indicadores sintéticos son exclusivamente instrumentos de prueba, no contenido institucional que deba incorporarse a la aplicación definitiva.

## 8. Requisitos de calidad

El sistema debe:

- Funcionar realmente, no limitarse a una maqueta.
- Tener una arquitectura modular.
- Permitir incorporar indicadores sin cambiar el código.
- Mantener consistencia entre interfaz, backend y base de datos.
- Incluir validación de entradas y manejo de errores.
- Proteger credenciales e información sensible.
- Mantener trazabilidad de cálculos y modificaciones.
- Contar con pruebas automatizadas.
- Poder ejecutarse localmente de manera reproducible.
- Estar preparado para crecer en usuarios, fuentes e indicadores.

## 9. Gobernanza institucional

Conserva las decisiones DEC-001 a DEC-051 como referencia de requisitos institucionales y arquitectura futura.

Sin embargo, **no bloquees el desarrollo de la plataforma por la implementación de todos los procesos avanzados de gobernanza**.

Las funcionalidades más complejas de autorización, criticidad, evaluación de evidencias y supervisión de eventos podrán incorporarse progresivamente.

Prioriza primero el funcionamiento completo del núcleo del sistema.

## 10. Método de trabajo

Utiliza ChatGPT Work para desarrollar, revisar, ejecutar, corregir y probar el proyecto.

Evita solicitar autorizaciones para decisiones técnicas menores que puedan resolverse conforme a buenas prácticas de ingeniería.

Solicita autorización cuando sea necesario crear recursos externos, acceder a cuentas, incurrir en costos, conectar datos reales o modificar permisos sensibles.

No utilices servicios en la nube ni datos institucionales reales sin aprobación.

Trabaja por hitos verificables, documenta las funcionalidades terminadas y mantén actualizado el repositorio autorizado.

**No consideres terminado un módulo únicamente porque sus pantallas existan: deberán funcionar correctamente.**

## 11. Resultado final esperado

Quiero recibir una plataforma SII-MB completa, probada y documentada, que pueda ejecutarse inicialmente en un entorno local y posteriormente desplegarse en infraestructura institucional.

Una vez construido el sistema, comenzaremos a declarar en él los indicadores que necesitemos, utilizando las herramientas de configuración desarrolladas.

**La construcción del sistema es independiente del listado actual de indicadores.**

No vuelvas a dedicar esfuerzos a la matriz, su clasificación o su homologación durante esta fase.

Comienza por revisar el código V0.1, preparar el repositorio privado previa autorización y desarrollar progresivamente el sistema completo.
