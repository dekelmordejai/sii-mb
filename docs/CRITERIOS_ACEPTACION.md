# Criterios de aceptación · V0.1

## Comprobación automatizada backend

- [ ] Endpoint de salud responde HTTP 200.
- [ ] Inventario nuevo se encuentra vacío.
- [ ] POST crea indicador en `draft` con ID y código estables.
- [ ] GET recupera el indicador y su definición.
- [ ] PATCH actualiza su borrador sin alterar el identificador.
- [ ] Campos inválidos y `status: approved` se rechazan.
- [ ] Búsqueda y paginación responden coherentemente.
- [ ] ID inexistente da HTTP 404.

## Comprobación manual de interfaz

- [ ] Página de inicio muestra estado de API y número de indicadores.
- [ ] Crear un indicador sin utilizar el CSV previo.
- [ ] Ver su ficha y editarla.
- [ ] Filtrar el inventario por texto.
- [ ] Reiniciar API sin pérdida de la ficha guardada.
- [ ] La interfaz distingue módulos pendientes de funciones reales.
- [ ] Los servidores usan solo `127.0.0.1`.

## Fuera del alcance de aceptación

No se probarán cálculos, fuentes, integraciones, autenticación ni publicaciones porque **no existen en V0.1**.
