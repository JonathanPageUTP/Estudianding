# 4. Lista de actividades

*Plataforma de tutorías entre estudiantes (TutorFISC) · Gerencia de Proyectos Informáticos (8469) · 1LS241*

Las actividades se derivan de los paquetes de trabajo de la EDT. Las duraciones se expresan en días hábiles (lunes a viernes, 8 horas, descontando los feriados nacionales) y se estimaron por juicio de expertos y analogía con proyectos académicos similares [SUPUESTO]. Todas las dependencias son Fin–Comienzo. Los hitos (H) tienen duración cero.

| ID | Código EDT | Actividad | Duración (días) | Predecesoras | Rol responsable | Asignación de roles |
|---|---|---|---|---|---|---|
| A01 | 1.1.1 | Elaborar el Acta de constitución y obtener su aprobación | 5 | — | Gerente de Proyecto | GP 100%, AS 25% |
| H1 | 1.1.1 | Hito: Acta de constitución aprobada | 0 | A01 | Gerente de Proyecto | — |
| A02 | 1.1.2 | Elaborar el plan de gestión del proyecto | 10 | A01 | Gerente de Proyecto | GP 60%, QA 25% |
| A03 | 1.1.3 | Dar seguimiento y control al proyecto (informes, valor ganado, control de cambios) | 78 | H2 | Gerente de Proyecto | GP 60% |
| A04 | 1.2.1 | Realizar entrevistas y encuestas a estudiantes, tutores y coordinación | 8 | A01 | Analista de Sistemas | AS 100%, UX 50% |
| A05 | 1.2.1 | Gestionar con la DITIC la autorización de credenciales institucionales | 15 | A01 | Gerente de Proyecto | GP 20% |
| A06 | 1.2.2 | Especificar los requisitos (SRS) y construir el Product Backlog | 7 | A04 | Analista de Sistemas | AS 100%, GP 20%, UX 25% |
| A07 | 1.2.2 | Validar los requisitos y el Product Backlog con el patrocinador | 2 | A06 | Analista de Sistemas | AS 100%, GP 40% |
| H2 | 1.2.2 | Hito: Plan de gestión y requisitos aprobados | 0 | A02, A07 | Gerente de Proyecto | — |
| A08 | 1.3.1 | Diseñar wireframes y flujos de navegación | 6 | A07 | Diseñador UX/UI | UX 100%, AS 25% |
| A09 | 1.3.1 | Elaborar el prototipo de alta fidelidad y validarlo con usuarios | 5 | A08 | Diseñador UX/UI | UX 100%, AS 25% |
| A10 | 1.3.2 | Definir la arquitectura y el modelo de datos | 6 | A07 | Desarrollador 1 | D1 100%, D2 50%, AS 25% |
| A11 | 1.3.3 | Configurar hosting, base de datos, dominio, repositorio y CI/CD | 5 | A10 | Desarrollador 2 | D2 100%, D1 50% |
| H3 | 1.3.3 | Hito: Diseño y arquitectura aprobados | 0 | A09, A11 | Gerente de Proyecto | — |
| A12 | 1.4.1 | Desarrollar el inicio de sesión con credenciales institucionales y el perfil del estudiante (Sprint 1) | 10 | H3, A05 | Desarrollador 1 | D1 100%, UX 25%, QA 50%, AS 25% |
| A13 | 1.4.2 | Desarrollar el registro y la validación de tutores por materia (Sprint 1) | 10 | H3 | Desarrollador 2 | D2 100%, UX 25%, QA 50%, AS 25% |
| A14 | 1.5.1 | Desarrollar la búsqueda y el perfil público de tutores (Sprint 2) | 10 | A12, A13 | Desarrollador 2 | D2 100%, UX 25%, QA 50%, AS 25% |
| A15 | 1.5.2 | Desarrollar la gestión de disponibilidad (agenda) del tutor (Sprint 2) | 10 | A12, A13 | Desarrollador 1 | D1 100%, UX 25%, QA 50%, AS 25% |
| A16 | 1.5.2 | Desarrollar la reserva, cancelación y reprogramación de sesiones (Sprint 3) | 10 | A14, A15 | Desarrollador 1 | D1 100%, UX 25%, QA 50%, AS 25% |
| A17 | 1.5.3 | Desarrollar las notificaciones y los recordatorios (Sprint 3) | 10 | A14, A15 | Desarrollador 2 | D2 100%, UX 25%, QA 50%, AS 25% |
| H4 | 1.5.3 | Hito: Producto mínimo viable (registro, búsqueda y agenda) | 0 | A16, A17 | Gerente de Proyecto | — |
| A18 | 1.6.1 | Desarrollar la evaluación y calificación del tutor (Sprint 4) | 10 | A16, A17 | Desarrollador 2 | D2 100%, UX 25%, QA 50%, AS 25% |
| A19 | 1.6.2 | Desarrollar los reportes para la coordinación (Sprint 4) | 10 | A16, A17 | Desarrollador 1 | D1 100%, UX 25%, QA 50%, AS 25% |
| H5 | 1.6.2 | Hito: Desarrollo completo (fin del Sprint 4) | 0 | A18, A19 | Gerente de Proyecto | — |
| A20 | 1.7.1 | Elaborar el plan y los casos de prueba | 8 | A07 | QA / Tester | QA 100%, AS 25% |
| A21 | 1.7.1 | Ejecutar pruebas de integración, sistema, rendimiento y seguridad | 8 | H5, A20 | QA / Tester | QA 100%, D1 50%, D2 50% |
| A22 | 1.7.2 | Ejecutar pruebas de aceptación (UAT) y de usabilidad | 6 | A21 | QA / Tester | QA 100%, AS 75%, UX 50%, D1 25%, D2 25% |
| H6 | 1.7.2 | Hito: Sistema aceptado por el patrocinador | 0 | A22 | Gerente de Proyecto | — |
| A23 | 1.8.1 | Elaborar manuales y material de capacitación | 5 | H5 | Analista de Sistemas | AS 50%, UX 50% |
| A24 | 1.8.1 | Capacitar a coordinadores, tutores y estudiantes | 3 | H6, A23 | Analista de Sistemas | AS 100%, UX 25%, GP 25% |
| A25 | 1.8.2 | Desplegar la plataforma en producción | 2 | H6 | Desarrollador 1 | D1 100%, D2 100%, QA 25% |
| A26 | 1.8.2 | Ejecutar el piloto con estudiantes de primer año | 10 | A24, A25 | Gerente de Proyecto | D1 50%, D2 50%, QA 50%, AS 50%, UX 25% |
| H7 | 1.8.2 | Hito: Piloto concluido | 0 | A26 | Gerente de Proyecto | — |
| A27 | 1.9.1 | Evaluar los resultados del piloto y elaborar el informe final | 4 | H7 | Gerente de Proyecto | GP 100%, AS 50%, QA 25% |
| A28 | 1.9.2 | Documentar lecciones aprendidas y formalizar el cierre | 3 | A27 | Gerente de Proyecto | GP 100%, AS 25%, UX 25%, D1 25%, D2 25%, QA 25% |
| H8 | 1.9.2 | Hito: Cierre formal del proyecto | 0 | A28 | Gerente de Proyecto | — |

> A03 es una actividad de nivel de esfuerzo: su duración (78 días) se extiende desde el hito H2 hasta el fin del piloto. Siglas de roles: GP Gerente de Proyecto, AS Analista de Sistemas, UX Diseñador UX/UI, D1 Desarrollador 1, D2 Desarrollador 2, QA QA / Tester.
