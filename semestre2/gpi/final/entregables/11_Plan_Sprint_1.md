# 11. Plan del Sprint 1

*Plataforma de tutorías entre estudiantes (TutorFISC) · Gerencia de Proyectos Informáticos (8469) · 1LS241*

| Campo | Valor |
|---|---|
| Duración | 2 semanas (10 días hábiles): lunes 22 de febrero de 2027 al viernes 5 de marzo de 2027 |
| Actividades del cronograma | A12 (1.4.1) y A13 (1.4.2) |
| Meta del sprint | Los estudiantes pueden ingresar con su cuenta institucional y los estudiantes avanzados pueden postularse como tutores, ser validados automáticamente por materia y aprobados por la coordinación. |
| Historias comprometidas | HU01, HU02, HU03, HU04, HU05, HU06 (24 story points) |
| Product Owner | Analista de Sistemas (delegado de la Coordinación de la FISC) |
| Scrum Master | Gerente de Proyecto |
| Developers | Desarrollador 1, Desarrollador 2, Diseñador UX/UI, QA / Tester |

## Capacidad del equipo

Capacidad = días del sprint × dedicación al sprint (según el cronograma) × 6 horas productivas por día [SUPUESTO: factor de enfoque del 75 % sobre 8 h].

| Rol | Dedicación | Capacidad (h) | Horas planificadas | Uso |
|---|---|---|---|---|
| Desarrollador 1 | 100% | 60 | 54 | 90% |
| Desarrollador 2 | 100% | 60 | 52 | 87% |
| Diseñador UX/UI | 50% | 30 | 27 | 90% |
| QA / Tester | 100% | 60 | 46 | 77% |
| Analista de Sistemas | 50% | 30 | 14 | 47% |
| **Total** |  | **240** | **193** | **80%** |

## Historias seleccionadas y tareas

### HU01 (5 SP, Must) – Como estudiante quiero iniciar sesión con mi cuenta institucional @utp.ac.pa

| Tarea | Rol | Horas |
|---|---|---|
| Registrar la aplicación en el directorio institucional con la DITIC | Desarrollador 1 | 3 |
| Implementar el flujo OAuth 2.0 / OpenID Connect y la sesión segura | Desarrollador 1 | 12 |
| Restringir el acceso al dominio utp.ac.pa y manejar errores | Desarrollador 1 | 3 |
| Pruebas unitarias de autenticación | Desarrollador 1 | 4 |
| Diseñar y ejecutar casos de prueba de inicio de sesión | QA / Tester | 6 |

### HU02 (3 SP, Must) – Como estudiante de primer año quiero completar mi perfil con carrera, año y materias que curso

| Tarea | Rol | Horas |
|---|---|---|
| Ajustar el diseño de la pantalla de perfil | Diseñador UX/UI | 4 |
| Desarrollar la API y la pantalla de perfil del estudiante | Desarrollador 1 | 10 |
| Pruebas unitarias y funcionales del perfil | QA / Tester | 4 |

### HU03 (3 SP, Must) – Como coordinador quiero asignar los roles de estudiante, tutor y coordinador

| Tarea | Rol | Horas |
|---|---|---|
| Implementar el control de acceso por roles (RBAC) y la bitácora | Desarrollador 1 | 8 |
| Desarrollar la pantalla de administración de roles | Desarrollador 1 | 5 |
| Casos de prueba de permisos por rol | QA / Tester | 5 |

### HU04 (5 SP, Must) – Como estudiante avanzado quiero postularme como tutor indicando las materias que domino

| Tarea | Rol | Horas |
|---|---|---|
| Ajustar el diseño del formulario de postulación | Diseñador UX/UI | 5 |
| Desarrollar la API y el formulario de postulación | Desarrollador 2 | 14 |
| Pruebas unitarias de postulación | Desarrollador 2 | 3 |
| Prueba funcional de postulación | QA / Tester | 5 |

### HU05 (5 SP, Must) – Como coordinador quiero que el sistema valide automáticamente los requisitos académicos del postulante

| Tarea | Rol | Horas |
|---|---|---|
| Cargar el catálogo de materias de primer año | Desarrollador 2 | 4 |
| Implementar la regla de validación académica configurable | Desarrollador 2 | 10 |
| Importar el archivo de calificaciones autorizado | Desarrollador 2 | 6 |
| Pruebas de valores límite de la regla de validación | QA / Tester | 8 |

### HU06 (3 SP, Must) – Como coordinador quiero aprobar o rechazar postulaciones con observaciones

| Tarea | Rol | Horas |
|---|---|---|
| Diseñar la bandeja de aprobación | Diseñador UX/UI | 4 |
| Desarrollar la bandeja de aprobación y el registro de observaciones | Desarrollador 2 | 10 |
| Casos de prueba de aprobación y rechazo | QA / Tester | 4 |

### Tareas transversales del incremento

| Tarea | Rol | Horas |
|---|---|---|
| Implementar componentes base de la guía de estilo | Diseñador UX/UI | 10 |
| Implementar componentes base de interfaz (layout, formularios) | Desarrollador 1 | 4 |
| Preparar datos de prueba anonimizados | QA / Tester | 6 |
| Prueba de regresión del incremento en staging | QA / Tester | 8 |
| Revisión de código cruzada (pull requests) | Desarrollador 2 | 5 |
| Revisión de código cruzada (pull requests) | Desarrollador 1 | 5 |
| Verificación de accesibilidad básica (contraste, etiquetas) | Diseñador UX/UI | 4 |

### Trabajo del Product Owner

| Tarea | Rol | Horas |
|---|---|---|
| Refinar el backlog del Sprint 2 y aceptar historias | Analista de Sistemas | 14 |

## Definition of Done (DoD)

- El código está en el repositorio, en la rama principal, mediante un pull request revisado por otro desarrollador.
- Las pruebas unitarias pasan en la integración continua y la cobertura del código nuevo es ≥ 70 %.
- El incremento está desplegado en el ambiente de pruebas (staging).
- QA verificó todos los criterios de aceptación de la historia y no quedan defectos críticos ni altos abiertos.
- Cumple las pautas básicas de WCAG 2.1 AA (contraste, etiquetas, navegación con teclado).
- No expone datos personales y respeta el control de acceso por rol.
- La documentación (README y API) está actualizada.
- El Product Owner aceptó la historia en la Sprint Review.

## Ceremonias

| Ceremonia | Fecha / frecuencia | Duración | Participantes | Resultado |
|---|---|---|---|---|
| Sprint Planning | lunes 22 de febrero de 2027, 8:00 | 4 h | Equipo Scrum completo | Meta del sprint y Sprint Backlog. |
| Daily Scrum | Diario a las 8:30 (23-feb-2027 al 05-mar-2027) | 15 min | Developers (SM facilita) | Plan del día e impedimentos. |
| Refinamiento del backlog | martes 2 de marzo de 2027, 14:00 | 2 h | PO, Developers | Historias del Sprint 2 listas (Definition of Ready). |
| Sprint Review | viernes 5 de marzo de 2027, 9:00 | 2 h | Equipo + Coordinación FISC | Incremento inspeccionado; backlog actualizado. |
| Sprint Retrospective | viernes 5 de marzo de 2027, 11:30 | 1.5 h | Equipo Scrum | Dos o tres acciones de mejora para el Sprint 2. |

> Impedimento previsto: si la DITIC aún no autoriza la aplicación (riesgo R03), HU01 se desarrolla con el plan alterno (código de un solo uso enviado al correo @utp.ac.pa) sin cambiar la meta del sprint.
