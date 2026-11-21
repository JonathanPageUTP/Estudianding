# 9. Plan de gestión de la calidad

*Plataforma de tutorías entre estudiantes (TutorFISC) · Gerencia de Proyectos Informáticos (8469) · 1LS241*

## Estándares aplicables

| Estándar / norma | Aplicación en el proyecto |
|---|---|
| Guía del PMBOK® 7.ª ed. (PMI) y Guía de Scrum 2020 | Marco de gestión híbrido: planificación predictiva y construcción por sprints. |
| ISO/IEC 25010 (calidad del producto de software) | Características evaluadas: adecuación funcional, eficiencia de desempeño, usabilidad, fiabilidad y seguridad. |
| ISO/IEC/IEEE 29119 (pruebas de software) | Estructura del plan, casos e informes de prueba. |
| WCAG 2.1 nivel AA | Accesibilidad de la interfaz web responsive. |
| OWASP Top 10 y OWASP ASVS nivel 1 | Requisitos y pruebas de seguridad de la aplicación. |
| Ley 81 de 2019 de Panamá (protección de datos personales) | Consentimiento, finalidad, minimización y seguridad de los datos académicos. |
| Guía de estilo de código del equipo (linters) y control de versiones con pull requests | Calidad interna del código y trazabilidad. |

## Métricas de calidad

| Métrica | Meta | Medición | Frecuencia | Responsable |
|---|---|---|---|---|
| Tiempo de respuesta (p95) | ≤ 2 s con 200 usuarios concurrentes | Prueba de carga (JMeter) | A21 y cada sprint | QA / Tester |
| Disponibilidad | ≥ 99 % durante el piloto | Monitor de disponibilidad | Diaria | Desarrollador 2 |
| Satisfacción de usuarios | > 80 % satisfechos o muy satisfechos | Encuesta posterior a la sesión | Piloto | Analista de Sistemas |
| Usabilidad (SUS) | ≥ 70 puntos | Cuestionario SUS | 1.3.1 y 1.7.2 | Diseñador UX/UI |
| Defectos críticos en producción | 0 | Registro de defectos | Piloto | QA / Tester |
| Defectos críticos o altos abiertos al cierre de sprint | 0 | Tablero del sprint | Cada sprint | QA / Tester |
| Cobertura de pruebas unitarias | ≥ 70 % de líneas | Reporte de CI | Cada pull request | Desarrollador 1 |
| Vulnerabilidades altas (OWASP) | 0 abiertas | Auditoría externa y escáner | A21 | QA / Tester |
| Accesibilidad | 0 errores WCAG AA en páginas clave | Herramienta automática + revisión manual | Cada sprint | Diseñador UX/UI |
| Entrega de correos | ≥ 98 % | Panel del servicio de correo | Semanal | Desarrollador 2 |
| Desempeño del cronograma y costo | SPI ≥ 0.95 y CPI ≥ 0.95 | Valor ganado | Quincenal | Gerente de Proyecto |

## Tipos de prueba

| Tipo | Objetivo | Cuándo / actividad | Responsable | Criterio de salida |
|---|---|---|---|---|
| Unitarias | Verificar funciones y componentes aislados. | Durante cada sprint (A12–A19) | Desarrolladores | Cobertura ≥ 70 %, 100 % aprobadas en CI. |
| Integración | Verificar la interacción entre módulos, base de datos, correo y autenticación institucional. | A21 | QA / Tester | 100 % de casos ejecutados, 0 críticos. |
| Sistema (rendimiento y seguridad) | Validar requisitos no funcionales. | A21 + auditoría externa | QA / Tester | p95 ≤ 2 s; 0 vulnerabilidades altas. |
| Aceptación (UAT) | Confirmar que se cumplen los criterios de aceptación de las historias. | A22 y cada Sprint Review | Coordinación FISC / Analista de Sistemas | Acta de aceptación firmada. |
| Usabilidad | Medir facilidad de uso con usuarios reales. | A09 (prototipo) y A22 | Diseñador UX/UI | SUS ≥ 70; éxito de tareas ≥ 80 %. |
| Regresión | Evitar que cambios rompan funciones existentes. | Final de cada sprint | QA / Tester | Suite de regresión aprobada. |

## Revisiones y auditorías

| Actividad de control | Frecuencia | Participantes | Producto |
|---|---|---|---|
| Revisión de código (pull request) | Cada cambio | D1, D2 | Pull request aprobado. |
| Sprint Review | Cada 2 semanas | Equipo + Coordinación FISC | Incremento aceptado o rechazado. |
| Retrospectiva | Cada 2 semanas | Equipo | Acciones de mejora. |
| Revisión de hitos (fase) | En H2, H3, H5, H6 | GP, patrocinador | Aprobación para continuar. |
| Auditoría de calidad del proceso | Al cierre del Sprint 2 y antes del UAT | GP y QA | Informe de cumplimiento del plan de calidad. |
| Auditoría de seguridad externa | Una vez (A21) | Proveedor externo | Informe de vulnerabilidades. |

## Criterios de aceptación de los entregables

| EDT | Entregable | Criterio de aceptación |
|---|---|---|
| 1.1.1 | Acta de constitución firmada. | Firmada por el patrocinador (FISC) y el Gerente de Proyecto; contiene todas las secciones de la plantilla del curso. |
| 1.1.2 | Plan de gestión aprobado (línea base de alcance, tiempo y costo). | Revisado por el patrocinador; líneas base coherentes entre sí (lista de verificación de coherencia sin observaciones). |
| 1.1.3 | Informes de avance quincenales y registro de cambios actualizado. | Un informe por quincena entregado al patrocinador; 100 % de solicitudes de cambio registradas y resueltas en el comité. |
| 1.2.1 | Informe de levantamiento y autorización de integración con credenciales institucionales. | Mínimo 60 encuestas y 8 entrevistas documentadas; autorización escrita de la DITIC o plan alterno aprobado. |
| 1.2.2 | SRS y Product Backlog priorizado y estimado. | Backlog con 15–25 historias INVEST, cada una con criterios de aceptación y vinculada a la EDT; acta de validación firmada. |
| 1.3.1 | Prototipo navegable en Figma y guía de estilo. | Prueba de usabilidad temprana con 5 usuarios; tasa de éxito de tareas ≥ 80 %; cumple contraste WCAG 2.1 AA. |
| 1.3.2 | Documento de arquitectura y modelo de datos. | Revisado por el Gerente de Proyecto y el Analista; cubre el 100 % de las historias Must del backlog. |
| 1.3.3 | Ambientes de desarrollo, pruebas (staging) y producción operativos. | Despliegue automático a staging desde la rama principal; HTTPS activo; respaldo diario configurado. |
| 1.4.1 | Incremento funcional de autenticación y perfiles. | Historias HU01–HU03 aceptadas en la Sprint Review conforme a la Definition of Done. |
| 1.4.2 | Incremento funcional de registro y validación de tutores. | Historias HU04–HU06 aceptadas en la Sprint Review conforme a la Definition of Done. |
| 1.5.1 | Incremento funcional de búsqueda. | Historias HU07–HU09 aceptadas; tiempo de respuesta de la búsqueda ≤ 2 s (p95). |
| 1.5.2 | Incremento funcional de agenda y reservas. | Historias HU10–HU13 aceptadas; cero reservas duplicadas en pruebas de concurrencia. |
| 1.5.3 | Incremento funcional de notificaciones. | Historias HU14–HU16 aceptadas; ≥ 98 % de correos entregados en staging. |
| 1.6.1 | Incremento funcional de evaluación. | Historias HU17–HU19 aceptadas conforme a la Definition of Done. |
| 1.6.2 | Incremento funcional de reportes. | Historias HU20–HU22 aceptadas; cifras del tablero cuadran con la base de datos en el 100 % de las pruebas. |
| 1.7.1 | Plan de pruebas, casos de prueba e informe de pruebas de sistema. | 100 % de casos ejecutados; 0 defectos críticos y 0 altos abiertos; p95 ≤ 2 s con 200 usuarios concurrentes. |
| 1.7.2 | Informe de UAT y acta de aceptación del sistema. | Acta de aceptación firmada por el patrocinador; SUS ≥ 70; criterios de aceptación de las historias Must cumplidos. |
| 1.8.1 | Manuales, videotutoriales y registro de asistencia a capacitaciones. | ≥ 90 % de coordinadores y tutores del piloto capacitados; evaluación de la capacitación ≥ 4/5. |
| 1.8.2 | Plataforma en producción e informe de operación del piloto. | Disponibilidad ≥ 99 % durante el piloto; ≥ 40 tutores validados y ≥ 100 estudiantes registrados. |
| 1.9.1 | Informe final del proyecto. | Incluye la medición de cada objetivo SMART y del desempeño de costo y tiempo (SPI y CPI). |
| 1.9.2 | Acta de cierre y registro de lecciones aprendidas. | Acta de cierre firmada por el patrocinador; documentación transferida a la DITIC. |
