# SII-MB — Reglas maestras del sistema

**Proyecto:** Sistema Integral de Indicadores de Metrobús (SII-MB)  
**Estado:** 51 decisiones conceptuales confirmadas; una enmienda formal.  
**Propósito de este documento:** servir como referencia funcional e institucional para construir el sistema en ChatGPT Work.

## A. Principios generales

1. **DEC-001. Plataforma integral.** El SII-MB debe evolucionar hacia una solución que administre indicadores, definiciones metodológicas, fuentes de datos, cálculos, resultados históricos, visualizaciones, permisos, versiones y auditoría.

2. **DEC-002. Diversidad de indicadores.** Podrá administrar indicadores oficiales, operativos, experimentales, propuestos e históricos. Su existencia en el sistema no implica aprobación ni autorización para publicarlos.

3. **DEC-003. Participación institucional.** Podrán participar distintas áreas de Metrobús, empresas operadoras y colaboradores externos autorizados, con funciones diferenciadas.

4. **DEC-004. Acceso restringido.** El acceso estará limitado a personal institucional autorizado y colaboradores externos expresamente habilitados. No se presupone la existencia de un portal público.

5. **DEC-005. Permisos por rol y alcance.** Los permisos considerarán tanto las funciones del usuario como el conjunto específico de información y operaciones al que puede acceder.

6. **DEC-006. Gobernanza híbrida.** La administración central podrá delegar determinadas operaciones a las áreas, bajo reglas y restricciones definidas.

7. **DEC-007. Coordinación metodológica central.** Las definiciones y aprobaciones metodológicas estarán sujetas a una autoridad coordinadora institucional.

8. **DEC-008. Coordinación propuesta por la JUD.** La Jefatura de la Unidad de Estadística y Evaluación del Servicio será la instancia coordinadora metodológica propuesta en el diseño. Las facultades reales deberán formalizarse institucionalmente.

9. **DEC-009. Participación de áreas competentes.** Los cambios que afecten operaciones, contratos, finanzas, seguridad u obligaciones normativas requerirán las consultas y autorizaciones especializadas pertinentes.

## B. Criticidad institucional

10. **DEC-010. Evaluación multidimensional.** La criticidad no se representará únicamente mediante un valor general.

11. **DEC-011. Diez dimensiones.** Se evaluarán los impactos operativo, financiero, contractual, normativo/legal, de seguridad, estratégico, reputacional, social/de atención a usuarios, de protección de información y tecnológico.

12. **DEC-012. Escala ordinal.** Los niveles serán Bajo, Moderado, Alto y Crítico. También existirán No aplica, con justificación, y Pendiente de evaluación.

13. **DEC-013. Criterios verificables.** Los niveles tendrán definiciones comunes y criterios específicos para cada dimensión.

14. **DEC-014. Tres perspectivas de evaluación.** Se distinguirán la gravedad del fenómeno medido, las consecuencias de errores en el indicador y las consecuencias de las decisiones basadas en él.

15. **DEC-015. Criticidad básica y contextual.** Cada indicador podrá tener una evaluación de base y evaluaciones específicas según sus usos.

16. **DEC-016. Evaluación contextual condicionada.** Será obligatoria en situaciones definidas; los usos ordinarios podrán apoyarse en una evaluación base aplicable.

17. **DEC-017. Activadores contextuales.** Se consideran pagos, seguridad, cumplimiento normativo, presupuestos, publicaciones oficiales, información sensible, decisiones automatizadas, cambios relevantes y riesgos adicionales identificados.

18. **DEC-018. Detección híbrida de activadores.** Los usuarios declararán el uso previsto y el sistema verificará posibles activadores mediante reglas.

19. **DEC-019. Autorización proporcional.** Los usos sensibles requerirán revisión humana; los procedimientos simplificados podrán aplicarse cuando exista autorización previa para ello.

20. **DEC-020. Autorización por naturaleza del uso.** Algunos usos requerirán autorización humana independientemente de la evaluación de impacto.

21. **DEC-021. Ocho clases de autorización especial.** Se aplicarán a determinaciones económicas o contractuales, seguridad, decisiones legales vinculantes, compromisos presupuestales, publicaciones oficiales relevantes, divulgación extraordinaria de información protegida, automatizaciones de alto impacto y excepciones a reglas aprobadas.

22. **DEC-022. Exploración provisional.** Los usuarios autorizados podrán analizar información provisional debidamente identificada. No podrán convertirla en resultados oficiales o decisiones vinculantes sin las aprobaciones necesarias.

## C. Identidad y ciclo de vida metodológico

23. **DEC-023. Tres ciclos de vida independientes.** Se separarán el estado de la metodología, el estado de los resultados calculados y la autorización de resultados para usos particulares.

24. **DEC-024. Metodologías versionadas.** Las versiones conservarán sus estados, fechas, aprobaciones y antecedentes.

25. **DEC-025 y DEC-029. Doce estados metodológicos:**
    - EM-01 Borrador.
    - EM-02 En revisión técnica.
    - EM-03 Correcciones requeridas.
    - EM-04 Validada técnicamente.
    - EM-05 Pendiente de aprobación.
    - EM-06 Aprobada no vigente.
    - EM-07 Vigente.
    - EM-08 Suspendida.
    - EM-09 Sustituida.
    - EM-10 Retirada.
    - EM-11 Rechazada.
    - EM-12 Desistida.

26. **DEC-026. Transiciones controladas.** Los estados tendrán transiciones permitidas y excepciones extraordinarias justificadas y auditables.

27. **DEC-027. Inmutabilidad de versiones aprobadas.** Los cambios sustantivos exigirán nuevas versiones; las correcciones editoriales podrán seguir un procedimiento controlado.

28. **DEC-028. Flexibilidad previa a la aprobación.** Se permitirá corregir, revisar nuevamente y desistir de propuestas mediante las reglas aplicables.

29. **DEC-030. Desistimiento institucional.** EM-12 podrá originarse desde EM-01, EM-02, EM-03, EM-04 o EM-05.

30. **DEC-031, enmendada por DEC-034.** Ningún área podrá cerrar unilateralmente una propuesta metodológica institucional, ni siquiera desde Borrador. El cierre requerirá autorización central.

31. **DEC-032. Ningún área es propietaria exclusiva de un indicador.** Una propuesta podrá continuar desarrollándose aunque el área que la inició deje de participar.

32. **DEC-033. Participación individual por área.** Se registrarán los roles, estados y antecedentes de participación de las diferentes áreas. Retirar una participación no equivale a eliminar el indicador.

33. **DEC-034. Autoridad de cierre institucional.** La JUD coordinará y autorizará el desistimiento de propuestas institucionales conforme a las facultades formalizadas.

34. **DEC-035. Verificación antes del cierre.** Se revisarán dependencias, impactos y alternativas de continuidad, consultando a las áreas vinculadas cuando corresponda.

35. **DEC-036. Expediente de cierre.** Los desistimientos tendrán documentación estructurada, con evidencia obligatoria y complementaria proporcional.

36. **DEC-037. Recuperación híbrida.** Una propuesta desistida podrá reabrirse extraordinariamente o dar origen a una nueva propuesta vinculada.

37. **DEC-038. Evaluación integral de continuidad.** Se analizarán cambios metodológicos, fuentes, vigencia de evidencias, tiempo transcurrido y dependencias antes de decidir.

38. **DEC-039. Estados de reapertura.** El expediente podrá regresar únicamente a EM-01 o EM-02 mediante autorización, sin restaurar automáticamente validaciones anteriores.

## D. Evidencias y control de cambios

39. **DEC-040. Revalidación selectiva.** Cada evidencia podrá reutilizarse, actualizarse o invalidarse según una evaluación individual trazable.

40. **DEC-041. Vigencia híbrida.** Se combinarán reglas por eventos, periodos de revisión y verificaciones periódicas según el tipo de evidencia.

41. **DEC-042. Diez categorías de evidencia:**
    - EV-01 Conceptual y matemática.
    - EV-02 Operativa y de negocio.
    - EV-03 Normativa y contractual.
    - EV-04 Fuentes de datos y linaje.
    - EV-05 Calidad y conciliación de datos.
    - EV-06 Cálculo e implementación técnica.
    - EV-07 Estadística y empírica.
    - EV-08 Agregación y temporalidad.
    - EV-09 Revisión y autorización institucional.
    - EV-10 Seguridad y protección de información.

42. **DEC-043. Motor de eventos y dependencias.** Los cambios registrados podrán activar revisiones sobre los objetos relacionados, sin invalidarlos indiscriminadamente.

43. **DEC-044. Doce categorías de eventos:**
    - EVT-01 Cambio metodológico.
    - EVT-02 Cambio de reglas de negocio.
    - EVT-03 Cambio de estructura de datos.
    - EVT-04 Corrección o modificación de datos.
    - EVT-05 Deterioro de calidad.
    - EVT-06 Cambio en catálogos y relaciones.
    - EVT-07 Cambio normativo o contractual.
    - EVT-08 Cambio temporal o de cobertura.
    - EVT-09 Modificación tecnológica.
    - EVT-10 Cambio de autorizaciones.
    - EVT-11 Cambio de seguridad o acceso.
    - EVT-12 Cambio en dependencias.

44. **DEC-045. Cobertura de supervisión.** Cada fuente incorporada deberá contar con mecanismos de detección de cambios, responsables y procedimientos alternativos. No todas las fuentes necesitan integración automática.

## E. Responsabilidades y atención de eventos

45. **DEC-046. Responsabilidades distribuidas.** Las áreas responsables de fuentes, los equipos técnicos, los responsables funcionales y la JUD tendrán funciones diferenciadas.

46. **DEC-047. Titulares y suplentes.** Se vincularán responsabilidades con funciones institucionales, personas titulares, suplentes autorizados y periodos de vigencia.

47. **DEC-048. Escalamiento multidimensional.** Se considerarán plazos, criticidad, urgencia, disponibilidad de responsables, bloqueos, incertidumbre y consecuencias sensibles.

48. **DEC-049. Prioridad contextual.** La prioridad operativa será distinta de la criticidad institucional y se determinará según las circunstancias de cada evento.

49. **DEC-050. Cuatro niveles operativos:**
    - PO-01 Inmediata.
    - PO-02 Alta.
    - PO-03 Ordinaria.
    - PO-04 Baja.
    - «Pendiente de clasificación» será un estado temporal independiente, no una quinta prioridad.

50. **DEC-051. Matriz común y reglas especiales.** La prioridad se determinará mediante criterios comunes, complementados con reglas para contextos sensibles y revisión humana cuando corresponda.

51. **DEC-052 no aprobada.** Los detalles de activación de PO-01, plazos y demás parametrizaciones de eventos se encuentran diferidos.

## F. Reglas arquitectónicas y de implementación acordadas posteriormente

**Estas reglas tienen prioridad para organizar el desarrollo práctico. No eliminan las decisiones anteriores, sino que determinan cuándo implementarlas.**

1. El objetivo principal es construir una aplicación real, funcional, extensible y mantenible, no producir únicamente documentos, prototipos visuales o especificaciones.

2. El sistema debe admitir la creación de indicadores dinámicamente desde la interfaz, incluso después de que la plataforma esté completamente desarrollada.

3. El catálogo actual de 46 registros es material de referencia y prueba, no un requisito previo de construcción. No es necesario homologar ni cargar todos esos indicadores antes de avanzar.

4. Los indicadores, las versiones metodológicas, las fuentes, las ejecuciones, los resultados y los tableros son entidades diferenciadas.

5. Los usuarios autorizados deberán poder crear, editar, configurar, consultar, desactivar y relacionar indicadores, respetando permisos e historial.

6. El cálculo de indicadores deberá ser configurable y seguro. No se permitirá ejecutar código arbitrario proporcionado por los usuarios como fórmula.

7. Los cálculos deberán contemplar granularidad, unidades, filtros, valores faltantes, denominadores cero, reglas de agregación y periodos de vigencia.

8. Los resultados deberán ser reproducibles y conservar referencias a la metodología, parámetros, fuentes y ejecución utilizada.

9. La plataforma permitirá incorporar nuevas fuentes de información sin rediseñar la aplicación. Se comenzará con CSV y datos sintéticos; posteriormente podrán incorporarse BigQuery, API y otros conectores.

10. Deberá incluir gráficas, tablas, filtros, comparativos, exportaciones y tableros configurables.

11. La experiencia de usuario debe ser profesional, clara, rápida y responsiva. Se prefieren interfaces limpias, tipografía legible, visualizaciones ejecutivas y filtros intuitivos.

12. La autenticación, autorización, validación de entradas, manejo seguro de secretos y auditoría no deberán quedar fuera de una versión destinada a usuarios reales.

13. Las funciones avanzadas de gobernanza deberán implementarse de forma incremental, sin bloquear la entrega de un MVP funcional.

14. La tecnología propuesta inicialmente es Next.js/React, FastAPI/Python, PostgreSQL y Plotly, con integración futura de BigQuery. Se podrán realizar ajustes técnicos justificados.

15. El desarrollo comenzará en GitHub privado y entorno local. No se crearán recursos en la nube ni se utilizarán datos institucionales sensibles sin autorización específica.

16. La versión V0.1 ya entregada, basada en Next.js, FastAPI y SQLite, será el punto de partida para inspección y aprovechamiento, no una implementación que deba conservarse sin cambios.

17. Cada módulo deberá incluir código ejecutable, pruebas, documentación y criterios de aceptación verificables.

18. Work deberá avanzar de manera autónoma en lo técnicamente autorizado, solicitar aprobación únicamente ante decisiones bloqueantes, permisos externos o cambios materiales de alcance.

19. No se considerará terminada una funcionalidad solo porque exista su interfaz. Deberá operar realmente y superar sus pruebas.

20. El avance se medirá por capacidades funcionando y entregables utilizables, no por el número de decisiones, documentos o formularios creados.

**Principio rector:** primero una plataforma genérica completa y extensible; posteriormente, la incorporación progresiva de indicadores y fuentes institucionales reales.
