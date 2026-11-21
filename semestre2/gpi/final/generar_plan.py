# -*- coding: utf-8 -*-
"""
Generador del Plan de Gestión del proyecto "Plataforma de tutorías entre estudiantes".

Una sola fuente de datos (este archivo) produce TODOS los entregables, de modo que
códigos EDT, fechas, costos y riesgos son idénticos en todos los documentos.

Salidas (carpeta final/):
  entregables/NN_*.md                 un archivo por entregable (1 a 13 + verificación)
  Plan_Gestion_Tutorias.docx          documento integrador en Word (editable)
  plan.html                           documento integrador web (imprimible a PDF)
  cronograma/*.csv, *.xml             Gantt importable (Planificador del curso, GanttProject, ProjectLibre/MS Project)
  img/*.png                           Gantt, EDT en árbol y mapa de calor

Uso:  python generar_plan.py
"""
import csv
import datetime as dt
import html
import os
import re
from collections import OrderedDict, defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
D_ENT = os.path.join(BASE, "entregables")
D_CRON = os.path.join(BASE, "cronograma")
D_IMG = os.path.join(BASE, "img")
for d in (D_ENT, D_CRON, D_IMG):
    os.makedirs(d, exist_ok=True)

# =============================================================================
# 1. PARÁMETROS GENERALES
# =============================================================================
PROYECTO = "Plataforma de tutorías entre estudiantes (TutorFISC)"
NOMBRE_CORTO = "TutorFISC"
INICIO = dt.date(2027, 1, 4)
FERIADOS = OrderedDict([
    (dt.date(2027, 2, 8), "Lunes de Carnaval"),
    (dt.date(2027, 2, 9), "Martes de Carnaval"),
    (dt.date(2027, 3, 26), "Viernes Santo"),
])
HORAS_DIA = 8
HORAS_MES = 173.33          # 40 h × 52 semanas / 12 meses
CARGA_PATRONAL = 0.35       # [SUPUESTO] cuotas patronales y prestaciones
PCT_RESERVA_GESTION = 0.05  # [SUPUESTO] política de la organización

ROLES = OrderedDict([
    ("GP", ("Gerente de Proyecto", 3200)),
    ("AS", ("Analista de Sistemas", 2200)),
    ("UX", ("Diseñador UX/UI", 1900)),
    ("D1", ("Desarrollador 1", 2300)),
    ("D2", ("Desarrollador 2", 1900)),
    ("QA", ("QA / Tester", 1700)),
])
TARIFA = {k: round(s * (1 + CARGA_PATRONAL) / HORAS_MES, 2) for k, (_, s) in ROLES.items()}
RN = {k: v[0] for k, v in ROLES.items()}  # nombre del rol

def money(x):
    return "B/. {:,.2f}".format(x)

def fdate(d):
    meses = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
    return "{:02d}-{}-{}".format(d.day, meses[d.month - 1], d.year)

def fdate_largo(d):
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
             "septiembre", "octubre", "noviembre", "diciembre"]
    dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    return "{} {} de {} de {}".format(dias[d.weekday()], d.day, meses[d.month - 1], d.year)

# =============================================================================
# 2. EDT / WBS
# =============================================================================
# (código, nombre)  — niveles 1 y 2
EDT_N2 = OrderedDict([
    ("1", "Plataforma de tutorías entre estudiantes"),
    ("1.1", "Gestión del proyecto"),
    ("1.2", "Requisitos"),
    ("1.3", "Diseño UX/UI y arquitectura"),
    ("1.4", "Módulo de usuarios y tutores"),
    ("1.5", "Módulo de búsqueda, agenda y notificaciones"),
    ("1.6", "Módulo de evaluación y reportes"),
    ("1.7", "Pruebas"),
    ("1.8", "Capacitación y piloto"),
    ("1.9", "Cierre del proyecto"),
])
# Paquetes de trabajo (nivel 3): código -> (nombre, descripción, entregable, criterio de aceptación,
#                                          rol A, roles C, roles I)
PT = OrderedDict([
    ("1.1.1", ("Acta de constitución",
               "Definición del propósito, objetivos SMART, alcance de alto nivel, interesados, hitos y presupuesto resumido; obtención de la autorización formal del patrocinador.",
               "Acta de constitución firmada.",
               "Firmada por el patrocinador (FISC) y el Gerente de Proyecto; contiene todas las secciones de la plantilla del curso.",
               "PAT", ["AS"], ["UX", "D1", "D2", "QA"])),
    ("1.1.2", ("Plan de gestión del proyecto",
               "Elaboración de los planes subsidiarios: alcance (EDT), cronograma, costos, calidad, riesgos, recursos (RACI) y comunicaciones.",
               "Plan de gestión aprobado (línea base de alcance, tiempo y costo).",
               "Revisado por el patrocinador; líneas base coherentes entre sí (lista de verificación de coherencia sin observaciones).",
               "GP", ["AS", "PAT"], ["UX", "D1", "D2"])),
    ("1.1.3", ("Seguimiento y control",
               "Reuniones de seguimiento, informes de avance quincenales, gestión del valor ganado (SPI/CPI), control integrado de cambios y actualización del registro de riesgos.",
               "Informes de avance quincenales y registro de cambios actualizado.",
               "Un informe por quincena entregado al patrocinador; 100 % de solicitudes de cambio registradas y resueltas en el comité.",
               "GP", ["AS"], ["PAT", "UX", "D1", "D2", "QA"])),
    ("1.2.1", ("Levantamiento de requisitos",
               "Entrevistas y encuestas a estudiantes de primer año, tutores potenciales y coordinación; gestión de la autorización de credenciales institucionales con la DITIC.",
               "Informe de levantamiento y autorización de integración con credenciales institucionales.",
               "Mínimo 60 encuestas y 8 entrevistas documentadas; autorización escrita de la DITIC o plan alterno aprobado.",
               "AS", ["GP", "PAT"], ["D1", "D2", "QA"])),
    ("1.2.2", ("Especificación de requisitos y Product Backlog",
               "Redacción de la especificación de requisitos (SRS), historias de usuario con criterios de aceptación y priorización MoSCoW; validación con el patrocinador.",
               "SRS y Product Backlog priorizado y estimado.",
               "Backlog con 15–25 historias INVEST, cada una con criterios de aceptación y vinculada a la EDT; acta de validación firmada.",
               "GP", ["PAT", "D1", "QA"], ["D2"])),
    ("1.3.1", ("Prototipo UX/UI",
               "Wireframes, flujos de navegación, guía de estilo y prototipo navegable de alta fidelidad (web responsive), validado con usuarios.",
               "Prototipo navegable en Figma y guía de estilo.",
               "Prueba de usabilidad temprana con 5 usuarios; tasa de éxito de tareas ≥ 80 %; cumple contraste WCAG 2.1 AA.",
               "GP", ["D1", "PAT"], ["D2", "QA"])),
    ("1.3.2", ("Arquitectura y modelo de datos",
               "Definición de la arquitectura de la solución (web responsive, API REST, base de datos relacional), modelo entidad-relación y decisiones técnicas.",
               "Documento de arquitectura y modelo de datos.",
               "Revisado por el Gerente de Proyecto y el Analista; cubre el 100 % de las historias Must del backlog.",
               "D1", ["GP"], ["UX", "QA"])),
    ("1.3.3", ("Infraestructura y ambientes",
               "Configuración del hosting en la nube, base de datos gestionada, dominio, certificado TLS, repositorio, integración y despliegue continuos (CI/CD) y ambientes de desarrollo, pruebas y producción.",
               "Ambientes de desarrollo, pruebas (staging) y producción operativos.",
               "Despliegue automático a staging desde la rama principal; HTTPS activo; respaldo diario configurado.",
               "D1", ["GP"], ["QA"])),
    ("1.4.1", ("Registro de estudiantes con credenciales institucionales",
               "Inicio de sesión con la cuenta institucional @utp.ac.pa, perfil del estudiante y gestión de roles (Sprint 1).",
               "Incremento funcional de autenticación y perfiles.",
               "Historias HU01–HU03 aceptadas en la Sprint Review conforme a la Definition of Done.",
               "D1", ["GP"], ["PAT"])),
    ("1.4.2", ("Registro y validación de tutores por materia",
               "Postulación de tutores, validación automática de requisitos académicos por materia y aprobación por la coordinación (Sprint 1).",
               "Incremento funcional de registro y validación de tutores.",
               "Historias HU04–HU06 aceptadas en la Sprint Review conforme a la Definition of Done.",
               "D1", ["GP"], ["PAT"])),
    ("1.5.1", ("Búsqueda de tutores",
               "Búsqueda y filtrado de tutores por materia, horario y modalidad; perfil público del tutor (Sprint 2).",
               "Incremento funcional de búsqueda.",
               "Historias HU07–HU09 aceptadas; tiempo de respuesta de la búsqueda ≤ 2 s (p95).",
               "D1", ["GP"], ["PAT"])),
    ("1.5.2", ("Agenda y reserva de sesiones",
               "Disponibilidad del tutor (Sprint 2) y reserva, cancelación y reprogramación de sesiones sin traslapes (Sprint 3).",
               "Incremento funcional de agenda y reservas.",
               "Historias HU10–HU13 aceptadas; cero reservas duplicadas en pruebas de concurrencia.",
               "D1", ["GP"], ["PAT"])),
    ("1.5.3", ("Notificaciones y recordatorios",
               "Confirmaciones por correo, recordatorios automáticos 24 h y 1 h antes de la sesión y notificaciones dentro de la plataforma (Sprint 3).",
               "Incremento funcional de notificaciones.",
               "Historias HU14–HU16 aceptadas; ≥ 98 % de correos entregados en staging.",
               "D1", ["GP"], ["PAT"])),
    ("1.6.1", ("Evaluación y calificación del tutor",
               "Calificación de 1 a 5 y comentario posterior a la sesión, registro de asistencia y moderación de comentarios (Sprint 4).",
               "Incremento funcional de evaluación.",
               "Historias HU17–HU19 aceptadas conforme a la Definition of Done.",
               "D1", ["GP"], ["PAT"])),
    ("1.6.2", ("Reportes para la coordinación",
               "Tablero de indicadores para la coordinación y exportación de reportes por período (Sprint 4).",
               "Incremento funcional de reportes.",
               "Historias HU20–HU22 aceptadas; cifras del tablero cuadran con la base de datos en el 100 % de las pruebas.",
               "D1", ["GP", "PAT"], [])),
    ("1.7.1", ("Pruebas de integración y de sistema",
               "Plan y casos de prueba; pruebas de integración, sistema, rendimiento y seguridad (OWASP Top 10) y corrección de defectos.",
               "Plan de pruebas, casos de prueba e informe de pruebas de sistema.",
               "100 % de casos ejecutados; 0 defectos críticos y 0 altos abiertos; p95 ≤ 2 s con 200 usuarios concurrentes.",
               "QA", ["GP", "AS"], ["UX", "PAT"])),
    ("1.7.2", ("Pruebas de aceptación y usabilidad",
               "Pruebas de aceptación de usuario (UAT) con la coordinación, tutores y estudiantes, y prueba de usabilidad con el cuestionario SUS.",
               "Informe de UAT y acta de aceptación del sistema.",
               "Acta de aceptación firmada por el patrocinador; SUS ≥ 70; criterios de aceptación de las historias Must cumplidos.",
               "PAT", ["GP"], [])),
    ("1.8.1", ("Capacitación",
               "Manuales de usuario por perfil, videotutoriales breves y sesiones de capacitación para coordinadores, tutores y estudiantes.",
               "Manuales, videotutoriales y registro de asistencia a capacitaciones.",
               "≥ 90 % de coordinadores y tutores del piloto capacitados; evaluación de la capacitación ≥ 4/5.",
               "AS", ["GP", "QA"], ["D1", "D2", "PAT"])),
    ("1.8.2", ("Piloto y puesta en producción",
               "Despliegue en producción y piloto de dos semanas con estudiantes de primer año de la FISC, con soporte y monitoreo.",
               "Plataforma en producción e informe de operación del piloto.",
               "Disponibilidad ≥ 99 % durante el piloto; ≥ 40 tutores validados y ≥ 100 estudiantes registrados.",
               "GP", ["PAT"], [])),
    ("1.9.1", ("Evaluación de resultados e informe final",
               "Análisis de los indicadores del piloto frente a los objetivos SMART y elaboración del informe final.",
               "Informe final del proyecto.",
               "Incluye la medición de cada objetivo SMART y del desempeño de costo y tiempo (SPI y CPI).",
               "GP", ["PAT", "UX", "D1", "D2"], [])),
    ("1.9.2", ("Cierre administrativo y lecciones aprendidas",
               "Registro de lecciones aprendidas, transferencia a la DITIC, liberación de recursos y firma del acta de cierre.",
               "Acta de cierre y registro de lecciones aprendidas.",
               "Acta de cierre firmada por el patrocinador; documentación transferida a la DITIC.",
               "PAT", [], [])),
])

def nombre_pt(c):
    return PT[c][0] if c in PT else EDT_N2[c]

# =============================================================================
# 3. ACTIVIDADES (orden por EDT; predecesoras Fin-Comienzo)
# =============================================================================
# id, edt, nombre, duración (días hábiles), predecesoras, asignación {rol: fracción}, responsable, sprint
ACT = [
    ("A01", "1.1.1", "Elaborar el Acta de constitución y obtener su aprobación", 5, [], {"GP": 1, "AS": .25}, "GP", ""),
    ("H1", "1.1.1", "Hito: Acta de constitución aprobada", 0, ["A01"], {}, "GP", ""),
    ("A02", "1.1.2", "Elaborar el plan de gestión del proyecto", 10, ["A01"], {"GP": .6, "QA": .25}, "GP", ""),
    ("A03", "1.1.3", "Dar seguimiento y control al proyecto (informes, valor ganado, control de cambios)", None, ["H2"], {"GP": .6}, "GP", ""),
    ("A04", "1.2.1", "Realizar entrevistas y encuestas a estudiantes, tutores y coordinación", 8, ["A01"], {"AS": 1, "UX": .5}, "AS", ""),
    ("A05", "1.2.1", "Gestionar con la DITIC la autorización de credenciales institucionales", 15, ["A01"], {"GP": .2}, "GP", ""),
    ("A06", "1.2.2", "Especificar los requisitos (SRS) y construir el Product Backlog", 7, ["A04"], {"AS": 1, "GP": .2, "UX": .25}, "AS", ""),
    ("A07", "1.2.2", "Validar los requisitos y el Product Backlog con el patrocinador", 2, ["A06"], {"AS": 1, "GP": .4}, "AS", ""),
    ("H2", "1.2.2", "Hito: Plan de gestión y requisitos aprobados", 0, ["A02", "A07"], {}, "GP", ""),
    ("A08", "1.3.1", "Diseñar wireframes y flujos de navegación", 6, ["A07"], {"UX": 1, "AS": .25}, "UX", ""),
    ("A09", "1.3.1", "Elaborar el prototipo de alta fidelidad y validarlo con usuarios", 5, ["A08"], {"UX": 1, "AS": .25}, "UX", ""),
    ("A10", "1.3.2", "Definir la arquitectura y el modelo de datos", 6, ["A07"], {"D1": 1, "D2": .5, "AS": .25}, "D1", ""),
    ("A11", "1.3.3", "Configurar hosting, base de datos, dominio, repositorio y CI/CD", 5, ["A10"], {"D2": 1, "D1": .5}, "D2", ""),
    ("H3", "1.3.3", "Hito: Diseño y arquitectura aprobados", 0, ["A09", "A11"], {}, "GP", ""),
    ("A12", "1.4.1", "Desarrollar el inicio de sesión con credenciales institucionales y el perfil del estudiante", 10, ["H3", "A05"], {"D1": 1, "UX": .25, "QA": .5, "AS": .25}, "D1", "Sprint 1"),
    ("A13", "1.4.2", "Desarrollar el registro y la validación de tutores por materia", 10, ["H3"], {"D2": 1, "UX": .25, "QA": .5, "AS": .25}, "D2", "Sprint 1"),
    ("A14", "1.5.1", "Desarrollar la búsqueda y el perfil público de tutores", 10, ["A12", "A13"], {"D2": 1, "UX": .25, "QA": .5, "AS": .25}, "D2", "Sprint 2"),
    ("A15", "1.5.2", "Desarrollar la gestión de disponibilidad (agenda) del tutor", 10, ["A12", "A13"], {"D1": 1, "UX": .25, "QA": .5, "AS": .25}, "D1", "Sprint 2"),
    ("A16", "1.5.2", "Desarrollar la reserva, cancelación y reprogramación de sesiones", 10, ["A14", "A15"], {"D1": 1, "UX": .25, "QA": .5, "AS": .25}, "D1", "Sprint 3"),
    ("A17", "1.5.3", "Desarrollar las notificaciones y los recordatorios", 10, ["A14", "A15"], {"D2": 1, "UX": .25, "QA": .5, "AS": .25}, "D2", "Sprint 3"),
    ("H4", "1.5.3", "Hito: Producto mínimo viable (registro, búsqueda y agenda)", 0, ["A16", "A17"], {}, "GP", ""),
    ("A18", "1.6.1", "Desarrollar la evaluación y calificación del tutor", 10, ["A16", "A17"], {"D2": 1, "UX": .25, "QA": .5, "AS": .25}, "D2", "Sprint 4"),
    ("A19", "1.6.2", "Desarrollar los reportes para la coordinación", 10, ["A16", "A17"], {"D1": 1, "UX": .25, "QA": .5, "AS": .25}, "D1", "Sprint 4"),
    ("H5", "1.6.2", "Hito: Desarrollo completo (fin del Sprint 4)", 0, ["A18", "A19"], {}, "GP", ""),
    ("A20", "1.7.1", "Elaborar el plan y los casos de prueba", 8, ["A07"], {"QA": 1, "AS": .25}, "QA", ""),
    ("A21", "1.7.1", "Ejecutar pruebas de integración, sistema, rendimiento y seguridad", 8, ["H5", "A20"], {"QA": 1, "D1": .5, "D2": .5}, "QA", ""),
    ("A22", "1.7.2", "Ejecutar pruebas de aceptación (UAT) y de usabilidad", 6, ["A21"], {"QA": 1, "AS": .75, "UX": .5, "D1": .25, "D2": .25}, "QA", ""),
    ("H6", "1.7.2", "Hito: Sistema aceptado por el patrocinador", 0, ["A22"], {}, "GP", ""),
    ("A23", "1.8.1", "Elaborar manuales y material de capacitación", 5, ["H5"], {"AS": .5, "UX": .5}, "AS", ""),
    ("A24", "1.8.1", "Capacitar a coordinadores, tutores y estudiantes", 3, ["H6", "A23"], {"AS": 1, "UX": .25, "GP": .25}, "AS", ""),
    ("A25", "1.8.2", "Desplegar la plataforma en producción", 2, ["H6"], {"D1": 1, "D2": 1, "QA": .25}, "D1", ""),
    ("A26", "1.8.2", "Ejecutar el piloto con estudiantes de primer año", 10, ["A24", "A25"], {"D1": .5, "D2": .5, "QA": .5, "AS": .5, "UX": .25}, "GP", ""),
    ("H7", "1.8.2", "Hito: Piloto concluido", 0, ["A26"], {}, "GP", ""),
    ("A27", "1.9.1", "Evaluar los resultados del piloto y elaborar el informe final", 4, ["H7"], {"GP": 1, "AS": .5, "QA": .25}, "GP", ""),
    ("A28", "1.9.2", "Documentar lecciones aprendidas y formalizar el cierre", 3, ["A27"], {"GP": 1, "AS": .25, "UX": .25, "D1": .25, "D2": .25, "QA": .25}, "GP", ""),
    ("H8", "1.9.2", "Hito: Cierre formal del proyecto", 0, ["A28"], {}, "GP", ""),
]
A = OrderedDict()
for row in ACT:
    i, w, n, d, p, al, r, s = row
    A[i] = dict(id=i, edt=w, nombre=n, dur=d, pred=p, alloc=al, resp=r, sprint=s, hito=i.startswith("H"))

# --- calendario laboral -----------------------------------------------------
def dias_habiles(n_max=200):
    out, d = [], INICIO
    while len(out) < n_max:
        if d.weekday() < 5 and d not in FERIADOS:
            out.append(d)
        d += dt.timedelta(days=1)
    return out
DH = dias_habiles()

def cpm():
    orden, vistos = [], set()
    def visita(k):
        if k in vistos:
            return
        for p in A[k]["pred"]:
            visita(p)
        vistos.add(k)
        orden.append(k)
    for k in A:
        visita(k)
    for k in orden:
        a = A[k]
        a["ES"] = max([A[p]["EF"] for p in a["pred"]] or [0])
        a["EF"] = a["ES"] + (a["dur"] or 0)
    fin = max(a["EF"] for a in A.values())
    suc = defaultdict(list)
    for k, a in A.items():
        for p in a["pred"]:
            suc[p].append(k)
    for k in reversed(orden):
        a = A[k]
        a["LF"] = min([A[s]["LS"] for s in suc[k]] or [fin])
        a["LS"] = a["LF"] - (a["dur"] or 0)
        a["holgura"] = a["LS"] - a["ES"]
        a["critica"] = a["holgura"] == 0
    for a in A.values():
        if a["hito"]:
            a["inicio"] = a["fin"] = DH[a["EF"] - 1]
        else:
            a["inicio"], a["fin"] = DH[a["ES"]], DH[a["EF"] - 1]
    return fin

# A03 (seguimiento y control) es de nivel de esfuerzo: se extiende desde H2 hasta el fin del piloto.
A["A03"]["dur"] = 1
cpm()
A["A03"]["dur"] = A["A26"]["EF"] - A["H2"]["EF"]
DUR_TOTAL = cpm()
FIN = DH[DUR_TOTAL - 1]

# --- verificación de sobreasignación -----------------------------------------
CARGA = defaultdict(lambda: defaultdict(float))
for a in A.values():
    for r, f in a["alloc"].items():
        for d in range(a["ES"], a["EF"]):
            CARGA[r][d] += f
MAX_CARGA = {r: max(CARGA[r].values()) for r in ROLES}
assert all(v <= 1.0001 for v in MAX_CARGA.values()), MAX_CARGA

# --- horas y costo de personal por actividad ---------------------------------
for a in A.values():
    a["horas"] = {r: (a["dur"] or 0) * HORAS_DIA * f for r, f in a["alloc"].items()}
    a["costo"] = sum(h * TARIFA[r] for r, h in a["horas"].items())
HORAS_ROL = {r: sum(a["horas"].get(r, 0) for a in A.values()) for r in ROLES}
COSTO_ROL = {r: HORAS_ROL[r] * TARIFA[r] for r in ROLES}
PERSONAL = sum(COSTO_ROL.values())

# =============================================================================
# 4. COSTOS DIRECTOS (no personal)
# =============================================================================
# concepto, categoría, EDT, cantidad, unidad, costo unitario, justificación
DIRECTOS = [
    ("Alquiler de laptops para el equipo (6 equipos × 5 meses)", "Equipos", "1.1.3", 30, "equipo-mes", 35.00, "[SUPUESTO] arrendamiento operativo; el equipo no usa equipos personales."),
    ("Internet y telefonía del equipo", "Otros", "1.1.3", 5, "mes", 60.00, "Plan compartido de datos y telefonía."),
    ("Papelería e impresiones de gestión", "Otros", "1.1.3", 1, "global", 80.00, "Actas, informes impresos para firmas."),
    ("Curso en línea de accesibilidad (WCAG) y seguridad (OWASP) para el equipo", "Capacitación", "1.1.3", 6, "persona", 30.00, "Nivela al equipo en los estándares del plan de calidad."),
    ("Refrigerios para grupos focales y entrevistas", "Otros", "1.2.1", 1, "global", 150.00, "8 entrevistas y 2 grupos focales."),
    ("Figma Professional (1 editor)", "Licencias", "1.3.1", 5, "mes", 15.00, "Prototipo y guía de estilo."),
    ("Servidor en la nube – producción (2 vCPU, 4 GB)", "Infraestructura", "1.3.3", 4, "mes", 40.00, "Febrero a mayo; precio de referencia de proveedores IaaS."),
    ("Servidor en la nube – pruebas (staging)", "Infraestructura", "1.3.3", 4, "mes", 20.00, "Ambiente de pruebas y UAT."),
    ("Base de datos PostgreSQL gestionada con respaldo diario", "Infraestructura", "1.3.3", 4, "mes", 30.00, "Alta disponibilidad básica y respaldos."),
    ("Dominio y DNS (1 año)", "Infraestructura", "1.3.3", 1, "año", 35.00, "[SUPUESTO] dominio propio de respaldo si la UTP no asigna subdominio; TLS con Let's Encrypt (B/. 0)."),
    ("GitHub Team (repositorio y CI/CD)", "Licencias", "1.3.3", 30, "usuario-mes", 4.00, "6 usuarios × 5 meses."),
    ("Servicio de correo transaccional", "Infraestructura", "1.5.3", 4, "mes", 20.00, "Envío de confirmaciones y recordatorios (marzo a junio)."),
    ("Auditoría de seguridad externa (prueba de penetración básica)", "Otros", "1.7.1", 1, "servicio", 1500.00, "Transferencia del riesgo R04 (protección de datos)."),
    ("Dispositivos de prueba (smartphone Android y iPhone reacondicionado)", "Equipos", "1.7.1", 2, "unidad", 325.00, "Pruebas de diseño responsive en equipos reales."),
    ("Refrigerios para participantes de pruebas de usabilidad", "Otros", "1.7.2", 1, "global", 120.00, "Sesiones SUS con 10 usuarios."),
    ("Material impreso y refrigerios para capacitaciones (4 sesiones)", "Capacitación", "1.8.1", 4, "sesión", 75.00, "Coordinadores, tutores y estudiantes."),
    ("Campaña de difusión del piloto (afiches y redes sociales)", "Otros", "1.8.2", 1, "global", 250.00, "Atrae tutores y estudiantes (mitiga R01 y R08)."),
    ("Certificados de reconocimiento para tutores voluntarios", "Otros", "1.8.2", 50, "certificado", 2.00, "Incentivo no monetario (los pagos a tutores están fuera del alcance)."),
    ("Impresión del informe final y acto de cierre", "Otros", "1.9.2", 1, "global", 100.00, "Entrega formal al patrocinador."),
]
DIRECTOS = [dict(concepto=c, cat=k, edt=e, cant=q, unidad=u, unit=p, total=q * p, just=j) for c, k, e, q, u, p, j in DIRECTOS]
TOTAL_DIRECTOS = sum(x["total"] for x in DIRECTOS)

COSTO_PT = OrderedDict()
for c in PT:
    per = sum(a["costo"] for a in A.values() if a["edt"] == c)
    dire = sum(x["total"] for x in DIRECTOS if x["edt"] == c)
    COSTO_PT[c] = dict(personal=per, directos=dire, total=per + dire)
BASE_COSTO = sum(v["total"] for v in COSTO_PT.values())  # estimación de costos de las actividades

# =============================================================================
# 5. RIESGOS
# =============================================================================
PROB_PCT = {1: .10, 2: .30, 3: .50, 4: .70, 5: .90}
# id, descripción, causa, categoría, P, I, estrategia, respuesta, responsable, impacto en costo (B/.) si ocurre, EDT afectada
RIESGOS = [
    ("R01", "Pocos estudiantes avanzados se registran como tutores voluntarios.",
     "Falta de incentivos y carga académica de los estudiantes avanzados.", "Organizacional", 4, 5, "Mitigar",
     "Campaña de difusión con la FISC, certificados de reconocimiento y gestión ante la facultad de horas de servicio social [SUPUESTO]; meta intermedia de 25 tutores al inicio del piloto.",
     "GP", 1000, "1.8.2"),
    ("R02", "Ausentismo de estudiantes a las sesiones reservadas.",
     "Olvido, choques de horario o reservas sin compromiso.", "Operativo", 4, 3, "Mitigar",
     "Recordatorios 24 h y 1 h antes (HU15), cancelación con 12 h de anticipación (HU13) y registro de asistencia (HU18).",
     "AS", 400, "1.5.3"),
    ("R03", "Demora de la UTP (DITIC) en autorizar la integración con credenciales institucionales.",
     "Trámites internos de seguridad y aprobación de aplicaciones en el directorio institucional.", "Externo", 3, 5, "Mitigar",
     "Solicitud desde la semana 2 (A05) con holgura antes del Sprint 1; plan alterno: registro con verificación por correo @utp.ac.pa mediante código de un solo uso.",
     "GP", 1800, "1.4.1"),
    ("R04", "Incumplimiento de la protección de datos personales (Ley 81 de 2019 de Panamá) o filtración de datos académicos.",
     "Manejo de índices, notas y datos de contacto de estudiantes.", "Legal / Seguridad", 2, 5, "Transferir",
     "Auditoría de seguridad externa contratada (1.7.1), consentimiento informado, cifrado en tránsito y en reposo, mínimo privilegio y aviso de privacidad aprobado por Asesoría Legal.",
     "QA", 1500, "1.7.1"),
    ("R05", "Crecimiento no controlado del alcance (por ejemplo, pedir pagos o videollamadas).",
     "Expectativas de interesados no alineadas con el Acta.", "Gestión", 3, 4, "Evitar",
     "Alcance excluido explícito en el Acta; toda solicitud pasa por el control integrado de cambios y el Product Owner prioriza el backlog.",
     "GP", 1200, "1.1.3"),
    ("R06", "Rotación o ausencia prolongada de un integrante del equipo.",
     "Enfermedad, renuncia u ofertas laborales externas.", "Recursos", 2, 4, "Mitigar",
     "Programación en pares, revisión de código cruzada, documentación en el repositorio y matriz de respaldo entre roles.",
     "GP", 1500, "1.1.3"),
    ("R07", "Retraso en el aprovisionamiento de la infraestructura (hosting, base de datos o dominio).",
     "Trámites de compra o restricciones de la red institucional.", "Técnico", 2, 3, "Mitigar",
     "Infraestructura como código y proveedor alterno precalificado; inicio de 1.3.3 con holgura respecto al Sprint 1.",
     "D2", 400, "1.3.3"),
    ("R08", "Baja adopción de la plataforma por parte de estudiantes de primer año.",
     "Desconocimiento de la plataforma o preferencia por grupos de mensajería informales.", "Organizacional", 3, 4, "Mitigar",
     "Presentación en inducción de primer año, docentes como promotores y diseño validado con usuarios (1.3.1).",
     "AS", 600, "1.8.2"),
    ("R09", "Estimaciones de esfuerzo optimistas en los sprints de desarrollo.",
     "Poca experiencia previa del equipo con integraciones institucionales.", "Gestión", 3, 3, "Mitigar",
     "Estimación con Planning Poker, velocidad medida desde el Sprint 1 y reserva de capacidad del 15 % por sprint.",
     "D1", 900, "1.5.2"),
    ("R10", "Los correos de notificación llegan a la carpeta de spam o son bloqueados.",
     "Filtros del correo institucional y reputación del dominio emisor.", "Técnico", 3, 2, "Mitigar",
     "Configurar SPF, DKIM y DMARC; coordinar con la DITIC una lista blanca y ofrecer notificaciones dentro de la plataforma (HU16).",
     "D2", 300, "1.5.3"),
    ("R11", "Baja disponibilidad de usuarios para entrevistas, UAT y piloto por el calendario académico.",
     "Receso de verano, Carnaval, Semana Santa y período de exámenes.", "Externo", 3, 3, "Aceptar",
     "Aceptación activa: el cronograma ya descuenta los feriados; se agenda el UAT y el piloto en semanas de clase y se usa encuesta en línea.",
     "AS", 300, "1.7.2"),
    ("R12", "Los datos académicos (índice y notas) no están disponibles para validar a los tutores.",
     "La Secretaría General no expone un servicio de consulta de calificaciones.", "Externo", 3, 3, "Mitigar",
     "Validación con archivo de calificaciones autorizado (CSV) o constancia de créditos subida por el postulante y verificada por la coordinación.",
     "AS", 400, "1.4.2"),
]
RIESGOS = [dict(id=i, desc=d, causa=c, cat=k, p=p, i=im, nivel=p * im, estr=e, resp_txt=r, resp=rr, costo=co, edt=ed,
                emv=round(PROB_PCT[p] * co, 2))
           for i, d, c, k, p, im, e, r, rr, co, ed in RIESGOS]
def zona(n):
    return "Alto" if n >= 15 else ("Medio" if n >= 8 else "Bajo")
RIESGOS_ACTA = ["R01", "R03", "R04", "R05", "R06"]

EMV_TOTAL = sum(r["emv"] for r in RIESGOS)
CONTINGENCIA = round(EMV_TOTAL)
LINEA_BASE = BASE_COSTO + CONTINGENCIA
RESERVA_GESTION = round(LINEA_BASE * PCT_RESERVA_GESTION)
PRESUPUESTO_TOTAL = LINEA_BASE + RESERVA_GESTION
PCT_CONT = CONTINGENCIA / BASE_COSTO
assert 0.05 <= PCT_CONT <= 0.10, PCT_CONT

# =============================================================================
# 6. PRODUCT BACKLOG
# =============================================================================
# id, EDT, rol, quiero, para, criterios, MoSCoW, SP, sprint
HU = [
    ("HU01", "1.4.1", "estudiante", "iniciar sesión con mi cuenta institucional @utp.ac.pa", "no crear ni recordar otra contraseña",
     ["Solo se aceptan cuentas del dominio utp.ac.pa.", "Al primer ingreso se crea el perfil automáticamente.", "Una cuenta externa recibe un mensaje claro de rechazo."], "Must", 5, 1),
    ("HU02", "1.4.1", "estudiante de primer año", "completar mi perfil con carrera, año y materias que curso", "recibir sugerencias de tutores pertinentes",
     ["Campos obligatorios validados.", "Las materias se eligen del catálogo de primer año.", "El perfil puede editarse en cualquier momento."], "Must", 3, 1),
    ("HU03", "1.4.1", "coordinador", "asignar los roles de estudiante, tutor y coordinador", "controlar el acceso a cada función",
     ["Solo un coordinador puede cambiar roles.", "Cada cambio queda en la bitácora de auditoría.", "Las opciones del menú cambian según el rol."], "Must", 3, 1),
    ("HU04", "1.4.2", "estudiante avanzado", "postularme como tutor indicando las materias que domino", "ayudar a estudiantes de primer año",
     ["Puede elegir una o más materias del catálogo.", "Debe aceptar el código de conducta del tutor.", "La postulación queda en estado «Pendiente»."], "Must", 5, 1),
    ("HU05", "1.4.2", "coordinador", "que el sistema valide automáticamente los requisitos académicos del postulante", "garantizar tutores competentes",
     ["Requisito por materia: nota A o B en la materia e índice acumulado ≥ 2.0 [SUPUESTO].", "Si no cumple, la postulación se marca «No elegible» con el motivo.", "La regla es configurable por materia."], "Must", 5, 1),
    ("HU06", "1.4.2", "coordinador", "aprobar o rechazar postulaciones con observaciones", "mantener el control de calidad del programa",
     ["Bandeja con postulaciones pendientes y su resultado de validación.", "El rechazo exige una observación.", "El postulante ve el resultado en su perfil."], "Must", 3, 1),
    ("HU07", "1.5.1", "estudiante", "buscar tutores por materia, horario y modalidad", "encontrar apoyo de forma oportuna",
     ["Filtros combinables por materia, día, hora y modalidad (presencial o virtual).", "Solo aparecen tutores aprobados y con disponibilidad.", "Respuesta ≤ 2 s (p95)."], "Must", 5, 2),
    ("HU08", "1.5.1", "estudiante", "ver el perfil del tutor con materias, calificación promedio y comentarios", "elegir con confianza",
     ["Muestra el promedio y el número de evaluaciones.", "Muestra los 5 comentarios más recientes ya moderados.", "No expone datos personales sensibles."], "Should", 3, 2),
    ("HU09", "1.5.1", "estudiante", "ordenar los resultados por calificación o por disponibilidad más próxima", "decidir más rápido",
     ["Dos criterios de orden disponibles.", "El orden se mantiene al paginar."], "Could", 2, 2),
    ("HU10", "1.5.2", "tutor", "registrar mi disponibilidad semanal en bloques de horario con lugar o enlace", "recibir reservas solo cuando puedo atender",
     ["Bloques de 30 a 120 minutos.", "No se permiten bloques traslapados.", "Se indica aula o enlace externo de reunión (la videollamada no es parte de la plataforma)."], "Must", 8, 2),
    ("HU11", "1.5.2", "tutor", "bloquear fechas específicas (exámenes, feriados)", "evitar reservas en días en que no estaré",
     ["Las fechas bloqueadas desaparecen de la búsqueda.", "Si existen reservas en la fecha, el sistema advierte antes de bloquear."], "Should", 3, 2),
    ("HU12", "1.5.2", "estudiante", "reservar una sesión en un bloque disponible", "asegurar mi tutoría",
     ["Un bloque admite una sola reserva (sin duplicados en concurrencia).", "Máximo 3 reservas activas por estudiante.", "La reserva aparece en «Mis sesiones» de ambos usuarios."], "Must", 8, 3),
    ("HU13", "1.5.2", "estudiante o tutor", "cancelar o reprogramar una sesión con al menos 12 h de anticipación", "liberar el espacio para otro estudiante",
     ["Antes de 12 h la cancelación es libre; después se registra como tardía.", "El bloque liberado vuelve a estar disponible.", "La otra parte recibe aviso."], "Must", 5, 3),
    ("HU14", "1.5.3", "estudiante", "recibir una confirmación por correo al reservar", "tener constancia de la sesión",
     ["Correo enviado en menos de 1 minuto.", "Incluye fecha, hora, lugar o enlace y nombre del tutor.", "Incluye un archivo .ics para el calendario."], "Must", 3, 3),
    ("HU15", "1.5.3", "estudiante y tutor", "recibir recordatorios 24 h y 1 h antes de la sesión", "no olvidar la sesión y reducir el ausentismo",
     ["Dos recordatorios automáticos por sesión.", "No se envían si la sesión fue cancelada.", "Envíos registrados en la bitácora."], "Must", 5, 3),
    ("HU16", "1.5.3", "usuario", "ver notificaciones dentro de la plataforma y configurar mis preferencias", "no depender solo del correo",
     ["Contador de notificaciones no leídas.", "El usuario puede desactivar correos no obligatorios."], "Could", 3, 3),
    ("HU17", "1.6.1", "estudiante", "calificar al tutor de 1 a 5 y dejar un comentario al terminar la sesión", "retroalimentar la calidad de las tutorías",
     ["Solo se evalúan sesiones realizadas.", "Una evaluación por sesión, editable 48 h.", "El promedio del tutor se actualiza de inmediato."], "Must", 5, 4),
    ("HU18", "1.6.1", "tutor", "marcar la asistencia del estudiante", "registrar las ausencias y medir el ausentismo",
     ["Estados: asistió, no asistió, cancelada tarde.", "Disponible desde la hora de inicio hasta 24 h después."], "Should", 3, 4),
    ("HU19", "1.6.1", "coordinador", "moderar comentarios inapropiados", "mantener un ambiente de respeto",
     ["Ocultar un comentario exige un motivo.", "El autor es notificado."], "Should", 2, 4),
    ("HU20", "1.6.2", "coordinador", "consultar un tablero con sesiones por materia, asistencia y calificación promedio", "tomar decisiones sobre el programa de tutorías",
     ["Filtros por período y materia.", "Indicadores: sesiones, asistencia %, promedio de evaluación, tutores activos.", "Datos actualizados cada hora como máximo."], "Must", 8, 4),
    ("HU21", "1.6.2", "coordinador", "exportar los reportes a Excel y PDF por período", "informar a las autoridades de la FISC",
     ["Exporta exactamente las cifras filtradas en el tablero.", "Incluye fecha de generación y usuario."], "Should", 3, 4),
    ("HU22", "1.6.2", "coordinador", "identificar materias con alta demanda y pocos tutores", "convocar más tutores a tiempo",
     ["Lista de materias con relación reservas / tutores mayor a un umbral configurable.", "Se resalta en el tablero."], "Could", 3, 4),
]
HU = [dict(id=i, edt=e, rol=r, quiero=q, para=p, ca=ca, mos=m, sp=sp, sprint=s) for i, e, r, q, p, ca, m, sp, s in HU]
SP_SPRINT = defaultdict(int)
for h in HU:
    SP_SPRINT[h["sprint"]] += h["sp"]
SPRINT_ACT = {1: ["A12", "A13"], 2: ["A14", "A15"], 3: ["A16", "A17"], 4: ["A18", "A19"]}

# =============================================================================
# 7. SPRINT 1
# =============================================================================
S1_INI, S1_FIN = A["A12"]["inicio"], A["A12"]["fin"]
FOCO = 6  # horas productivas por día [SUPUESTO] (factor de enfoque 75 %)
S1_DIAS = A["A12"]["dur"]
S1_CAP = OrderedDict()
for r in ["D1", "D2", "UX", "QA", "AS"]:
    f = sum(A[k]["alloc"].get(r, 0) for k in SPRINT_ACT[1])
    S1_CAP[r] = dict(ded=f, horas=f * S1_DIAS * FOCO)
# historia, tarea, rol, horas
S1_TAREAS = [
    ("HU01", "Registrar la aplicación en el directorio institucional con la DITIC", "D1", 3),
    ("HU01", "Implementar el flujo OAuth 2.0 / OpenID Connect y la sesión segura", "D1", 12),
    ("HU01", "Restringir el acceso al dominio utp.ac.pa y manejar errores", "D1", 3),
    ("HU01", "Pruebas unitarias de autenticación", "D1", 4),
    ("HU01", "Diseñar y ejecutar casos de prueba de inicio de sesión", "QA", 6),
    ("HU02", "Ajustar el diseño de la pantalla de perfil", "UX", 4),
    ("HU02", "Desarrollar la API y la pantalla de perfil del estudiante", "D1", 10),
    ("HU02", "Pruebas unitarias y funcionales del perfil", "QA", 4),
    ("HU03", "Implementar el control de acceso por roles (RBAC) y la bitácora", "D1", 8),
    ("HU03", "Desarrollar la pantalla de administración de roles", "D1", 5),
    ("HU03", "Casos de prueba de permisos por rol", "QA", 5),
    ("HU04", "Ajustar el diseño del formulario de postulación", "UX", 5),
    ("HU04", "Desarrollar la API y el formulario de postulación", "D2", 14),
    ("HU04", "Pruebas unitarias de postulación", "D2", 3),
    ("HU04", "Prueba funcional de postulación", "QA", 5),
    ("HU05", "Cargar el catálogo de materias de primer año", "D2", 4),
    ("HU05", "Implementar la regla de validación académica configurable", "D2", 10),
    ("HU05", "Importar el archivo de calificaciones autorizado", "D2", 6),
    ("HU05", "Pruebas de valores límite de la regla de validación", "QA", 8),
    ("HU06", "Diseñar la bandeja de aprobación", "UX", 4),
    ("HU06", "Desarrollar la bandeja de aprobación y el registro de observaciones", "D2", 10),
    ("HU06", "Casos de prueba de aprobación y rechazo", "QA", 4),
    ("Transversal", "Implementar componentes base de la guía de estilo", "UX", 10),
    ("Transversal", "Implementar componentes base de interfaz (layout, formularios)", "D1", 4),
    ("Transversal", "Preparar datos de prueba anonimizados", "QA", 6),
    ("Transversal", "Prueba de regresión del incremento en staging", "QA", 8),
    ("Transversal", "Revisión de código cruzada (pull requests)", "D2", 5),
    ("Transversal", "Revisión de código cruzada (pull requests)", "D1", 5),
    ("Transversal", "Verificación de accesibilidad básica (contraste, etiquetas)", "UX", 4),
    ("PO", "Refinar el backlog del Sprint 2 y aceptar historias", "AS", 14),
]
S1_USO = defaultdict(float)
for _, _, r, h in S1_TAREAS:
    S1_USO[r] += h
for r, v in S1_USO.items():
    assert v <= S1_CAP[r]["horas"], (r, v, S1_CAP[r])

# =============================================================================
# 8. CONTENIDO (bloques) — cada sección = un entregable
# =============================================================================
# Tipos de bloque: ("h", nivel, texto) ("p", texto) ("ul", [..]) ("ol", [..])
#                  ("table", encabezados, filas, opciones) ("pre", texto) ("img", archivo, pie) ("note", texto)
SECCIONES = []
def seccion(num, slug, titulo):
    s = dict(num=num, slug=slug, titulo=titulo, bloques=[])
    SECCIONES.append(s)
    return s["bloques"]

def H(b, n, t): b.append(("h", n, t))
def P(b, t): b.append(("p", t))
def UL(b, xs): b.append(("ul", xs))
def OL(b, xs): b.append(("ol", xs))
def T(b, enc, filas, **op): b.append(("table", enc, filas, op))
def NOTE(b, t): b.append(("note", t))

HITOS = [a for a in A.values() if a["hito"]]
def ruta_txt():
    grupos = OrderedDict()
    for a in sorted((a for a in A.values() if a["critica"]), key=lambda a: (a["ES"], a["EF"])):
        grupos.setdefault((a["ES"], a["EF"]), []).append(a["id"])
    return " → ".join(("(" + " ∥ ".join(g) + ")") if len(g) > 1 else g[0] for g in grupos.values())
RUTA = [a for a in A.values() if a["critica"] and not a["hito"]]
OBJ = [
    ("OE1", "Registrar y validar al menos 40 tutores que cubran como mínimo 12 materias de primer año de la FISC al finalizar el piloto ({}).".format(fdate(A["H7"]["fin"])),
     "N.º de tutores aprobados y materias cubiertas (reporte HU20)."),
    ("OE2", "Lograr que al menos 100 estudiantes de primer año se registren y que se realicen al menos 120 sesiones de tutoría durante las dos semanas del piloto.",
     "Estudiantes registrados y sesiones con asistencia marcada."),
    ("OE3", "Reducir el tiempo para conseguir una tutoría de 7 días [SUPUESTO: línea base de la encuesta de 1.2.1] a menos de 48 horas entre la búsqueda y la sesión, medido durante el piloto.",
     "Promedio de horas entre la reserva y la sesión."),
    ("OE4", "Alcanzar una satisfacción de los estudiantes mayor al 80 % y un puntaje SUS ≥ 70 en la encuesta aplicada al cierre del piloto.",
     "Encuesta posterior a la sesión y cuestionario SUS."),
    ("OE5", "Entregar la plataforma en producción y cerrar el proyecto a más tardar el {} con un desempeño de costo y tiempo CPI ≥ 0.95 y SPI ≥ 0.95.".format(fdate(FIN)),
     "Acta de cierre e informe de valor ganado."),
]

# ---------- 1. Ficha de la idea ----------
b = seccion(1, "01_Ficha_de_la_Idea", "Ficha de la idea")
T(b, ["Campo", "Contenido"], [
    ["N.º de equipo", "______"],
    ["Integrantes", "1. ______________________\n2. ______________________\n3. ______________________\n4. ______________________\n5. ______________________"],
    ["Curso / Grupo", "Gerencia de Proyectos Informáticos (8469) · Grupo 1LS241 · II Semestre 2026"],
    ["Idea elegida", PROYECTO + ": aplicación web responsive en la que estudiantes avanzados de la FISC, validados por materia, ofrecen tutorías a estudiantes de primer año, quienes los buscan, reservan sesiones y los evalúan."],
    ["Cliente / patrocinador", "Facultad de Ingeniería de Sistemas Computacionales (FISC) de la UTP."],
])
H(b, 2, "Problema")
P(b, "Los estudiantes de primer año de la FISC no encuentran apoyo académico oportuno. Hoy la ayuda entre pares depende de contactos personales y de grupos informales de mensajería: no existe un registro de quiénes pueden dar tutoría en cada materia, ni una forma de verificar que dominan la materia, ni de agendar, recordar o evaluar las sesiones. Como consecuencia, el estudiante busca ayuda tarde —usualmente cerca de los parciales— y la coordinación no dispone de datos para identificar las materias con mayor necesidad de apoyo.")
H(b, 2, "Usuarios e interesados principales")
T(b, ["Interesado", "Rol en el proyecto", "Interés principal"], [
    ["Estudiantes de primer año", "Usuarios finales (reciben tutoría)", "Conseguir apoyo rápido y confiable."],
    ["Estudiantes avanzados (tutores)", "Usuarios finales (ofrecen tutoría)", "Organizar su tiempo y obtener reconocimiento."],
    ["Coordinación académica de la FISC", "Usuario administrador", "Controlar la calidad y obtener indicadores."],
    ["Decanato de la FISC", "Patrocinador", "Mejorar el rendimiento y la retención de primer año."],
    ["DITIC de la UTP [SUPUESTO: unidad de TI institucional]", "Proveedor de credenciales e infraestructura", "Seguridad e integración con los servicios institucionales."],
    ["Docentes de materias de primer año", "Promotores", "Que sus estudiantes refuercen contenidos."],
])
H(b, 2, "¿Por qué se eligió?")
UL(b, [
    "**Problema real y cercano:** el equipo lo vivió en su primer año, lo que facilita el levantamiento de requisitos.",
    "**Alcance acotado y medible:** cuatro capacidades centrales (registro y validación de tutores, búsqueda, agenda y evaluación) caben en 5 meses con un equipo de 6 roles.",
    "**Patrocinador accesible:** la FISC es a la vez cliente y usuario, lo que permite validar entregables con rapidez.",
    "**Permite aplicar todo el curso:** combina un ciclo predictivo (Acta, EDT, Gantt, presupuesto) con desarrollo ágil por sprints (backlog, Scrum).",
    "**Impacto social:** apoyo entre pares de bajo costo, sin pagos, que puede extenderse a otras facultades.",
])

# ---------- 2. Acta ----------
b = seccion(2, "02_Acta_de_Constitucion", "Acta de constitución del proyecto (Project Charter)")
T(b, ["Campo", "Contenido"], [
    ["Título del proyecto", PROYECTO],
    ["Patrocinador", "Decanato de la Facultad de Ingeniería de Sistemas Computacionales (FISC), Universidad Tecnológica de Panamá."],
    ["Gerente de Proyecto", "Gerente de Proyecto del equipo simulado (con autoridad para asignar los recursos aprobados en esta Acta)."],
    ["Fecha de inicio / fin", "{} / {} ({} días hábiles, 5 meses)".format(fdate_largo(INICIO), fdate_largo(FIN), DUR_TOTAL)],
    ["Presupuesto total autorizado", money(PRESUPUESTO_TOTAL)],
    ["Enfoque", "Híbrido: planificación predictiva (EDT, cronograma, costos) y construcción ágil con Scrum en 4 sprints de 2 semanas."],
])
H(b, 2, "Justificación")
P(b, "La FISC necesita aumentar el apoyo académico a los estudiantes de primer año, etapa en la que se concentran la reprobación y la deserción. Existe una oferta potencial de estudiantes avanzados dispuestos a apoyar, pero no hay un mecanismo que conecte la oferta con la demanda, garantice la idoneidad del tutor y genere datos para la gestión. Una plataforma web de bajo costo, integrada con las credenciales institucionales, resuelve ese vacío sin requerir contratación de personal docente adicional.")
H(b, 2, "Objetivo general")
P(b, "Implementar, en un plazo de 5 meses y con un presupuesto de {}, una plataforma web responsive que permita a los estudiantes de primer año de la FISC encontrar, reservar y evaluar tutorías impartidas por estudiantes avanzados validados por materia, y que proporcione a la coordinación indicadores para gestionar el programa.".format(money(PRESUPUESTO_TOTAL)))
H(b, 2, "Objetivos específicos (SMART)")
T(b, ["ID", "Objetivo", "Indicador de medición"], [[o[0], o[1], o[2]] for o in OBJ])
H(b, 2, "Alcance de alto nivel")
T(b, ["Incluye", "Excluye"], [[
    "• Registro y validación de tutores por materia (nota aprobada e índice mínimo).\n• Registro de estudiantes con credenciales institucionales.\n• Búsqueda de tutores.\n• Agenda y reserva de sesiones.\n• Notificaciones y recordatorios.\n• Evaluación y calificación del tutor.\n• Reportes para la coordinación.\n• Pruebas, capacitación y piloto.",
    "• Pagos a tutores o cobros a estudiantes.\n• Videollamada integrada (se registra un enlace externo).\n• Aplicación móvil nativa (la solución es web responsive).\n• Integración en línea con el sistema de matrícula.\n• Soporte y mantenimiento posteriores al cierre (se transfieren a la DITIC).",
]])
H(b, 2, "Entregables principales")
UL(b, ["{} {}".format(c, EDT_N2[c]) + " — " + "; ".join(PT[p][2].rstrip(".") for p in PT if p.startswith(c + ".")) + "." for c in EDT_N2 if c != "1"])
H(b, 2, "Interesados (matriz poder / interés)")
T(b, ["Interesado", "Poder", "Interés", "Cuadrante", "Estrategia"], [
    ["Decanato de la FISC (patrocinador)", "Alto", "Alto", "Gestionar de cerca", "Aprobaciones en hitos, informe quincenal."],
    ["Coordinación académica de la FISC", "Alto", "Alto", "Gestionar de cerca", "Product Owner delegado: asiste a cada Sprint Review."],
    ["DITIC de la UTP", "Alto", "Bajo", "Mantener satisfecho", "Consultar en decisiones de seguridad e integración."],
    ["Secretaría General (calificaciones)", "Alto", "Bajo", "Mantener satisfecho", "Solicitud formal de datos académicos."],
    ["Estudiantes de primer año", "Bajo", "Alto", "Mantener informado", "Encuestas, pruebas de usabilidad y difusión."],
    ["Estudiantes tutores", "Bajo", "Alto", "Mantener informado", "Grupo focal, capacitación y reconocimiento."],
    ["Docentes de primer año", "Bajo", "Bajo", "Monitorear", "Comunicados en momentos clave."],
])
H(b, 2, "Equipo del proyecto")
T(b, ["Rol", "Responsabilidades principales"], [
    [RN["GP"], "Planificar, dirigir y controlar el proyecto; Scrum Master; enlace con el patrocinador."],
    [RN["AS"], "Levantar y especificar requisitos; Product Owner delegado por la coordinación; capacitación."],
    [RN["UX"], "Investigación de usuarios, prototipos, guía de estilo y pruebas de usabilidad."],
    [RN["D1"], "Líder técnico: arquitectura, autenticación institucional, agenda/reservas y reportes."],
    [RN["D2"], "Infraestructura y CI/CD, tutores, búsqueda, notificaciones y evaluación."],
    [RN["QA"], "Plan de pruebas, pruebas funcionales, de integración, rendimiento, seguridad y UAT."],
])
H(b, 2, "Supuestos")
UL(b, [
    "La FISC designa a un coordinador con disponibilidad de 4 h semanales para validar entregables.",
    "La DITIC autoriza la autenticación con las cuentas institucionales antes del Sprint 1 ({}).".format(fdate(S1_INI)),
    "Existen al menos 40 estudiantes avanzados interesados en ser tutores [SUPUESTO].",
    "La Secretaría General entrega un archivo autorizado de calificaciones para validar a los tutores.",
    "El primer semestre académico de 2027 está en curso durante el piloto (mayo de 2027).",
])
H(b, 2, "Restricciones")
UL(b, [
    "Tiempo: 5 meses, del {} al {}.".format(fdate(INICIO), fdate(FIN)),
    "Costo: presupuesto máximo de {} (incluye reservas).".format(money(PRESUPUESTO_TOTAL)),
    "Alcance: sin pagos, sin videollamada integrada, sin aplicación nativa.",
    "Normativa: Ley 81 de 2019 de protección de datos personales y políticas de seguridad de la UTP.",
    "Tecnología: web responsive compatible con los navegadores actuales y con el correo institucional.",
])
H(b, 2, "Riesgos de alto nivel")
T(b, ["ID", "Riesgo", "Nivel (P×I)"], [[r["id"], r["desc"], "{} ({})".format(r["nivel"], zona(r["nivel"]))] for r in RIESGOS if r["id"] in RIESGOS_ACTA])
H(b, 2, "Hitos principales")
T(b, ["Hito", "Descripción", "Fecha"], [[h["id"], h["nombre"].replace("Hito: ", ""), fdate(h["fin"])] for h in HITOS])
H(b, 2, "Presupuesto resumido")
T(b, ["Concepto", "Monto"], [
    ["Personal (horas del cronograma × tarifa)", money(PERSONAL)],
    ["Costos directos (infraestructura, licencias, equipos, capacitación y otros)", money(TOTAL_DIRECTOS)],
    ["Reserva de contingencia ({:.1%})".format(PCT_CONT), money(CONTINGENCIA)],
    ["**Línea base de costos**", "**" + money(LINEA_BASE) + "**"],
    ["Reserva de gestión ({:.0%})".format(PCT_RESERVA_GESTION), money(RESERVA_GESTION)],
    ["**Presupuesto total del proyecto**", "**" + money(PRESUPUESTO_TOTAL) + "**"],
])
H(b, 2, "Criterios de éxito")
UL(b, [
    "Cumplimiento de los objetivos OE1 a OE5 medidos en el informe final.",
    "Plataforma en producción con 0 defectos críticos abiertos.",
    "Cierre a más tardar el {} con una variación de costo no mayor al 5 % de la línea base.".format(fdate(FIN)),
    "Acta de aceptación y acta de cierre firmadas por el patrocinador.",
])
H(b, 2, "Firmas de aprobación")
T(b, ["Rol", "Nombre", "Firma", "Fecha"], [
    ["Patrocinador – Decanato de la FISC", "", "", ""],
    ["Coordinación académica de la FISC", "", "", ""],
    ["Gerente de Proyecto", "", "", ""],
])

# ---------- 3. EDT ----------
b = seccion(3, "03_EDT_WBS", "Estructura de desglose del trabajo (EDT / WBS)")
P(b, "La EDT se organiza por entregables en tres niveles: el proyecto (nivel 1), {} entregables (nivel 2) y {} paquetes de trabajo (nivel 3). Cumple la regla del 100 %: cada elemento del alcance incluido en el Acta está representado en al menos un paquete y no existe trabajo fuera del alcance.".format(len(EDT_N2) - 1, len(PT)))
H(b, 2, "EDT codificada")
filas = [["1", "1", EDT_N2["1"], "Proyecto"]]
for c in EDT_N2:
    if c == "1":
        continue
    filas.append([c, "2", EDT_N2[c], "Entregable"])
    for p in PT:
        if p.startswith(c + "."):
            filas.append([p, "3", PT[p][0], "Paquete de trabajo"])
T(b, ["Código", "Nivel", "Nombre del elemento", "Tipo"], filas)
H(b, 2, "EDT en forma de árbol")
b.append(("img", "edt.png", "Figura 1. EDT del proyecto en forma de árbol."))
arbol = ["1 " + EDT_N2["1"]]
n2 = [c for c in EDT_N2 if c != "1"]
for i, c in enumerate(n2):
    ult = i == len(n2) - 1
    arbol.append(("└── " if ult else "├── ") + c + " " + EDT_N2[c])
    hijos = [p for p in PT if p.startswith(c + ".")]
    for j, p in enumerate(hijos):
        arbol.append(("    " if ult else "│   ") + ("└── " if j == len(hijos) - 1 else "├── ") + p + " " + PT[p][0])
b.append(("pre", "\n".join(arbol)))
H(b, 2, "Verificación de la regla del 100 %")
T(b, ["Elemento del alcance (Acta)", "Paquete(s) de la EDT"], [
    ["Registro y validación de tutores por materia", "1.4.2"],
    ["Registro de estudiantes con credenciales institucionales", "1.4.1 (y 1.2.1 para la autorización de la DITIC)"],
    ["Búsqueda de tutores", "1.5.1"],
    ["Agenda y reserva de sesiones", "1.5.2"],
    ["Notificaciones y recordatorios", "1.5.3"],
    ["Evaluación y calificación del tutor", "1.6.1"],
    ["Reportes para la coordinación", "1.6.2"],
    ["Pruebas", "1.7.1, 1.7.2 (las pruebas unitarias forman parte de cada módulo por la Definition of Done)"],
    ["Capacitación y piloto", "1.8.1, 1.8.2"],
    ["Gestión del proyecto y cierre", "1.1.1–1.1.3, 1.9.1, 1.9.2"],
])
H(b, 2, "Diccionario de la EDT")
T(b, ["Código", "Paquete", "Descripción", "Entregable", "Criterio de aceptación", "Responsable (A)"],
  [[c, v[0], v[1], v[2], v[3], "Patrocinador" if v[4] == "PAT" else RN[v[4]]] for c, v in PT.items()], small=True)

# ---------- 4. Actividades ----------
b = seccion(4, "04_Lista_de_Actividades", "Lista de actividades")
P(b, "Las actividades se derivan de los paquetes de trabajo de la EDT. Las duraciones se expresan en días hábiles (lunes a viernes, 8 horas, descontando los feriados nacionales) y se estimaron por juicio de expertos y analogía con proyectos académicos similares [SUPUESTO]. Todas las dependencias son Fin–Comienzo. Los hitos (H) tienen duración cero.")
T(b, ["ID", "Código EDT", "Actividad", "Duración (días)", "Predecesoras", "Rol responsable", "Asignación de roles"],
  [[a["id"], a["edt"], a["nombre"] + (" ({})".format(a["sprint"]) if a["sprint"] else ""), str(a["dur"]), ", ".join(a["pred"]) or "—", RN[a["resp"]],
    ", ".join("{} {:.0%}".format(r, f) for r, f in a["alloc"].items()) or "—"] for a in A.values()], small=True)
NOTE(b, "A03 es una actividad de nivel de esfuerzo: su duración ({} días) se extiende desde el hito H2 hasta el fin del piloto. Siglas de roles: GP Gerente de Proyecto, AS Analista de Sistemas, UX Diseñador UX/UI, D1 Desarrollador 1, D2 Desarrollador 2, QA QA / Tester.".format(A["A03"]["dur"]))

# ---------- 5. Cronograma ----------
b = seccion(5, "05_Cronograma_Gantt", "Cronograma y diagrama de Gantt")
P(b, "El cronograma se calculó con el método de la ruta crítica (CPM) a partir del {}. La duración total es de **{} días hábiles** y el proyecto finaliza el **{}**, dentro de los 5 meses acordados. Feriados descontados: {}.".format(
    fdate_largo(INICIO), DUR_TOTAL, fdate_largo(FIN), "; ".join("{} ({})".format(fdate(d), n) for d, n in FERIADOS.items())))
b.append(("img", "gantt.png", "Figura 2. Diagrama de Gantt (en rojo, la ruta crítica; rombos, los hitos)."))
H(b, 2, "Tabla del cronograma")
T(b, ["ID", "EDT", "Actividad", "Dur.", "Inicio", "Fin", "Holgura", "¿Crítica?"],
  [[a["id"], a["edt"], a["nombre"], str(a["dur"]), fdate(a["inicio"]), fdate(a["fin"]), str(a["holgura"]), "Sí" if a["critica"] else "No"] for a in A.values()],
  small=True, resaltar=[i for i, a in enumerate(A.values()) if a["critica"]])
H(b, 2, "Ruta crítica")
P(b, "La ruta crítica es: **{}**. Sus actividades tienen holgura cero; cualquier retraso en ellas retrasa la fecha de cierre. El símbolo ∥ indica actividades paralelas igualmente críticas: en cada sprint ambos desarrolladores están en la ruta crítica.".format(ruta_txt()))
mh = max((a for a in A.values() if not a["hito"]), key=lambda a: a["holgura"])
T(b, ["Concepto", "Resultado"], [
    ["Duración total del proyecto", "{} días hábiles ({} – {})".format(DUR_TOTAL, fdate(INICIO), fdate(FIN))],
    ["Actividades de la ruta crítica", ", ".join(a["id"] for a in RUTA)],
    ["Actividad con mayor holgura", "{} – {} ({} días)".format(mh["id"], mh["nombre"], mh["holgura"])],
    ["Fecha estimada de finalización", fdate_largo(FIN)],
])
P(b, "La holgura de {} días de A05 (autorización de la DITIC) funciona como amortiguador del riesgo R03: si la autorización se retrasa hasta {} días, el Sprint 1 no se afecta. Para acortar el proyecto se actuaría solo sobre la ruta crítica: ejecución rápida (fast tracking) solapando A22 (UAT) con A23–A24 o intensificación (crashing) agregando un desarrollador temporal en los sprints, con costo adicional.".format(A["A05"]["holgura"], A["A05"]["holgura"]))
H(b, 2, "Hitos")
T(b, ["Hito", "Descripción", "Fecha", "Predecesoras"], [[h["id"], h["nombre"].replace("Hito: ", ""), fdate(h["fin"]), ", ".join(h["pred"])] for h in HITOS])
H(b, 2, "Sprints de construcción")
T(b, ["Sprint", "Inicio", "Fin", "Actividades", "Paquetes EDT", "Story points"],
  [["Sprint {}".format(s), fdate(A[ks[0]]["inicio"]), fdate(A[ks[0]]["fin"]), ", ".join(ks), ", ".join(sorted(set(A[k]["edt"] for k in ks))), str(SP_SPRINT[s])] for s, ks in SPRINT_ACT.items()])
H(b, 2, "Archivos importables")
UL(b, [
    "**cronograma/Cronograma_MSProject.xml** – formato MS Project XML; se abre en ProjectLibre (Archivo → Abrir) y en GanttProject (Proyecto → Importar). Incluye EDT, dependencias, hitos, calendario con feriados, recursos y asignaciones. Es la opción recomendada.",
    "**cronograma/Cronograma_GanttProject.csv** – CSV con las columnas de GanttProject (ID, Name, Begin date, End date, Duration, Predecessors, Outline number, Resources).",
    "**cronograma/Cronograma_PlanificadorGantt.csv** – CSV para el Planificador Gantt del curso (Importar / exportar).",
    "**cronograma/Actividades.csv** – tabla completa del cronograma para Excel.",
])

# ---------- 6. RACI ----------
b = seccion(6, "06_Matriz_RACI", "Matriz RACI")
P(b, "La matriz cruza los paquetes de trabajo de la EDT con los roles del proyecto simulado y el patrocinador. R = responsable de ejecutar, A = aprueba y rinde cuentas (exactamente una por fila), C = consultado, I = informado. Los roles R coinciden con las asignaciones del cronograma; cuando quien rinde cuentas también ejecuta se indica «A/R».")
COLS_RACI = list(ROLES) + ["PAT"]
RACI = OrderedDict()
for c, v in PT.items():
    asign = set(r for a in A.values() if a["edt"] == c for r in a["alloc"])
    fila = {}
    for r in COLS_RACI:
        if r == v[4]:
            fila[r] = "A/R" if r in asign else "A"
        elif r in asign:
            fila[r] = "R"
        elif r in v[5]:
            fila[r] = "C"
        elif r in v[6]:
            fila[r] = "I"
        else:
            fila[r] = "I" if r == "PAT" else ""
    RACI[c] = fila
T(b, ["EDT", "Paquete de trabajo"] + list(ROLES) + ["Patrocinador"], [[c, PT[c][0]] + [RACI[c][r] for r in COLS_RACI] for c in PT], small=True)
NOTE(b, "GP Gerente de Proyecto · AS Analista de Sistemas · UX Diseñador UX/UI · D1 Desarrollador 1 · D2 Desarrollador 2 · QA QA / Tester · Patrocinador: Decanato y Coordinación de la FISC.")

# ---------- 7. Presupuesto ----------
b = seccion(7, "07_Presupuesto", "Presupuesto")
H(b, 2, "Supuestos de costo")
UL(b, [
    "Salarios mensuales de referencia del mercado panameño de TI para perfiles junior–semi senior en 2027 [SUPUESTO].",
    "Factor de carga patronal y prestaciones de {:.0%} [SUPUESTO]: cuota patronal de la CSS, seguro educativo, riesgos profesionales, décimo tercer mes, vacaciones y prima de antigüedad.".format(CARGA_PATRONAL),
    "Tarifa por hora = salario × {:.2f} ÷ {} horas/mes; jornada de {} h/día.".format(1 + CARGA_PATRONAL, HORAS_MES, HORAS_DIA),
    "Horas por rol = Σ (duración de la actividad × {} h × % de asignación del cronograma).".format(HORAS_DIA),
    "Los precios de servicios en la nube se toman como referencia de proveedores públicos, convertidos 1:1 (B/. = USD).",
])
H(b, 2, "Costo de personal por rol")
T(b, ["Rol", "Salario mensual", "Tarifa por hora (con carga)", "Horas asignadas", "Costo"],
  [[RN[r], money(ROLES[r][1]), money(TARIFA[r]), "{:,.0f}".format(HORAS_ROL[r]), money(COSTO_ROL[r])] for r in ROLES] +
  [["**Total personal**", "", "", "**{:,.0f}**".format(sum(HORAS_ROL.values())), "**" + money(PERSONAL) + "**"]])
H(b, 2, "Costos directos")
T(b, ["Concepto", "Categoría", "EDT", "Cant.", "Costo unitario", "Total"],
  [[x["concepto"], x["cat"], x["edt"], "{} {}".format(x["cant"], x["unidad"]), money(x["unit"]), money(x["total"])] for x in DIRECTOS] +
  [["**Total costos directos**", "", "", "", "", "**" + money(TOTAL_DIRECTOS) + "**"]], small=True)
cat = OrderedDict()
for x in DIRECTOS:
    cat[x["cat"]] = cat.get(x["cat"], 0) + x["total"]
T(b, ["Categoría", "Total"], [[k, money(v)] for k, v in cat.items()])
H(b, 2, "Presupuesto por paquete de la EDT")
filas = []
for c in EDT_N2:
    if c == "1":
        continue
    hijos = [p for p in PT if p.startswith(c + ".")]
    for p in hijos:
        v = COSTO_PT[p]
        filas.append([p, PT[p][0], money(v["personal"]), money(v["directos"]), money(v["total"])])
    filas.append(["**" + c + "**", "**Subtotal " + EDT_N2[c] + "**", "**" + money(sum(COSTO_PT[p]["personal"] for p in hijos)) + "**",
                  "**" + money(sum(COSTO_PT[p]["directos"] for p in hijos)) + "**", "**" + money(sum(COSTO_PT[p]["total"] for p in hijos)) + "**"])
filas.append(["", "**Estimación de costos de las actividades**", "**" + money(PERSONAL) + "**", "**" + money(TOTAL_DIRECTOS) + "**", "**" + money(BASE_COSTO) + "**"])
T(b, ["EDT", "Paquete de trabajo", "Personal", "Directos", "Total"], filas, small=True)
H(b, 2, "Reservas y total general")
P(b, "La **reserva de contingencia** cubre los riesgos identificados (conocidos-desconocidos) y se calculó como la suma del valor monetario esperado (EMV = probabilidad × impacto en costo) de los 12 riesgos de la matriz: {} ({:.1%} de la estimación, dentro del rango 5–10 %). La **reserva de gestión** ({:.0%} de la línea base) cubre riesgos no identificados; solo el patrocinador autoriza su uso.".format(money(CONTINGENCIA), PCT_CONT, PCT_RESERVA_GESTION))
T(b, ["Concepto", "Monto"], [
    ["Costo de personal", money(PERSONAL)],
    ["Costos directos", money(TOTAL_DIRECTOS)],
    ["Estimación de costos de las actividades", money(BASE_COSTO)],
    ["Reserva de contingencia (EMV de la matriz de riesgos, {:.1%})".format(PCT_CONT), money(CONTINGENCIA)],
    ["**Línea base de costos**", "**" + money(LINEA_BASE) + "**"],
    ["Reserva de gestión ({:.0%})".format(PCT_RESERVA_GESTION), money(RESERVA_GESTION)],
    ["**Presupuesto total del proyecto (= Acta)**", "**" + money(PRESUPUESTO_TOTAL) + "**"],
])

# ---------- 8. Riesgos ----------
b = seccion(8, "08_Matriz_de_Riesgos", "Matriz de riesgos")
P(b, "Escalas: probabilidad e impacto de 1 (muy bajo) a 5 (muy alto). Nivel = P × I. Zonas: Alto ≥ 15, Medio 8–14, Bajo ≤ 7. Los riesgos R01, R03, R04, R05 y R06 son los riesgos de alto nivel declarados en el Acta.")
H(b, 2, "Identificación y análisis")
T(b, ["ID", "Descripción", "Causa", "Categoría", "P", "I", "Nivel"],
  [[r["id"], r["desc"], r["causa"], r["cat"], str(r["p"]), str(r["i"]), "{} {}".format(r["nivel"], zona(r["nivel"]))] for r in RIESGOS], small=True)
H(b, 2, "Plan de respuesta")
T(b, ["ID", "Estrategia", "Acción de respuesta", "Responsable", "EDT"],
  [[r["id"], r["estr"], r["resp_txt"], RN[r["resp"]], r["edt"]] for r in RIESGOS], small=True)
H(b, 2, "Mapa de calor")
b.append(("img", "heatmap.png", "Figura 3. Mapa de calor probabilidad × impacto."))
grid = []
for p in range(5, 0, -1):
    fila = ["P = {}".format(p)]
    for i in range(1, 6):
        ids = [r["id"] for r in RIESGOS if r["p"] == p and r["i"] == i]
        fila.append(" ".join(ids) if ids else "·")
    grid.append(fila)
T(b, ["Probabilidad \\ Impacto", "I = 1", "I = 2", "I = 3", "I = 4", "I = 5"], grid)
H(b, 2, "Cálculo de la reserva de contingencia (EMV)")
T(b, ["ID", "Probabilidad", "Impacto en costo", "EMV"],
  [[r["id"], "{:.0%}".format(PROB_PCT[r["p"]]), money(r["costo"]), money(r["emv"])] for r in RIESGOS] +
  [["**Total**", "", "", "**" + money(EMV_TOTAL) + "**"]])
P(b, "Conversión de la escala de probabilidad: 1 = 10 %, 2 = 30 %, 3 = 50 %, 4 = 70 %, 5 = 90 % [SUPUESTO]. El total redondeado ({}) es la reserva de contingencia del presupuesto.".format(money(CONTINGENCIA)))

# ---------- 9. Calidad ----------
b = seccion(9, "09_Plan_de_Calidad", "Plan de gestión de la calidad")
H(b, 2, "Estándares aplicables")
T(b, ["Estándar / norma", "Aplicación en el proyecto"], [
    ["Guía del PMBOK® 7.ª ed. (PMI) y Guía de Scrum 2020", "Marco de gestión híbrido: planificación predictiva y construcción por sprints."],
    ["ISO/IEC 25010 (calidad del producto de software)", "Características evaluadas: adecuación funcional, eficiencia de desempeño, usabilidad, fiabilidad y seguridad."],
    ["ISO/IEC/IEEE 29119 (pruebas de software)", "Estructura del plan, casos e informes de prueba."],
    ["WCAG 2.1 nivel AA", "Accesibilidad de la interfaz web responsive."],
    ["OWASP Top 10 y OWASP ASVS nivel 1", "Requisitos y pruebas de seguridad de la aplicación."],
    ["Ley 81 de 2019 de Panamá (protección de datos personales)", "Consentimiento, finalidad, minimización y seguridad de los datos académicos."],
    ["Guía de estilo de código del equipo (linters) y control de versiones con pull requests", "Calidad interna del código y trazabilidad."],
])
H(b, 2, "Métricas de calidad")
T(b, ["Métrica", "Meta", "Medición", "Frecuencia", "Responsable"], [
    ["Tiempo de respuesta (p95)", "≤ 2 s con 200 usuarios concurrentes", "Prueba de carga (JMeter)", "A21 y cada sprint", RN["QA"]],
    ["Disponibilidad", "≥ 99 % durante el piloto", "Monitor de disponibilidad", "Diaria", RN["D2"]],
    ["Satisfacción de usuarios", "> 80 % satisfechos o muy satisfechos", "Encuesta posterior a la sesión", "Piloto", RN["AS"]],
    ["Usabilidad (SUS)", "≥ 70 puntos", "Cuestionario SUS", "1.3.1 y 1.7.2", RN["UX"]],
    ["Defectos críticos en producción", "0", "Registro de defectos", "Piloto", RN["QA"]],
    ["Defectos críticos o altos abiertos al cierre de sprint", "0", "Tablero del sprint", "Cada sprint", RN["QA"]],
    ["Cobertura de pruebas unitarias", "≥ 70 % de líneas", "Reporte de CI", "Cada pull request", RN["D1"]],
    ["Vulnerabilidades altas (OWASP)", "0 abiertas", "Auditoría externa y escáner", "A21", RN["QA"]],
    ["Accesibilidad", "0 errores WCAG AA en páginas clave", "Herramienta automática + revisión manual", "Cada sprint", RN["UX"]],
    ["Entrega de correos", "≥ 98 %", "Panel del servicio de correo", "Semanal", RN["D2"]],
    ["Desempeño del cronograma y costo", "SPI ≥ 0.95 y CPI ≥ 0.95", "Valor ganado", "Quincenal", RN["GP"]],
])
H(b, 2, "Tipos de prueba")
T(b, ["Tipo", "Objetivo", "Cuándo / actividad", "Responsable", "Criterio de salida"], [
    ["Unitarias", "Verificar funciones y componentes aislados.", "Durante cada sprint (A12–A19)", "Desarrolladores", "Cobertura ≥ 70 %, 100 % aprobadas en CI."],
    ["Integración", "Verificar la interacción entre módulos, base de datos, correo y autenticación institucional.", "A21", RN["QA"], "100 % de casos ejecutados, 0 críticos."],
    ["Sistema (rendimiento y seguridad)", "Validar requisitos no funcionales.", "A21 + auditoría externa", RN["QA"], "p95 ≤ 2 s; 0 vulnerabilidades altas."],
    ["Aceptación (UAT)", "Confirmar que se cumplen los criterios de aceptación de las historias.", "A22 y cada Sprint Review", "Coordinación FISC / " + RN["AS"], "Acta de aceptación firmada."],
    ["Usabilidad", "Medir facilidad de uso con usuarios reales.", "A09 (prototipo) y A22", RN["UX"], "SUS ≥ 70; éxito de tareas ≥ 80 %."],
    ["Regresión", "Evitar que cambios rompan funciones existentes.", "Final de cada sprint", RN["QA"], "Suite de regresión aprobada."],
])
H(b, 2, "Revisiones y auditorías")
T(b, ["Actividad de control", "Frecuencia", "Participantes", "Producto"], [
    ["Revisión de código (pull request)", "Cada cambio", "D1, D2", "Pull request aprobado."],
    ["Sprint Review", "Cada 2 semanas", "Equipo + Coordinación FISC", "Incremento aceptado o rechazado."],
    ["Retrospectiva", "Cada 2 semanas", "Equipo", "Acciones de mejora."],
    ["Revisión de hitos (fase)", "En H2, H3, H5, H6", "GP, patrocinador", "Aprobación para continuar."],
    ["Auditoría de calidad del proceso", "Al cierre del Sprint 2 y antes del UAT", "GP y QA", "Informe de cumplimiento del plan de calidad."],
    ["Auditoría de seguridad externa", "Una vez (A21)", "Proveedor externo", "Informe de vulnerabilidades."],
])
H(b, 2, "Criterios de aceptación de los entregables")
T(b, ["EDT", "Entregable", "Criterio de aceptación"], [[c, v[2], v[3]] for c, v in PT.items()], small=True)

# ---------- 10. Backlog ----------
b = seccion(10, "10_Product_Backlog", "Product Backlog")
P(b, "El backlog contiene {} historias de usuario con un total de {} story points (escala Fibonacci). La prioridad sigue el método MoSCoW (Must, Should, Could); las funciones excluidas del alcance (pagos, videollamada, app nativa) se registran como «Won't» y no forman parte del backlog. Cada historia se vincula a un paquete de la EDT y al sprint en que se planifica.".format(len(HU), sum(h["sp"] for h in HU)))
T(b, ["ID", "EDT", "Historia de usuario", "Criterios de aceptación", "MoSCoW", "SP", "Sprint"],
  [[h["id"], h["edt"], "Como {} quiero {} para {}.".format(h["rol"], h["quiero"], h["para"]), "\n".join("• " + c for c in h["ca"]), h["mos"], str(h["sp"]), str(h["sprint"])] for h in HU], small=True)
mos = defaultdict(int)
for h in HU:
    mos[h["mos"]] += h["sp"]
T(b, ["Resumen", "Valor"], [
    ["Story points por sprint", " · ".join("S{}: {}".format(s, SP_SPRINT[s]) for s in sorted(SP_SPRINT))],
    ["Story points por prioridad", " · ".join("{}: {}".format(k, mos[k]) for k in ["Must", "Should", "Could"])],
    ["Velocidad planificada", "≈ {:.0f} SP por sprint [SUPUESTO, se ajusta con la velocidad real del Sprint 1]".format(sum(SP_SPRINT.values()) / len(SP_SPRINT))],
])

# ---------- 11. Sprint 1 ----------
b = seccion(11, "11_Plan_Sprint_1", "Plan del Sprint 1")
hs1 = [h for h in HU if h["sprint"] == 1]
T(b, ["Campo", "Valor"], [
    ["Duración", "2 semanas ({} días hábiles): {} al {}".format(S1_DIAS, fdate_largo(S1_INI), fdate_largo(S1_FIN))],
    ["Actividades del cronograma", "A12 (1.4.1) y A13 (1.4.2)"],
    ["Meta del sprint", "Los estudiantes pueden ingresar con su cuenta institucional y los estudiantes avanzados pueden postularse como tutores, ser validados automáticamente por materia y aprobados por la coordinación."],
    ["Historias comprometidas", "{} ({} story points)".format(", ".join(h["id"] for h in hs1), SP_SPRINT[1])],
    ["Product Owner", RN["AS"] + " (delegado de la Coordinación de la FISC)"],
    ["Scrum Master", RN["GP"]],
    ["Developers", ", ".join(RN[r] for r in ["D1", "D2", "UX", "QA"])],
])
H(b, 2, "Capacidad del equipo")
P(b, "Capacidad = días del sprint × dedicación al sprint (según el cronograma) × {} horas productivas por día [SUPUESTO: factor de enfoque del 75 % sobre 8 h].".format(FOCO))
T(b, ["Rol", "Dedicación", "Capacidad (h)", "Horas planificadas", "Uso"],
  [[RN[r], "{:.0%}".format(v["ded"]), "{:.0f}".format(v["horas"]), "{:.0f}".format(S1_USO[r]), "{:.0%}".format(S1_USO[r] / v["horas"])] for r, v in S1_CAP.items()] +
  [["**Total**", "", "**{:.0f}**".format(sum(v["horas"] for v in S1_CAP.values())), "**{:.0f}**".format(sum(S1_USO.values())), "**{:.0%}**".format(sum(S1_USO.values()) / sum(v["horas"] for v in S1_CAP.values()))]])
H(b, 2, "Historias seleccionadas y tareas")
for h in hs1 + [dict(id="Transversal", rol=None), dict(id="PO", rol=None)]:
    tareas = [t for t in S1_TAREAS if t[0] == h["id"]]
    if h["rol"]:
        H(b, 3, "{} ({} SP, {}) – Como {} quiero {}".format(h["id"], h["sp"], h["mos"], h["rol"], h["quiero"]))
    elif h["id"] == "Transversal":
        H(b, 3, "Tareas transversales del incremento")
    else:
        H(b, 3, "Trabajo del Product Owner")
    T(b, ["Tarea", "Rol", "Horas"], [[t[1], RN[t[2]], str(t[3])] for t in tareas])
H(b, 2, "Definition of Done (DoD)")
UL(b, [
    "El código está en el repositorio, en la rama principal, mediante un pull request revisado por otro desarrollador.",
    "Las pruebas unitarias pasan en la integración continua y la cobertura del código nuevo es ≥ 70 %.",
    "El incremento está desplegado en el ambiente de pruebas (staging).",
    "QA verificó todos los criterios de aceptación de la historia y no quedan defectos críticos ni altos abiertos.",
    "Cumple las pautas básicas de WCAG 2.1 AA (contraste, etiquetas, navegación con teclado).",
    "No expone datos personales y respeta el control de acceso por rol.",
    "La documentación (README y API) está actualizada.",
    "El Product Owner aceptó la historia en la Sprint Review.",
])
H(b, 2, "Ceremonias")
dias_s1 = DH[A["A12"]["ES"]:A["A12"]["EF"]]
T(b, ["Ceremonia", "Fecha / frecuencia", "Duración", "Participantes", "Resultado"], [
    ["Sprint Planning", fdate_largo(dias_s1[0]) + ", 8:00", "4 h", "Equipo Scrum completo", "Meta del sprint y Sprint Backlog."],
    ["Daily Scrum", "Diario a las 8:30 ({} al {})".format(fdate(dias_s1[1]), fdate(dias_s1[-1])), "15 min", "Developers (SM facilita)", "Plan del día e impedimentos."],
    ["Refinamiento del backlog", fdate_largo(dias_s1[6]) + ", 14:00", "2 h", "PO, Developers", "Historias del Sprint 2 listas (Definition of Ready)."],
    ["Sprint Review", fdate_largo(dias_s1[-1]) + ", 9:00", "2 h", "Equipo + Coordinación FISC", "Incremento inspeccionado; backlog actualizado."],
    ["Sprint Retrospective", fdate_largo(dias_s1[-1]) + ", 11:30", "1.5 h", "Equipo Scrum", "Dos o tres acciones de mejora para el Sprint 2."],
])
NOTE(b, "Impedimento previsto: si la DITIC aún no autoriza la aplicación (riesgo R03), HU01 se desarrolla con el plan alterno (código de un solo uso enviado al correo @utp.ac.pa) sin cambiar la meta del sprint.")

# ---------- 12/13 Guion ----------
b = seccion(13, "13_Guion_de_Exposicion", "Guion de exposición")
P(b, "Duración total: 18 minutos de exposición + 2 minutos de preguntas. Cada presentador cuenta con unos 3.5 minutos y entrega la palabra al siguiente con una frase de enlace.")
GUION = [
    ("Presentador 1", "0:00 – 3:30", "Introducción, idea y Acta",
     ["Saludo, equipo y nombre del proyecto.", "Problema: primer año sin apoyo académico oportuno.", "Objetivo general y los 5 objetivos SMART.",
      "Alcance: qué incluye y qué excluye (pagos, videollamada, app nativa).", "Patrocinador, interesados en la matriz poder/interés."],
     "«Con el alcance claro, veamos cómo lo dividimos en trabajo concreto.»"),
    ("Presentador 2", "3:30 – 7:00", "EDT y actividades",
     ["EDT en árbol: 9 entregables y 21 paquetes; regla del 100 %.", "Ejemplo del diccionario: 1.4.2 Registro y validación de tutores.",
      "Lista de 28 actividades y 8 hitos; enfoque híbrido con 4 sprints.", "Cómo se estimaron las duraciones."],
     "«Estas actividades, ordenadas en el tiempo, forman nuestro cronograma.»"),
    ("Presentador 3", "7:00 – 10:30", "Cronograma, ruta crítica y RACI",
     ["Gantt del {} al {} ({} días hábiles, feriados descontados).".format(fdate(INICIO), fdate(FIN), DUR_TOTAL),
      "Ruta crítica y por qué los sprints son críticos.", "Holgura de A05 como amortiguador del riesgo de credenciales.",
      "Matriz RACI: una sola A por paquete."],
     "«Saber quién hace qué nos permite calcular cuánto cuesta.»"),
    ("Presentador 4", "10:30 – 14:00", "Presupuesto y riesgos",
     ["Salarios, tarifa por hora y horas por rol tomadas del Gantt.", "Costos directos y subtotal por paquete de la EDT.",
      "Total: {} (contingencia {} y reserva de gestión {}).".format(money(PRESUPUESTO_TOTAL), money(CONTINGENCIA), money(RESERVA_GESTION)),
      "Matriz de riesgos: mapa de calor y los 3 riesgos más altos (R01, R03, R02/R05).", "La contingencia sale del EMV de los riesgos."],
     "«Para que el presupuesto valga la pena, el producto debe tener calidad.»"),
    ("Presentador 5", "14:00 – 18:00", "Calidad, backlog, Sprint 1 y conclusiones",
     ["Métricas clave: p95 ≤ 2 s, disponibilidad ≥ 99 %, satisfacción > 80 %, 0 defectos críticos.",
      "Backlog: 22 historias, {} SP, MoSCoW y vínculo con la EDT.".format(sum(h["sp"] for h in HU)),
      "Sprint 1: meta, capacidad, Definition of Done y ceremonias.", "Lista de verificación de coherencia.", "Conclusiones y cierre; abrir preguntas."],
     "«Muchas gracias; quedamos atentos a sus preguntas.»"),
]
for quien, tiempo, tema, puntos, enlace in GUION:
    H(b, 3, "{} ({}) – {}".format(quien, tiempo, tema))
    UL(b, puntos + ["Transición: " + enlace])
H(b, 2, "Recomendaciones")
UL(b, ["Una idea por diapositiva y cifras redondeadas en voz alta.", "Ensayar dos veces con cronómetro.",
       "Llevar a mano el Gantt y el presupuesto para responder preguntas.", "Todos deben poder explicar la ruta crítica y el total del presupuesto."])

# ---------- Verificación de coherencia (se calcula, no se escribe a mano) ----------
CHECKS = []
def chk(regla, ok, evidencia):
    CHECKS.append((regla, ok, evidencia))
codigos_act = set(a["edt"] for a in A.values())
chk("Todos los paquetes de la EDT tienen actividades en el cronograma", set(PT) == codigos_act,
    "{} paquetes, {} con actividades.".format(len(PT), len(codigos_act & set(PT))))
chk("Los códigos EDT de actividades, RACI, presupuesto y backlog existen en la EDT",
    codigos_act <= set(PT) and set(RACI) == set(PT) and set(COSTO_PT) == set(PT) and all(h["edt"] in PT for h in HU) and all(x["edt"] in PT for x in DIRECTOS),
    "Actividades, RACI, presupuesto, costos directos y {} historias usan solo códigos de la EDT.".format(len(HU)))
chk("Los nombres de los paquetes son idénticos en todos los documentos", True,
    "Todos los documentos toman el nombre del mismo diccionario PT del generador.")
chk("Cada fila de la RACI tiene exactamente una A", all(sum("A" in v for v in f.values()) == 1 for f in RACI.values()),
    "{} filas verificadas.".format(len(RACI)))
chk("Los R de la RACI coinciden con las asignaciones del cronograma",
    all(("R" in RACI[a["edt"]][r]) for a in A.values() for r in a["alloc"]), "Cada rol asignado en el Gantt aparece como R o A/R.")
chk("El total del presupuesto coincide con el Acta", True, "Acta y presupuesto: {} (mismo valor calculado).".format(money(PRESUPUESTO_TOTAL)))
chk("La contingencia está entre 5 % y 10 % y se justifica con la matriz de riesgos", 0.05 <= PCT_CONT <= 0.10,
    "{} = EMV de los 12 riesgos = {:.1%}.".format(money(CONTINGENCIA), PCT_CONT))
chk("Los costos de personal se calculan con las duraciones y asignaciones del Gantt",
    abs(PERSONAL - sum(a["costo"] for a in A.values())) < 0.01, "Σ actividades = {}.".format(money(PERSONAL)))
chk("El cronograma respeta los 5 meses", INICIO == dt.date(2027, 1, 4) and FIN <= dt.date(2027, 6, 4),
    "{} → {} ({} días hábiles).".format(fdate(INICIO), fdate(FIN), DUR_TOTAL))
chk("Las fechas de los hitos del Acta coinciden con el Gantt", True, "Ambas tablas leen la fecha calculada por el CPM: " + ", ".join("{} {}".format(h["id"], fdate(h["fin"])) for h in HITOS) + ".")
chk("Los riesgos de alto nivel del Acta están en la matriz", set(RIESGOS_ACTA) <= set(r["id"] for r in RIESGOS), ", ".join(RIESGOS_ACTA) + ".")
chk("Ningún rol está sobreasignado (> 100 %) en ningún día", all(v <= 1.0001 for v in MAX_CARGA.values()),
    ", ".join("{} {:.0%}".format(r, v) for r, v in MAX_CARGA.items()) + " (carga máxima diaria).")
chk("El backlog tiene entre 15 y 25 historias y el Sprint 1 cabe en la capacidad", 15 <= len(HU) <= 25 and all(S1_USO[r] <= S1_CAP[r]["horas"] for r in S1_CAP),
    "{} historias; Sprint 1 usa {:.0f} de {:.0f} h.".format(len(HU), sum(S1_USO.values()), sum(v["horas"] for v in S1_CAP.values())))
chk("Los sprints del backlog coinciden con las actividades del Gantt",
    all(A[k]["edt"] in set(h["edt"] for h in HU if h["sprint"] == s) for s, ks in SPRINT_ACT.items() for k in ks),
    "Sprint 1: 1.4.x · Sprint 2: 1.5.1–1.5.2 · Sprint 3: 1.5.2–1.5.3 · Sprint 4: 1.6.x.")
chk("La matriz tiene entre 10 y 12 riesgos", 10 <= len(RIESGOS) <= 12, "{} riesgos.".format(len(RIESGOS)))
chk("La EDT tiene al menos 8 paquetes de trabajo", len(PT) >= 8, "{} paquetes en 3 niveles.".format(len(PT)))
assert all(c[1] for c in CHECKS), [c for c in CHECKS if not c[1]]

b = seccion(14, "14_Verificacion_de_Coherencia", "Lista de verificación de coherencia")
P(b, "Las verificaciones siguientes las ejecuta el generador del plan (generar_plan.py) cada vez que se regeneran los documentos; si alguna regla fallara, el documento no se generaría.")
T(b, ["#", "Regla", "Cumple", "Evidencia"], [[str(i + 1), c[0], "✔ Sí" if c[1] else "✘ No", c[2]] for i, c in enumerate(CHECKS)])

# ---------- Introducción y conclusiones (solo documento integrador) ----------
INTRO = [
    "El presente documento constituye el plan de gestión del proyecto «{}», elaborado para el curso Gerencia de Proyectos Informáticos. El proyecto responde a una necesidad concreta de la Facultad de Ingeniería de Sistemas Computacionales: los estudiantes de primer año no encuentran apoyo académico oportuno, mientras que existen estudiantes avanzados dispuestos a ofrecerlo sin un canal organizado.".format(PROYECTO),
    "El plan adopta un enfoque híbrido. La iniciación y la planificación siguen el enfoque predictivo de la Guía del PMBOK® —acta de constitución, EDT, cronograma con ruta crítica, matriz RACI, presupuesto, riesgos y calidad—, mientras que la construcción del producto se organiza en cuatro sprints de Scrum, guiados por un Product Backlog vinculado a la EDT.",
    "Todos los entregables se generaron a partir de una única fuente de datos, de modo que los códigos de la EDT, las fechas, las asignaciones y los montos son idénticos en cada sección. El proyecto simulado inicia el {} y finaliza el {}, con un presupuesto total de {}.".format(fdate_largo(INICIO), fdate_largo(FIN), money(PRESUPUESTO_TOTAL)),
]
CONCL = [
    "El proyecto es viable en 5 meses: la ruta crítica suma {} días hábiles y cierra el {}, con holgura en la gestión de credenciales institucionales, que es el riesgo externo más sensible.".format(DUR_TOTAL, fdate(FIN)),
    "El presupuesto de {} se construyó de abajo hacia arriba: el {:.0%} corresponde a personal calculado con las horas reales del cronograma, y las reservas se justifican con el valor monetario esperado de los riesgos.".format(money(PRESUPUESTO_TOTAL), PERSONAL / BASE_COSTO),
    "Los riesgos de mayor nivel (escasez de tutores, autorización de credenciales y ausentismo) tienen respuestas incorporadas al alcance y al backlog, como los recordatorios automáticos y la campaña de difusión.",
    "El enfoque híbrido combina el control de las líneas base que exige el patrocinador con la retroalimentación temprana de los usuarios en cada Sprint Review, lo que reduce el riesgo de construir un producto que no se use.",
    "La coherencia entre documentos se verificó punto por punto; cualquier cambio futuro debe pasar por el control integrado de cambios y regenerar todos los documentos desde la misma fuente.",
]

# =============================================================================
# 9. FIGURAS (matplotlib)
# =============================================================================
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import FancyBboxPatch, Patch
from matplotlib.lines import Line2D

C_CRIT, C_NORM, C_LOE, C_INK, C_MUTED, C_GRID = "#c0392b", "#2f6db5", "#9aa5b1", "#1f2933", "#52606d", "#e4e7eb"
VERDE = "#0b6b3a"

def fig_gantt():
    acts = list(A.values())
    fig, ax = plt.subplots(figsize=(13, 10.5))
    for i, a in enumerate(acts):
        y = len(acts) - 1 - i
        if a["hito"]:
            x = mdates.date2num(a["fin"]) + 0.5
            ax.scatter([x], [y], marker="D", s=70, color=C_INK, zorder=3, edgecolors="white", linewidths=1.5)
        else:
            x0 = mdates.date2num(a["inicio"])
            w = mdates.date2num(a["fin"]) + 1 - x0
            col = C_LOE if a["id"] == "A03" else (C_CRIT if a["critica"] else C_NORM)
            ax.barh(y, w, left=x0, height=0.62, color=col, edgecolor="white", linewidth=1)
    for d in FERIADOS:
        ax.axvspan(mdates.date2num(d), mdates.date2num(d) + 1, color="#f4c542", alpha=.35, lw=0)
    for s, ks in SPRINT_ACT.items():
        x0 = mdates.date2num(A[ks[0]]["inicio"])
        x1 = mdates.date2num(A[ks[0]]["fin"]) + 1
        ax.axvspan(x0, x1, color=C_GRID, alpha=.6, lw=0, zorder=0)
        ax.text((x0 + x1) / 2, len(acts) - 0.2, "Sprint {}".format(s), ha="center", va="bottom", fontsize=8, color=C_MUTED)
    ax.set_yticks(range(len(acts)))
    ax.set_yticklabels(["{}  {}".format(a["id"], (a["nombre"][:52] + "…") if len(a["nombre"]) > 53 else a["nombre"]) for a in reversed(acts)], fontsize=7.5, color=C_INK)
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    ax.tick_params(axis="x", labelsize=8, colors=C_MUTED)
    ax.set_xlim(mdates.date2num(INICIO) - 2, mdates.date2num(FIN) + 3)
    ax.set_ylim(-0.8, len(acts) + 0.6)
    ax.grid(axis="x", color=C_GRID, lw=.8)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(C_MUTED)
    ax.legend(handles=[Patch(color=C_CRIT, label="Ruta crítica"), Patch(color=C_NORM, label="Con holgura"),
                       Patch(color=C_LOE, label="Nivel de esfuerzo (A03)"), Patch(color="#f4c542", alpha=.5, label="Feriado"),
                       Line2D([], [], marker="D", ls="", color=C_INK, label="Hito")],
              loc="lower left", fontsize=8, frameon=False, ncol=5, bbox_to_anchor=(0, -0.07))
    ax.set_title("Cronograma {} · {} a {} · {} días hábiles".format(NOMBRE_CORTO, fdate(INICIO), fdate(FIN), DUR_TOTAL), fontsize=11, color=C_INK, loc="left")
    fig.tight_layout()
    fig.savefig(os.path.join(D_IMG, "gantt.png"), dpi=170, bbox_inches="tight")
    plt.close(fig)

def fig_edt():
    n2 = [c for c in EDT_N2 if c != "1"]
    fig, ax = plt.subplots(figsize=(15, 7.2))
    ax.set_xlim(0, len(n2))
    ax.set_ylim(0, 10)
    ax.axis("off")
    def caja(x, y, w, h, txt, fc, ec, col="white", fs=8, bold=False):
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=fc, ec=ec, lw=1.2))
        ax.text(x, y, txt, ha="center", va="center", fontsize=fs, color=col, wrap=True, fontweight="bold" if bold else "normal")
    import textwrap
    cx = len(n2) / 2
    caja(cx, 9.3, 4.2, 0.9, "1  " + EDT_N2["1"], VERDE, VERDE, fs=10, bold=True)
    ax.plot([0.5, len(n2) - 0.5], [8.35, 8.35], color=C_MUTED, lw=1)
    ax.plot([cx, cx], [8.85, 8.35], color=C_MUTED, lw=1)
    for i, c in enumerate(n2):
        x = i + 0.5
        ax.plot([x, x], [8.35, 8.0], color=C_MUTED, lw=1)
        caja(x, 7.45, 0.92, 1.1, c + "\n" + textwrap.fill(EDT_N2[c], 15), "#d9efe2", VERDE, col=C_INK, fs=7.2, bold=True)
        hijos = [p for p in PT if p.startswith(c + ".")]
        for j, p in enumerate(hijos):
            y = 5.9 - j * 1.75
            ax.plot([x - 0.47, x - 0.47, x - 0.44], [6.9, y, y], color=C_MUTED, lw=.8)
            caja(x + 0.02, y, 0.88, 1.5, p + "\n" + textwrap.fill(PT[p][0], 16), "white", "#7b8794", col=C_INK, fs=6.6)
    fig.tight_layout()
    fig.savefig(os.path.join(D_IMG, "edt.png"), dpi=170, bbox_inches="tight")
    plt.close(fig)

def fig_heat():
    fig, ax = plt.subplots(figsize=(7.5, 6))
    col = {"Bajo": "#cfe8d5", "Medio": "#f6dfa4", "Alto": "#f0a8a0"}
    for p in range(1, 6):
        for i in range(1, 6):
            n = p * i
            ax.add_patch(plt.Rectangle((i - 0.5, p - 0.5), 1, 1, fc=col[zona(n)], ec="white", lw=2))
            ids = [r["id"] for r in RIESGOS if r["p"] == p and r["i"] == i]
            ax.text(i, p + 0.28, str(n), ha="center", va="center", fontsize=7, color=C_MUTED)
            if ids:
                ax.text(i, p - 0.05, "\n".join(ids), ha="center", va="center", fontsize=9, color=C_INK, fontweight="bold")
    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(0.5, 5.5)
    ax.set_xticks(range(1, 6))
    ax.set_yticks(range(1, 6))
    ax.set_xlabel("Impacto", color=C_INK)
    ax.set_ylabel("Probabilidad", color=C_INK)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(colors=C_MUTED, length=0)
    ax.legend(handles=[Patch(color=col[k], label="{} ({})".format(k, t)) for k, t in [("Alto", "≥ 15"), ("Medio", "8–14"), ("Bajo", "≤ 7")]],
              loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=3, frameon=False, fontsize=9)
    ax.set_title("Mapa de calor de riesgos (P × I)", color=C_INK, loc="left")
    fig.tight_layout()
    fig.savefig(os.path.join(D_IMG, "heatmap.png"), dpi=170)
    plt.close(fig)

fig_gantt()
fig_edt()
fig_heat()

# =============================================================================
# 10. ARCHIVOS DEL CRONOGRAMA
# =============================================================================
with open(os.path.join(D_CRON, "Cronograma_PlanificadorGantt.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["id", "nombre", "fase", "responsable", "inicio", "fin", "duracion", "avance", "hito", "depende"])
    for a in A.values():
        w.writerow([a["id"], "{} {}".format(a["edt"], a["nombre"]), "{} {}".format(a["edt"][:3], EDT_N2[a["edt"][:3]]), RN[a["resp"]],
                    a["inicio"].isoformat(), a["fin"].isoformat(), (a["fin"] - a["inicio"]).days + 1, 0, "si" if a["hito"] else "no", " ".join(a["pred"])])

with open(os.path.join(D_CRON, "Actividades.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["ID", "EDT", "Actividad", "Duración (días hábiles)", "Predecesoras", "Responsable", "Inicio", "Fin", "Holgura", "Crítica", "Horas", "Costo personal (B/.)"])
    for a in A.values():
        w.writerow([a["id"], a["edt"], a["nombre"], a["dur"], " ".join(a["pred"]), RN[a["resp"]], a["inicio"].isoformat(), a["fin"].isoformat(),
                    a["holgura"], "Sí" if a["critica"] else "No", "{:.0f}".format(sum(a["horas"].values())), "{:.2f}".format(a["costo"]).replace(".", ",")])

# GanttProject / XML: tareas agrupadas bajo resúmenes de nivel 2 de la EDT
FILAS_XML = []
uid = 0
for c in EDT_N2:
    if c == "1":
        continue
    hijos = [a for a in A.values() if a["edt"].startswith(c + ".")]
    uid += 1
    ini = min(a["inicio"] for a in hijos)
    fin = max(a["fin"] for a in hijos)
    FILAS_XML.append(dict(uid=uid, nombre=EDT_N2[c], wbs=c, nivel=1, resumen=True, hito=False, inicio=ini, fin=fin,
                          dur=sum(1 for d in DH if ini <= d <= fin), pred=[], critica=False, a=None))
    for a in hijos:
        uid += 1
        a["uid"] = uid
        FILAS_XML.append(dict(uid=uid, nombre=a["nombre"], wbs=a["edt"], nivel=2, resumen=False, hito=a["hito"], inicio=a["inicio"], fin=a["fin"],
                              dur=a["dur"], pred=a["pred"], critica=a["critica"], a=a))
for i, fx in enumerate(FILAS_XML):
    fx["id"] = i + 1
    fx["outline"] = fx["wbs"][2:] if fx["nivel"] == 1 else None
cont = defaultdict(int)
for fx in FILAS_XML:
    if fx["nivel"] == 1:
        padre = fx["outline"]
    else:
        cont[padre] += 1
        fx["outline"] = "{}.{}".format(padre, cont[padre])

with open(os.path.join(D_CRON, "Cronograma_GanttProject.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["ID", "Name", "Begin date", "End date", "Duration", "Completion", "Cost", "Coordinator", "Predecessors", "Outline number", "Resources", "Assignments", "Task color", "Web Link", "Notes"])
    for fx in FILAS_XML:
        a = fx["a"]
        preds = ";".join(str(A[p]["uid"]) for p in fx["pred"])
        res = ";".join(RN[r] for r in a["alloc"]) if a else ""
        asg = ";".join("{}:{:.0f}".format(RN[r], v * 100) for r, v in a["alloc"].items()) if a else ""
        w.writerow([fx["id"], fx["nombre"], fx["inicio"].strftime("%d/%m/%Y"), fx["fin"].strftime("%d/%m/%Y"), fx["dur"], 0,
                    "{:.2f}".format(a["costo"]) if a else "", RN[a["resp"]] if a else "", preds, fx["outline"], res, asg,
                    "#c0392b" if fx["critica"] else "", "", "EDT " + fx["wbs"] + (" · " + a["id"] if a else "")])

def xesc(s):
    return html.escape(str(s), quote=False)
def xdur(dias):
    return "PT{}H0M0S".format(int(round(dias * HORAS_DIA)))
x = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', '<Project xmlns="http://schemas.microsoft.com/project">',
     "<SaveVersion>14</SaveVersion>", "<Name>{}.xml</Name>".format(NOMBRE_CORTO), "<Title>{}</Title>".format(xesc(PROYECTO)),
     "<ScheduleFromStart>1</ScheduleFromStart>", "<StartDate>{}T08:00:00</StartDate>".format(INICIO.isoformat()),
     "<FinishDate>{}T17:00:00</FinishDate>".format(FIN.isoformat()), "<CalendarUID>1</CalendarUID>",
     "<DefaultStartTime>08:00:00</DefaultStartTime>", "<DefaultFinishTime>17:00:00</DefaultFinishTime>",
     "<MinutesPerDay>480</MinutesPerDay>", "<MinutesPerWeek>2400</MinutesPerWeek>", "<DaysPerMonth>20</DaysPerMonth>",
     "<CurrencySymbol>B/.</CurrencySymbol>", "<CurrencyCode>PAB</CurrencyCode>",
     "<Calendars><Calendar><UID>1</UID><Name>Estándar Panamá 2027</Name><IsBaseCalendar>1</IsBaseCalendar><WeekDays>"]
for dtype in range(1, 8):
    if dtype in (1, 7):
        x.append("<WeekDay><DayType>{}</DayType><DayWorking>0</DayWorking></WeekDay>".format(dtype))
    else:
        x.append("<WeekDay><DayType>{}</DayType><DayWorking>1</DayWorking><WorkingTimes><WorkingTime><FromTime>08:00:00</FromTime><ToTime>12:00:00</ToTime></WorkingTime><WorkingTime><FromTime>13:00:00</FromTime><ToTime>17:00:00</ToTime></WorkingTime></WorkingTimes></WeekDay>".format(dtype))
for d in FERIADOS:
    x.append("<WeekDay><DayType>0</DayType><DayWorking>0</DayWorking><TimePeriod><FromDate>{0}T00:00:00</FromDate><ToDate>{0}T23:59:00</ToDate></TimePeriod></WeekDay>".format(d.isoformat()))
x.append("</WeekDays></Calendar></Calendars><Tasks>")
for fx in FILAS_XML:
    fin_h = "{}T{}".format(fx["fin"].isoformat(), "08:00:00" if fx["hito"] else "17:00:00")
    ini_h = "{}T08:00:00".format((fx["fin"] if fx["hito"] else fx["inicio"]).isoformat())
    t = ["<Task>", "<UID>{}</UID>".format(fx["uid"]), "<ID>{}</ID>".format(fx["id"]), "<Name>{}</Name>".format(xesc(fx["nombre"])),
         "<Type>1</Type>", "<IsNull>0</IsNull>", "<WBS>{}</WBS>".format(fx["wbs"]), "<OutlineNumber>{}</OutlineNumber>".format(fx["outline"]),
         "<OutlineLevel>{}</OutlineLevel>".format(fx["nivel"]), "<Priority>500</Priority>", "<Start>{}</Start>".format(ini_h if not fx["hito"] else fin_h.replace("T08", "T17")),
         "<Finish>{}</Finish>".format(fin_h if not fx["hito"] else fin_h.replace("T08", "T17")), "<Duration>{}</Duration>".format(xdur(fx["dur"])), "<DurationFormat>7</DurationFormat>",
         "<Milestone>{}</Milestone>".format(int(fx["hito"])), "<Summary>{}</Summary>".format(int(fx["resumen"])),
         "<Critical>{}</Critical>".format(int(fx["critica"])), "<CalendarUID>-1</CalendarUID>"]
    if fx["a"]:
        t.append("<Notes>{}</Notes>".format(xesc("{} · EDT {} · Responsable: {}".format(fx["a"]["id"], fx["wbs"], RN[fx["a"]["resp"]]))))
    for p in fx["pred"]:
        t.append("<PredecessorLink><PredecessorUID>{}</PredecessorUID><Type>1</Type><CrossProject>0</CrossProject><LinkLag>0</LinkLag><LagFormat>7</LagFormat></PredecessorLink>".format(A[p]["uid"]))
    t.append("</Task>")
    x.append("".join(t))
x.append("</Tasks><Resources>")
RUID = {r: i + 1 for i, r in enumerate(ROLES)}
for r in ROLES:
    x.append("<Resource><UID>{0}</UID><ID>{0}</ID><Name>{1}</Name><Type>1</Type><Initials>{2}</Initials><MaxUnits>1.00</MaxUnits><StandardRate>{3:.2f}</StandardRate><StandardRateFormat>2</StandardRateFormat><CalendarUID>1</CalendarUID></Resource>".format(
        RUID[r], xesc(RN[r]), r, TARIFA[r]))
x.append("</Resources><Assignments>")
au = 0
for a in A.values():
    for r, v in a["alloc"].items():
        au += 1
        x.append("<Assignment><UID>{}</UID><TaskUID>{}</TaskUID><ResourceUID>{}</ResourceUID><Units>{:.2f}</Units><Work>{}</Work></Assignment>".format(
            au, a["uid"], RUID[r], v, xdur(a["dur"] * v)))
x.append("</Assignments></Project>")
with open(os.path.join(D_CRON, "Cronograma_MSProject.xml"), "w", encoding="utf-8") as f:
    f.write("\n".join(x))

# =============================================================================
# 11. RENDERIZADO: Markdown, HTML y DOCX
# =============================================================================
def md_inline(s):
    return s.replace("\n", "<br>").replace("|", "\\|")

def render_md(bloques, nivel_base=1):
    out = []
    for blq in bloques:
        k = blq[0]
        if k == "h":
            out.append("#" * (blq[1] + nivel_base - 1) + " " + blq[2])
        elif k == "p":
            out.append(blq[1])
        elif k == "note":
            out.append("> " + blq[1])
        elif k == "ul":
            out.append("\n".join("- " + i for i in blq[1]))
        elif k == "ol":
            out.append("\n".join("{}. {}".format(n + 1, i) for n, i in enumerate(blq[1])))
        elif k == "pre":
            out.append("```\n" + blq[1] + "\n```")
        elif k == "img":
            out.append("![{}](../img/{})\n\n*{}*".format(blq[2], blq[1], blq[2]))
        elif k == "table":
            enc, filas = blq[1], blq[2]
            out.append("| " + " | ".join(enc) + " |\n|" + "|".join("---" for _ in enc) + "|\n" +
                       "\n".join("| " + " | ".join(md_inline(c) for c in f) + " |" for f in filas))
        out.append("")
    return "\n".join(out)

for s in SECCIONES:
    with open(os.path.join(D_ENT, s["slug"] + ".md"), "w", encoding="utf-8") as f:
        f.write("# {}. {}\n\n*{} · Gerencia de Proyectos Informáticos (8469) · 1LS241*\n\n".format(s["num"], s["titulo"], PROYECTO))
        f.write(render_md(s["bloques"], 1))

# ---- HTML ----
def h_inline(s):
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return s.replace("\n", "<br>")

def render_html(bloques):
    out = []
    for blq in bloques:
        k = blq[0]
        if k == "h":
            out.append("<h{0}>{1}</h{0}>".format(blq[1] + 1, h_inline(blq[2])))
        elif k == "p":
            out.append("<p>" + h_inline(blq[1]) + "</p>")
        elif k == "note":
            out.append('<p class="note">' + h_inline(blq[1]) + "</p>")
        elif k in ("ul", "ol"):
            out.append("<{0}>{1}</{0}>".format(k, "".join("<li>" + h_inline(i) + "</li>" for i in blq[1])))
        elif k == "pre":
            out.append("<pre>" + html.escape(blq[1]) + "</pre>")
        elif k == "img":
            out.append('<figure><img src="img/{}" alt="{}"><figcaption>{}</figcaption></figure>'.format(blq[1], html.escape(blq[2]), html.escape(blq[2])))
        elif k == "table":
            op = blq[3]
            hl = set(op.get("resaltar", []))
            filas = "".join("<tr{}>{}</tr>".format(' class="crit"' if i in hl else "", "".join("<td>" + h_inline(c) + "</td>" for c in f)) for i, f in enumerate(blq[2]))
            out.append('<div class="tw"><table class="{}"><thead><tr>{}</tr></thead><tbody>{}</tbody></table></div>'.format(
                "small" if op.get("small") else "", "".join("<th>" + h_inline(e) + "</th>" for e in blq[1]), filas))
    return "\n".join(out)

ORDEN = [s for s in SECCIONES if s["num"] != 14] + [s for s in SECCIONES if s["num"] == 14]
CSS = """
:root{--verde:#0b6b3a;--verde2:#e3f1e8;--ink:#1f2933;--muted:#52606d;--line:#cbd2d9;--bg:#ffffff;--crit:#fde2df}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 "Segoe UI",Calibri,Arial,sans-serif}
main{max-width:1050px;margin:0 auto;padding:24px 16px 80px}
.portada{min-height:92vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;border-bottom:3px solid var(--verde);margin-bottom:32px}
.portada h1{color:var(--verde);font-size:2rem;margin:.6em 0 .2em}.portada .u{font-weight:700;color:var(--verde);font-size:1.25rem}
.portada table{margin:24px auto;border-collapse:collapse;min-width:min(520px,100%)}.portada td{border:1px solid var(--line);padding:6px 10px;text-align:left}
h2{color:var(--verde);border-bottom:2px solid var(--verde);padding-bottom:4px;margin-top:2.4em;break-after:avoid}h3{color:var(--verde);margin-top:1.6em}h4{margin-top:1.3em}
.tw{overflow-x:auto;margin:12px 0}table{border-collapse:collapse;width:100%}th{background:var(--verde);color:#fff;text-align:left;padding:6px 8px;font-weight:600}
td{border:1px solid var(--line);padding:5px 8px;vertical-align:top}tbody tr:nth-child(even) td{background:#f7faf8}table.small{font-size:.82rem}
tr.crit td{background:var(--crit)!important}pre{background:#f5f7fa;border:1px solid var(--line);padding:12px;overflow-x:auto;font-size:.85rem;line-height:1.35}
figure{margin:16px 0;text-align:center}figure img{max-width:100%;border:1px solid var(--line)}figcaption{color:var(--muted);font-size:.85rem;font-style:italic}
.note{border-left:4px solid var(--verde);background:var(--verde2);padding:8px 12px}nav.toc ol{columns:2;column-gap:32px}nav.toc a{color:var(--verde);text-decoration:none}
.top{position:sticky;top:0;background:#fff;border-bottom:1px solid var(--line);padding:6px 16px;font-size:.85rem;z-index:2}.top a{color:var(--verde);margin-right:14px}
@media print{.top{display:none}h2{break-before:page}.portada{min-height:auto;height:100vh}body{font-size:11pt}}
"""
partes = ['<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
          "<title>Plan de Gestión TutorFISC</title><style>{}</style></head><body>".format(CSS),
          '<div class="top"><a href="../index.html">← GPI</a><a href="Plan_Gestion_Tutorias.docx">Descargar Word</a><a href="cronograma/Cronograma_MSProject.xml">Gantt (XML)</a><a href="cronograma/Cronograma_PlanificadorGantt.csv">Gantt (CSV)</a></div><main>',
          '<section class="portada"><div class="u">Universidad Tecnológica de Panamá</div><div>Facultad de Ingeniería de Sistemas Computacionales</div>',
          "<div>Gerencia de Proyectos Informáticos (8469) · Grupo 1LS241 · II Semestre 2026</div>",
          "<h1>Plan de Gestión del Proyecto</h1><div style='font-size:1.2rem'>{}</div>".format(html.escape(PROYECTO)),
          "<table><tr><td>Equipo N.º</td><td>______</td></tr><tr><td>Integrantes</td><td>______________________<br>______________________<br>______________________<br>______________________<br>______________________</td></tr>",
          "<tr><td>Docente</td><td>______________________</td></tr><tr><td>Fecha de entrega</td><td>______________________</td></tr></table></section>",
          '<nav class="toc"><h2 style="break-before:auto">Índice</h2><ol><li><a href="#intro">Introducción</a></li>']
for s in ORDEN:
    partes.append('<li><a href="#{}">{}</a></li>'.format(s["slug"], html.escape(s["titulo"])))
partes.append('<li><a href="#concl">Conclusiones</a></li><li><a href="#refs">Referencias</a></li></ol></nav>')
partes.append('<h2 id="intro">Introducción</h2>' + "".join("<p>{}</p>".format(h_inline(p)) for p in INTRO))
for n, s in enumerate(ORDEN, 1):
    partes.append('<h2 id="{}">{}. {}</h2>'.format(s["slug"], n, html.escape(s["titulo"])))
    partes.append(render_html(s["bloques"]).replace("<h2>", "<h3>").replace("</h2>", "</h3>").replace("<h4>", "<h4>"))
REFS = ["Project Management Institute. (2021). Guía de los fundamentos para la dirección de proyectos (Guía del PMBOK®), 7.ª ed. PMI.",
        "Schwaber, K. & Sutherland, J. (2020). La Guía de Scrum. scrumguides.org.",
        "Gido, J., Clements, J. & Baker, R. (2018). Administración exitosa de proyectos, 6.ª ed. Cengage Learning.",
        "ISO/IEC 25010:2023. Systems and software engineering — Product quality model.",
        "W3C. (2018). Web Content Accessibility Guidelines (WCAG) 2.1.",
        "OWASP Foundation. (2021). OWASP Top 10.",
        "Asamblea Nacional de Panamá. (2019). Ley 81 de 26 de marzo de 2019, sobre protección de datos personales."]
partes.append('<h2 id="concl">Conclusiones</h2><ul>' + "".join("<li>{}</li>".format(h_inline(c)) for c in CONCL) + "</ul>")
partes.append('<h2 id="refs">Referencias</h2><ul>' + "".join("<li>{}</li>".format(html.escape(r)) for r in REFS) + "</ul>")
partes.append("</main></body></html>")
HTML_OUT = "\n".join(partes)
# En el documento integrador los títulos internos bajan un nivel (h2 de sección → h3...)
with open(os.path.join(BASE, "plan.html"), "w", encoding="utf-8") as f:
    f.write(HTML_OUT)

# ---- DOCX ----
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.59), Cm(27.94)
for m in ("left_margin", "right_margin"):
    setattr(sec, m, Cm(2.2))
sec.top_margin = sec.bottom_margin = Cm(2.0)
st = doc.styles["Normal"]
st.font.name = "Calibri"
st.font.size = Pt(11)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
for nombre, tam in (("Heading 1", 16), ("Heading 2", 13), ("Heading 3", 11.5), ("Heading 4", 11)):
    hs = doc.styles[nombre]
    hs.font.color.rgb = RGBColor(0x0B, 0x6B, 0x3A)
    hs.font.size = Pt(tam)
    hs.font.name = "Calibri"

def runs(par, texto, size=None, bold=False):
    for i, trozo in enumerate(re.split(r"\*\*(.+?)\*\*", texto)):
        if not trozo:
            continue
        r = par.add_run(trozo)
        r.bold = bold or (i % 2 == 1)
        if size:
            r.font.size = Pt(size)

def sombrear(celda, color):
    tcPr = celda._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color)
    tcPr.append(shd)

def repetir_encabezado(fila):
    trPr = fila._tr.get_or_add_trPr()
    e = OxmlElement("w:tblHeader")
    e.set(qn("w:val"), "true")
    trPr.append(e)

def campo(par, instr):
    r = par.add_run()
    a = OxmlElement("w:fldChar"); a.set(qn("w:fldCharType"), "begin")
    b_ = OxmlElement("w:instrText"); b_.set(qn("xml:space"), "preserve"); b_.text = instr
    c_ = OxmlElement("w:fldChar"); c_.set(qn("w:fldCharType"), "separate")
    t_ = OxmlElement("w:t"); t_.text = "Clic derecho → Actualizar campo para ver el índice."
    d_ = OxmlElement("w:fldChar"); d_.set(qn("w:fldCharType"), "end")
    r._r.append(a); r._r.append(b_); r._r.append(c_); r._r.append(t_); r._r.append(d_)

def docx_bloques(bloques, base):
    for blq in bloques:
        k = blq[0]
        if k == "h":
            doc.add_heading(blq[2], level=min(blq[1] + base - 1, 4))
        elif k == "p":
            par = doc.add_paragraph()
            par.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            runs(par, blq[1])
        elif k == "note":
            par = doc.add_paragraph()
            par.paragraph_format.left_indent = Cm(0.5)
            runs(par, blq[1], size=9.5)
            for r in par.runs:
                r.italic = True
        elif k in ("ul", "ol"):
            for i in blq[1]:
                runs(doc.add_paragraph(style="List Bullet" if k == "ul" else "List Number"), i)
        elif k == "pre":
            par = doc.add_paragraph()
            r = par.add_run(blq[1])
            r.font.name = "Consolas"
            r.font.size = Pt(8.5)
        elif k == "img":
            doc.add_picture(os.path.join(D_IMG, blq[1]), width=Cm(17))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            cap = doc.add_paragraph()
            cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = cap.add_run(blq[2]); r.italic = True; r.font.size = Pt(9)
        elif k == "table":
            enc, filas, op = blq[1], blq[2], blq[3]
            fs = 8 if op.get("small") or len(enc) > 5 else 9.5
            hl = set(op.get("resaltar", []))
            t = doc.add_table(rows=1, cols=len(enc))
            t.style = "Table Grid"
            t.alignment = WD_TABLE_ALIGNMENT.CENTER
            for j, e in enumerate(enc):
                c = t.rows[0].cells[j]
                c.text = ""
                runs(c.paragraphs[0], e, size=fs, bold=True)
                c.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                sombrear(c, "0B6B3A")
            repetir_encabezado(t.rows[0])
            for i, f in enumerate(filas):
                cells = t.add_row().cells
                for j, v in enumerate(f):
                    cells[j].text = ""
                    lineas = v.split("\n")
                    runs(cells[j].paragraphs[0], lineas[0], size=fs)
                    for ln in lineas[1:]:
                        runs(cells[j].add_paragraph(), ln, size=fs)
                    if i in hl:
                        sombrear(cells[j], "FDE2DF")
            doc.add_paragraph()

# Portada
for txt, tam, neg in [("Universidad Tecnológica de Panamá", 18, True), ("Facultad de Ingeniería de Sistemas Computacionales", 13, False),
                      ("Gerencia de Proyectos Informáticos (8469) · Grupo 1LS241 · II Semestre 2026", 11, False), ("", 11, False),
                      ("PLAN DE GESTIÓN DEL PROYECTO", 22, True), (PROYECTO, 15, False), ("", 11, False)]:
    par = doc.add_paragraph()
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = par.add_run(txt); r.font.size = Pt(tam); r.bold = neg
    if neg:
        r.font.color.rgb = RGBColor(0x0B, 0x6B, 0x3A)
t = doc.add_table(rows=0, cols=2); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
for a_, b_ in [("Equipo N.º", "______"), ("Integrantes", "\n".join(["______________________________"] * 5)),
               ("Docente", "______________________________"), ("Fecha de entrega", "______________________________"),
               ("Período del proyecto simulado", "{} – {}".format(fdate(INICIO), fdate(FIN)))]:
    c = t.add_row().cells
    c[0].text = a_; c[0].paragraphs[0].runs[0].bold = True
    c[1].text = b_
doc.add_page_break()
doc.add_heading("Índice", level=1)
campo(doc.add_paragraph(), 'TOC \\o "1-2" \\h \\z \\u')
doc.add_page_break()
doc.add_heading("Introducción", level=1)
for p in INTRO:
    par = doc.add_paragraph(); par.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY; runs(par, p)
for n, s in enumerate(ORDEN, 1):
    doc.add_page_break()
    doc.add_heading("{}. {}".format(n, s["titulo"]), level=1)
    docx_bloques(s["bloques"], 1)
doc.add_page_break()
doc.add_heading("Conclusiones", level=1)
for c in CONCL:
    runs(doc.add_paragraph(style="List Bullet"), c)
doc.add_heading("Referencias", level=1)
for r in REFS:
    doc.add_paragraph(r)
# número de página en el pie
fp = sec.footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = fp.add_run()
for tipo, txt in (("begin", None), (None, "PAGE"), ("end", None)):
    if tipo:
        e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), tipo); r._r.append(e)
    else:
        e = OxmlElement("w:instrText"); e.set(qn("xml:space"), "preserve"); e.text = txt; r._r.append(e)
doc.save(os.path.join(BASE, "Plan_Gestion_Tutorias.docx"))

# Documento integrador también en Markdown
with open(os.path.join(D_ENT, "12_Documento_Integrador.md"), "w", encoding="utf-8") as f:
    f.write("# Plan de Gestión del Proyecto – {}\n\n".format(PROYECTO))
    f.write("**Universidad Tecnológica de Panamá** · Facultad de Ingeniería de Sistemas Computacionales  \nGerencia de Proyectos Informáticos (8469) · Grupo 1LS241 · II Semestre 2026  \n")
    f.write("Equipo N.º ____ · Integrantes: ________ · Docente: ________ · Fecha: ________\n\n## Índice\n\n")
    f.write("\n".join("{}. {}".format(n, s["titulo"]) for n, s in enumerate(ORDEN, 1)) + "\n\n## Introducción\n\n" + "\n\n".join(INTRO) + "\n\n")
    for n, s in enumerate(ORDEN, 1):
        f.write("## {}. {}\n\n".format(n, s["titulo"]) + render_md(s["bloques"], 2).replace("\n## ", "\n### ").replace("\n### #", "\n####") + "\n")
    f.write("## Conclusiones\n\n" + "\n".join("- " + c for c in CONCL) + "\n\n## Referencias\n\n" + "\n".join("- " + r for r in REFS) + "\n")

# Resumen en consola
print("Duración: {} días hábiles · {} → {}".format(DUR_TOTAL, INICIO, FIN))
print("Personal {:,.2f} · Directos {:,.2f} · Base {:,.2f} · Contingencia {:,.0f} ({:.1%}) · Gestión {:,.0f} · TOTAL {:,.2f}".format(
    PERSONAL, TOTAL_DIRECTOS, BASE_COSTO, CONTINGENCIA, PCT_CONT, RESERVA_GESTION, PRESUPUESTO_TOTAL))
print("Ruta crítica:", ruta_txt())
print("Carga máxima:", MAX_CARGA)
print("Sprint 1:", S1_INI, "→", S1_FIN, dict(S1_USO), {r: v["horas"] for r, v in S1_CAP.items()})
print("Verificaciones:", sum(c[1] for c in CHECKS), "/", len(CHECKS))
