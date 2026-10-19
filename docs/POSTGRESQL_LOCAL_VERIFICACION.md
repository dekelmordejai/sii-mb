# PostgreSQL local utilizado en la verificación

Se descargó un archivo portable de PostgreSQL 17.11 desde la [página de binarios de EDB](https://www.enterprisedb.com/download-postgresql-binaries), enlazada por la [página oficial de PostgreSQL para Windows](https://www.postgresql.org/download/windows/). No se ejecutó el instalador ni se registró un servicio de Windows.

- Enlace de descarga observado: https://sbp.enterprisedb.com/getfile.jsp?fileid=1260616
- SHA-256 calculado localmente del ZIP: `80379B2C04D51C30225532E0AE04509899141E9957ED096FE749D7FD9DF8F82F`. Es la huella del archivo usado, no una afirmación de comparación con una firma independiente del distribuidor.
- Versión reportada por el ejecutable: PostgreSQL 17.11, x86_64-windows, MSVC 19.44.
- Instancia temporal: exclusivamente 127.0.0.1:55432; autenticación SCRAM con contraseña aleatoria. Archivos y credenciales de prueba fuera de Git y del ZIP del proyecto.
- Bases/indicadores/fuentes exclusivamente sintéticos. Los tests de API usan esquemas aleatorios test_sii_UUID y los eliminan al terminar. La restauración utiliza una base nueva test_sii_restore_UUID, que también se elimina.

La batería compartida se puede repetir definiendo SII_MB_TEST_POSTGRES_URL. Para el respaldo/restauración se requiere SII_MB_PG_BIN con los ejecutables de la misma versión principal y un usuario autorizado para crear la base temporal. No ejecutar esas pruebas contra una base institucional.

La prueba de restauración comprueba login, identidad exacta de una ejecución recuperada y reproducción del mismo resultado con los datos restaurados. El flujo de navegador también se probó con PostgreSQL real. Esto no equivale a una prueba de contenedores Docker ni a certificación institucional de disponibilidad o seguridad.
