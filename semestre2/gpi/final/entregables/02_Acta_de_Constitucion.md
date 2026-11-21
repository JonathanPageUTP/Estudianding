# 2. Acta de constitución del proyecto (Project Charter)

*Plataforma de tutorías entre estudiantes (TutorFISC) · Gerencia de Proyectos Informáticos (8469) · 1LS241*

| Campo | Contenido |
|---|---|
| Título del proyecto | Plataforma de tutorías entre estudiantes (TutorFISC) |
| Patrocinador | Decanato de la Facultad de Ingeniería de Sistemas Computacionales (FISC), Universidad Tecnológica de Panamá. |
| Gerente de Proyecto | Gerente de Proyecto del equipo simulado (con autoridad para asignar los recursos aprobados en esta Acta). |
| Fecha de inicio / fin | lunes 4 de enero de 2027 / viernes 4 de junio de 2027 (107 días hábiles, 5 meses) |
| Presupuesto total autorizado | B/. 65,111.76 |
| Enfoque | Híbrido: planificación predictiva (EDT, cronograma, costos) y construcción ágil con Scrum en 4 sprints de 2 semanas. |

## Justificación

La FISC necesita aumentar el apoyo académico a los estudiantes de primer año, etapa en la que se concentran la reprobación y la deserción. Existe una oferta potencial de estudiantes avanzados dispuestos a apoyar, pero no hay un mecanismo que conecte la oferta con la demanda, garantice la idoneidad del tutor y genere datos para la gestión. Una plataforma web de bajo costo, integrada con las credenciales institucionales, resuelve ese vacío sin requerir contratación de personal docente adicional.

## Objetivo general

Implementar, en un plazo de 5 meses y con un presupuesto de B/. 65,111.76, una plataforma web responsive que permita a los estudiantes de primer año de la FISC encontrar, reservar y evaluar tutorías impartidas por estudiantes avanzados validados por materia, y que proporcione a la coordinación indicadores para gestionar el programa.

## Objetivos específicos (SMART)

| ID | Objetivo | Indicador de medición |
|---|---|---|
| OE1 | Registrar y validar al menos 40 tutores que cubran como mínimo 12 materias de primer año de la FISC al finalizar el piloto (26-may-2027). | N.º de tutores aprobados y materias cubiertas (reporte HU20). |
| OE2 | Lograr que al menos 100 estudiantes de primer año se registren y que se realicen al menos 120 sesiones de tutoría durante las dos semanas del piloto. | Estudiantes registrados y sesiones con asistencia marcada. |
| OE3 | Reducir el tiempo para conseguir una tutoría de 7 días [SUPUESTO: línea base de la encuesta de 1.2.1] a menos de 48 horas entre la búsqueda y la sesión, medido durante el piloto. | Promedio de horas entre la reserva y la sesión. |
| OE4 | Alcanzar una satisfacción de los estudiantes mayor al 80 % y un puntaje SUS ≥ 70 en la encuesta aplicada al cierre del piloto. | Encuesta posterior a la sesión y cuestionario SUS. |
| OE5 | Entregar la plataforma en producción y cerrar el proyecto a más tardar el 04-jun-2027 con un desempeño de costo y tiempo CPI ≥ 0.95 y SPI ≥ 0.95. | Acta de cierre e informe de valor ganado. |

## Alcance de alto nivel

| Incluye | Excluye |
|---|---|
| • Registro y validación de tutores por materia (nota aprobada e índice mínimo).<br>• Registro de estudiantes con credenciales institucionales.<br>• Búsqueda de tutores.<br>• Agenda y reserva de sesiones.<br>• Notificaciones y recordatorios.<br>• Evaluación y calificación del tutor.<br>• Reportes para la coordinación.<br>• Pruebas, capacitación y piloto. | • Pagos a tutores o cobros a estudiantes.<br>• Videollamada integrada (se registra un enlace externo).<br>• Aplicación móvil nativa (la solución es web responsive).<br>• Integración en línea con el sistema de matrícula.<br>• Soporte y mantenimiento posteriores al cierre (se transfieren a la DITIC). |

## Entregables principales

- 1.1 Gestión del proyecto — Acta de constitución firmada; Plan de gestión aprobado (línea base de alcance, tiempo y costo); Informes de avance quincenales y registro de cambios actualizado.
- 1.2 Requisitos — Informe de levantamiento y autorización de integración con credenciales institucionales; SRS y Product Backlog priorizado y estimado.
- 1.3 Diseño UX/UI y arquitectura — Prototipo navegable en Figma y guía de estilo; Documento de arquitectura y modelo de datos; Ambientes de desarrollo, pruebas (staging) y producción operativos.
- 1.4 Módulo de usuarios y tutores — Incremento funcional de autenticación y perfiles; Incremento funcional de registro y validación de tutores.
- 1.5 Módulo de búsqueda, agenda y notificaciones — Incremento funcional de búsqueda; Incremento funcional de agenda y reservas; Incremento funcional de notificaciones.
- 1.6 Módulo de evaluación y reportes — Incremento funcional de evaluación; Incremento funcional de reportes.
- 1.7 Pruebas — Plan de pruebas, casos de prueba e informe de pruebas de sistema; Informe de UAT y acta de aceptación del sistema.
- 1.8 Capacitación y piloto — Manuales, videotutoriales y registro de asistencia a capacitaciones; Plataforma en producción e informe de operación del piloto.
- 1.9 Cierre del proyecto — Informe final del proyecto; Acta de cierre y registro de lecciones aprendidas.

## Interesados (matriz poder / interés)

| Interesado | Poder | Interés | Cuadrante | Estrategia |
|---|---|---|---|---|
| Decanato de la FISC (patrocinador) | Alto | Alto | Gestionar de cerca | Aprobaciones en hitos, informe quincenal. |
| Coordinación académica de la FISC | Alto | Alto | Gestionar de cerca | Product Owner delegado: asiste a cada Sprint Review. |
| DITIC de la UTP | Alto | Bajo | Mantener satisfecho | Consultar en decisiones de seguridad e integración. |
| Secretaría General (calificaciones) | Alto | Bajo | Mantener satisfecho | Solicitud formal de datos académicos. |
| Estudiantes de primer año | Bajo | Alto | Mantener informado | Encuestas, pruebas de usabilidad y difusión. |
| Estudiantes tutores | Bajo | Alto | Mantener informado | Grupo focal, capacitación y reconocimiento. |
| Docentes de primer año | Bajo | Bajo | Monitorear | Comunicados en momentos clave. |

## Equipo del proyecto

| Rol | Responsabilidades principales |
|---|---|
| Gerente de Proyecto | Planificar, dirigir y controlar el proyecto; Scrum Master; enlace con el patrocinador. |
| Analista de Sistemas | Levantar y especificar requisitos; Product Owner delegado por la coordinación; capacitación. |
| Diseñador UX/UI | Investigación de usuarios, prototipos, guía de estilo y pruebas de usabilidad. |
| Desarrollador 1 | Líder técnico: arquitectura, autenticación institucional, agenda/reservas y reportes. |
| Desarrollador 2 | Infraestructura y CI/CD, tutores, búsqueda, notificaciones y evaluación. |
| QA / Tester | Plan de pruebas, pruebas funcionales, de integración, rendimiento, seguridad y UAT. |

## Supuestos

- La FISC designa a un coordinador con disponibilidad de 4 h semanales para validar entregables.
- La DITIC autoriza la autenticación con las cuentas institucionales antes del Sprint 1 (22-feb-2027).
- Existen al menos 40 estudiantes avanzados interesados en ser tutores [SUPUESTO].
- La Secretaría General entrega un archivo autorizado de calificaciones para validar a los tutores.
- El primer semestre académico de 2027 está en curso durante el piloto (mayo de 2027).

## Restricciones

- Tiempo: 5 meses, del 04-ene-2027 al 04-jun-2027.
- Costo: presupuesto máximo de B/. 65,111.76 (incluye reservas).
- Alcance: sin pagos, sin videollamada integrada, sin aplicación nativa.
- Normativa: Ley 81 de 2019 de protección de datos personales y políticas de seguridad de la UTP.
- Tecnología: web responsive compatible con los navegadores actuales y con el correo institucional.

## Riesgos de alto nivel

| ID | Riesgo | Nivel (P×I) |
|---|---|---|
| R01 | Pocos estudiantes avanzados se registran como tutores voluntarios. | 20 (Alto) |
| R03 | Demora de la UTP (DITIC) en autorizar la integración con credenciales institucionales. | 15 (Alto) |
| R04 | Incumplimiento de la protección de datos personales (Ley 81 de 2019 de Panamá) o filtración de datos académicos. | 10 (Medio) |
| R05 | Crecimiento no controlado del alcance (por ejemplo, pedir pagos o videollamadas). | 12 (Medio) |
| R06 | Rotación o ausencia prolongada de un integrante del equipo. | 8 (Medio) |

## Hitos principales

| Hito | Descripción | Fecha |
|---|---|---|
| H1 | Acta de constitución aprobada | 08-ene-2027 |
| H2 | Plan de gestión y requisitos aprobados | 02-feb-2027 |
| H3 | Diseño y arquitectura aprobados | 19-feb-2027 |
| H4 | Producto mínimo viable (registro, búsqueda y agenda) | 05-abr-2027 |
| H5 | Desarrollo completo (fin del Sprint 4) | 19-abr-2027 |
| H6 | Sistema aceptado por el patrocinador | 07-may-2027 |
| H7 | Piloto concluido | 26-may-2027 |
| H8 | Cierre formal del proyecto | 04-jun-2027 |

## Presupuesto resumido

| Concepto | Monto |
|---|---|
| Personal (horas del cronograma × tarifa) | B/. 51,810.76 |
| Costos directos (infraestructura, licencias, equipos, capacitación y otros) | B/. 5,450.00 |
| Reserva de contingencia (8.3%) | B/. 4,750.00 |
| **Línea base de costos** | **B/. 62,010.76** |
| Reserva de gestión (5%) | B/. 3,101.00 |
| **Presupuesto total del proyecto** | **B/. 65,111.76** |

## Criterios de éxito

- Cumplimiento de los objetivos OE1 a OE5 medidos en el informe final.
- Plataforma en producción con 0 defectos críticos abiertos.
- Cierre a más tardar el 04-jun-2027 con una variación de costo no mayor al 5 % de la línea base.
- Acta de aceptación y acta de cierre firmadas por el patrocinador.

## Firmas de aprobación

| Rol | Nombre | Firma | Fecha |
|---|---|---|---|
| Patrocinador – Decanato de la FISC |  |  |  |
| Coordinación académica de la FISC |  |  |  |
| Gerente de Proyecto |  |  |  |
