# 14. Lista de verificación de coherencia

*Plataforma de tutorías entre estudiantes (TutorFISC) · Gerencia de Proyectos Informáticos (8469) · 1LS241*

Las verificaciones siguientes las ejecuta el generador del plan (generar_plan.py) cada vez que se regeneran los documentos; si alguna regla fallara, el documento no se generaría.

| # | Regla | Cumple | Evidencia |
|---|---|---|---|
| 1 | Todos los paquetes de la EDT tienen actividades en el cronograma | ✔ Sí | 21 paquetes, 21 con actividades. |
| 2 | Los códigos EDT de actividades, RACI, presupuesto y backlog existen en la EDT | ✔ Sí | Actividades, RACI, presupuesto, costos directos y 22 historias usan solo códigos de la EDT. |
| 3 | Los nombres de los paquetes son idénticos en todos los documentos | ✔ Sí | Todos los documentos toman el nombre del mismo diccionario PT del generador. |
| 4 | Cada fila de la RACI tiene exactamente una A | ✔ Sí | 21 filas verificadas. |
| 5 | Los R de la RACI coinciden con las asignaciones del cronograma | ✔ Sí | Cada rol asignado en el Gantt aparece como R o A/R. |
| 6 | El total del presupuesto coincide con el Acta | ✔ Sí | Acta y presupuesto: B/. 65,111.76 (mismo valor calculado). |
| 7 | La contingencia está entre 5 % y 10 % y se justifica con la matriz de riesgos | ✔ Sí | B/. 4,750.00 = EMV de los 12 riesgos = 8.3%. |
| 8 | Los costos de personal se calculan con las duraciones y asignaciones del Gantt | ✔ Sí | Σ actividades = B/. 51,810.76. |
| 9 | El cronograma respeta los 5 meses | ✔ Sí | 04-ene-2027 → 04-jun-2027 (107 días hábiles). |
| 10 | Las fechas de los hitos del Acta coinciden con el Gantt | ✔ Sí | Ambas tablas leen la fecha calculada por el CPM: H1 08-ene-2027, H2 02-feb-2027, H3 19-feb-2027, H4 05-abr-2027, H5 19-abr-2027, H6 07-may-2027, H7 26-may-2027, H8 04-jun-2027. |
| 11 | Los riesgos de alto nivel del Acta están en la matriz | ✔ Sí | R01, R03, R04, R05, R06. |
| 12 | Ningún rol está sobreasignado (> 100 %) en ningún día | ✔ Sí | GP 100%, AS 100%, UX 100%, D1 100%, D2 100%, QA 100% (carga máxima diaria). |
| 13 | El backlog tiene entre 15 y 25 historias y el Sprint 1 cabe en la capacidad | ✔ Sí | 22 historias; Sprint 1 usa 193 de 240 h. |
| 14 | Los sprints del backlog coinciden con las actividades del Gantt | ✔ Sí | Sprint 1: 1.4.x · Sprint 2: 1.5.1–1.5.2 · Sprint 3: 1.5.2–1.5.3 · Sprint 4: 1.6.x. |
| 15 | La matriz tiene entre 10 y 12 riesgos | ✔ Sí | 12 riesgos. |
| 16 | La EDT tiene al menos 8 paquetes de trabajo | ✔ Sí | 21 paquetes en 3 niveles. |
