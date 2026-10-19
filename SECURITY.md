# Seguridad y alcance de la demostración

Este proyecto está destinado al desarrollo local con datos sintéticos. Hacer público el código no publica una instancia de la aplicación ni concede acceso a bases de datos.

## Controles implementados

- Autenticación por sesión, cookies HttpOnly/SameSite y contraseñas scrypt con sal aleatoria.
- Roles y alcances separados de indicadores y fuentes; controles en lectura, escritura, reproducción y exportación.
- Validación de entradas y expresiones declarativas con operadores permitidos, límites de tamaño y complejidad.
- Auditoría y revocación de sesiones; archivos de entorno y bases excluidos de Git.

Las credenciales de pruebas son ficticias y están confinadas a entornos de prueba independientes. No deben reutilizarse en una instalación accesible por terceros.

## Límites conocidos

La configuración predeterminada escucha en loopback. Antes de exponer una instalación se requieren HTTPS, cookies seguras, identidad y recuperación de cuentas apropiadas, revisión de permisos de infraestructura y pruebas adicionales de abuso/carga. No se presenta el proyecto como un servicio de producción certificado ni como un sistema institucional aprobado.

## Reportes

No publiques contraseñas, tokens, datos personales, respaldos ni información institucional en issues o pull requests. Un reporte público solo debe contener un caso de reproducción sintético y sin secretos. Para vulnerabilidades que requieran información sensible, acuerda primero un canal privado con la persona mantenedora a través de su perfil de GitHub.
