# Motor declarativo decimal-1

Cada guardado crea una versión metodológica inmutable. No hay rutas de edición/borrado de métodos, fuentes ni ejecuciones. SHA-256 identifica el contenido UTF-8 almacenado de la fuente; no los metadatos del archivo.

Operaciones: `count`, `sum`, `mean`, `min`, `max`, `ratio_of_sums`, `expression`. El total se calcula sobre las filas seleccionadas, no mediante promedio de porcentajes agrupados. Aritmética Decimal, precisión de 50 dígitos, redondeo half-even. Se almacenan cadenas decimales; la gráfica y el resumen solo redondean para presentación.

Entradas numéricas finitas de magnitud máxima 1e18 y hasta 12 decimales. Fechas exactas YYYY-MM-DD; periodo y vigencia inclusivos. Agrupación por columna y granularidad diaria/mensual/anual.

## Expresiones

Árbol JSON de operadores permitidos, hasta 64 nodos y profundidad 8. Nunca ejecuta Python, SQL ni funciones externas.

```json
{"operation":"expression","unit":"%","expression":{"op":"multiply","args":[{"op":"divide","args":[{"op":"sum","column":"valor"},{"op":"sum","column":"base"}]},{"op":"literal","value":100}]}}
```

Constantes `literal`; agregaciones `count/sum/mean/min/max`; operaciones binarias `add/subtract/multiply/divide`. Una agregación admite `"where":{"column":"grupo","eq":"A"}`. Se pueden componer tasas, razones e índices ponderados. El formulario de operaciones básicas no requiere escribir expresiones; el editor JSON permite composición avanzada.

## Calidad

La fuente admite tipos texto/número/fecha, valida valores no vacíos e informa faltantes. El método puede rechazar faltantes numéricos, omitir la fila informando el conteo o sustituir por cero explícitamente. Las columnas numéricas de una expresión se validan sobre todas las filas seleccionadas aunque una condición interna excluya alguna. Fechas/grupos faltantes y números inválidos siempre producen error. Selección vacía: HTTP 422, no cero ficticio.

Denominador agregado cero: `value=null, status=zero_denominator`. Subexpresión indefinida: `null, status=undefined`. No se genera infinito ni se oculta un error con cero.

## Reproducción y vidas independientes

La ejecución conserva solicitud, método, fuente, huella, motor, fecha, total y serie. Reproducir genera otra ejecución con las mismas referencias. Si la versión del motor cambia, se exige su entorno histórico y se responde 409, sin simular compatibilidad. Git y lockfiles conservan el entorno de código.

Los fallos de cálculo se registran en auditoría con parámetros y diagnóstico, sin inventar resultados. La reproducción requiere permisos actuales e indicador activo.

Todos los métodos están en borrador, los resultados son provisionales y no existe autorización de uso institucional. El rol técnico admin no equivale a autoridad metodológica.
