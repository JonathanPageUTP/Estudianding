# Prompt: material para aprenderse una charla (modelo visual `semestre2/gr/parcial1`)

Sirve para preparar una **charla / exposición / presentación oral**: aprenderse el contenido,
el orden en que se dice y las palabras que no pueden faltar.
Copia el bloque de abajo, cambia los valores entre `<…>` y pégalo en Claude Code.
Ejemplo: `Aplica PROMPT-CHARLA.md a semestre2/gpi/charla1, materia "Gestión de Proyectos", sigla GPI, tema "Gestión de riesgos"`.

---

```text
Lee PROMPT-CHARLA.md y aplícalo a:

- Carpeta:        <semestre2/gpi/charla1>
- Materia:        <Gestión de Proyectos Informáticos>
- Sigla corta:    <GPI>                    (para títulos y claves de localStorage)
- Tema / título:  <Gestión de riesgos en proyectos de software>
- Duración:       <10 min>                 (tiempo total de la charla)
- Expositores:    <yo solo | Ana, Luis, yo> (si es en grupo, indica qué parte me toca)
- Material base:  <nombre del PDF / PPTX / transcripción / notas>  (si no lo indico, usa todo lo de la carpeta)

Puntos específicos que quiero cubrir (en este orden):
1. <Qué es un riesgo y diferencia con un problema>
2. <Matriz probabilidad × impacto>
3. <Estrategias: evitar, transferir, mitigar, aceptar>
4. <Ejemplo real / caso>
(si no doy puntos, propónlos tú a partir del material y dímelos antes de generar)

Usa como referencia de diseño semestre2/gr/parcial1. Todo el contenido sale SOLO del
material de la carpeta y de lo que te escribo aquí: no inventes datos.
```

---

## Qué hay que generar

Todo dentro de la carpeta de la charla, en archivos HTML **autocontenidos** (CSS y JS inline, sin
librerías externas, sin build), en español y pensados primero para el celular.

| Archivo | Botón en el índice | Qué es |
|---|---|---|
| `guion.html` | Guion | El guion de la charla, punto por punto, en el orden en que se dice |
| `claves.html` | Palabras Clave | Palabras y frases que no pueden faltar, por punto, con modo práctica |
| `resumen.html` | Resumen General | La charla completa en una sola pantalla: idea central + mapa de puntos |
| `puntos.html` | Resumen por Punto | Un resumen denso de cada punto específico, plegable |
| `flash.html` | FlashCards | Tarjetas para memorizar orden, datos y posibles preguntas del público |
| `ensayo.html` | Ensayo | Modo práctica con cronómetro: decir cada punto de memoria y autoevaluarse |
| `index.html` | — | Menú de la charla (ver abajo) |

Además: si la materia aún no enlaza esta charla, agrega el botón en `<materia>/index.html`.

## Proceso

1. **Leer todo el material** de la carpeta completo (PDF, PPTX, transcripciones, notas).
   - PDF: `pdftotext -raw -enc UTF-8`; las láminas que salen vacías son imagen: renderizarlas
     (`pip install --user pypdfium2`) y mirarlas.
   - PPTX: usar el skill de pptx; leer también las **notas del orador** si existen.
2. **Puntos específicos**: son el esqueleto de todo. Cada página sigue ese orden, numerado
   (`1 · PUNTO`, `2 · PUNTO`…), con una apertura (`0 · INTRO`) y un cierre (`FIN · CIERRE`).
   Si no los di, proponerlos a partir del material y confirmarlos antes de generar.
3. **Tiempo**: repartir la duración total entre intro, puntos y cierre (≈10 % intro, 80 % puntos,
   10 % cierre, ajustado al peso de cada punto). Ese reparto aparece en el guion y en el ensayo.
4. **Fidelidad**: usar la terminología del material. No agregar datos, cifras ni ejemplos que no
   estén en el material o en mi mensaje. Las mnemotecnias y frases de transición sí son
   inventadas, pero deben codificar exactamente lo que dice el material.
5. Generar las páginas, luego el `index.html`, luego revisar (ver *Verificación*).
6. Commit con mensaje como los del historial:
   `Charla <SIGLA> <tema corto>: guion, palabras clave, resúmenes, flashcards y ensayo`.
7. Hacer push.

## Estilo visual común

Igual que en `PROMPT-PARCIAL.md` (sección *Estilo visual común*): tema oscuro con tokens en
`:root`, columna `max-width ≈ 460px`, gutter 16px, sin scroll horizontal, bloque
`@media (max-width:560px)`, inputs a 16px, botones ≥ 44px, `localStorage` siempre en `try/catch`.
Claves con prefijo: `<sigla>_charla<N>_…_v1` (ej. `gpi_charla1_flash_v1`).

## Detalle de cada página

### `guion.html` — Guion
- Header fijo "Guion · <Tema>" con duración total y barra de progreso de lectura.
- Una tarjeta por bloque (`0 · Intro`, `1 · …`, …, `Cierre`), cada una con:
  - **Tiempo** asignado (`⏱ 1:30`) y tiempo acumulado (`→ 3:00`).
  - **Objetivo** del punto en una línea ("Que entiendan que…").
  - **Qué decir**: 3–6 viñetas cortas en orden, no párrafos para leer.
  - **Palabras clave** del punto como chips resaltados.
  - **Dato / ejemplo** que lo respalda (con la fuente: lámina o página del material).
  - **Transición** al siguiente punto: una frase lista para decir ("Ahora que sabemos X, veamos Y").
  - Si hay lámina asociada: "🖼 Lámina <n>".
- Botón **🎤 Modo escenario**: letra grande, solo viñetas y palabras clave, pantalla siempre
  encendida si el navegador lo permite (`navigator.wakeLock` dentro de `try/catch`), se pasa de
  bloque tocando la mitad derecha/izquierda.
- Si es en grupo: marcar con color qué bloques son míos y quién habla antes/después.

### `claves.html` — Palabras clave
- Agrupadas por punto, con chips de anclas arriba.
- Cada item, mismo formato que `siglas.html` del parcial:
  ```html
  <div class="s"><span class="k">PIRA</span><div class="b">
    <div class="tt">Estrategias de respuesta al riesgo</div>
    <div class="x"><b>P</b>revenir · <b>I</b>mpacto reducido · <b>R</b>edistribuir · <b>A</b>ceptar</div>
    <div class="m">"Pira" = fogata: hay que apagar el riesgo</div>
  </div></div>
  ```
  `k` = término clave o sigla, `tt` = punto de la charla, `x` = definición corta / expansión,
  `m` = mnemotecnia o frase para recordarlo.
- Botón **🙈 Modo práctica** (oculta las definiciones; tocar revela).
- Al final: **SECUENCIA DE LA CHARLA** (una sigla/frase que codifica el orden de todos los
  puntos), **NÚMEROS Y DATOS CLAVE** y **NO CONFUNDIR**.

### `resumen.html` — Resumen general
- Cabe idealmente en una o dos pantallas del celular.
- **Idea central** en una frase grande (lo que el público debe recordar).
- **Mapa de la charla**: flujo vertical con los puntos numerados, cada uno con su frase-resumen
  de una línea y su tiempo.
- **Mensaje de cierre** / llamado a la acción.
- Resumen del contenido general en 5–8 viñetas.

### `puntos.html` — Resumen por punto
- Buscador, chips de navegación, botón **Plegar todo**.
- Una sección plegable por punto (`1 Qué es un riesgo ▾`) con:
  - Resumen denso en viñetas (lo que dice el material sobre ese punto, completo).
  - Definiciones textuales en `<blockquote class="q">` cuando el material las tenga.
  - Tabla, flujo o lista si el contenido lo pide.
  - Caja `mnemo` y caja `error` ("no confundir") cuando aplique.
  - **Posibles preguntas del público** sobre ese punto con respuesta corta.
- Indicar arriba "Basado en **<material base>**".

### `flash.html` — FlashCards
- Igual que en el parcial (`var CARDS = [{cat, q, a}, …]`, giro, mezclar, difícil/aprendida,
  filtros, progreso en localStorage). `cat` = número y nombre del punto.
- Tipos de tarjeta: "¿Qué punto va después de X?", "¿Cuáles son las palabras clave de X?",
  definiciones, datos/cifras, ejemplos y preguntas probables del público. ~30–50 tarjetas.

### `ensayo.html` — Ensayo
- Cronómetro general con la duración objetivo; cada bloque muestra solo su **título** y su
  tiempo asignado.
- Flujo por bloque: decir el punto en voz alta → **Revelar** (aparecen viñetas y palabras clave)
  → marcar con casillas qué palabras clave sí dije → siguiente.
- El tiempo por bloque se colorea (verde dentro del tiempo, ámbar +20 %, rojo más).
- Resultado final: tiempo total vs. objetivo, % de palabras clave dichas por punto, puntos más
  débiles, historial de ensayos en localStorage, botón "🔄 Ensayar otra vez".

### `index.html` — Menú de la charla
Copiar `semestre2/gr/parcial1/index.html` tal cual (estilo, modo oscuro, botones ← y ⌂) y cambiar:
- `<title>Charla | <Tema></title>` y `<h1>` con el tema de la charla.
- Enlaces: volver = `../index.html`, inicio = `../../../index.html`.
- Botones en este orden: Guion, Palabras Clave, Resumen General, Resumen por Punto, FlashCards,
  Ensayo; luego `<div class="separator"></div>` y un botón por cada archivo del material
  (`<Nombre corto> (PDF)`).

## Verificación antes de terminar

- Cada página a ~412px de ancho: sin scroll horizontal, nada oculto (ver notas de emulación en
  `PROMPT-PARCIAL.md`). El modo escenario se lee bien con el teléfono a un brazo de distancia.
- Los puntos aparecen **en el mismo orden y con el mismo nombre** en todas las páginas.
- La suma de los tiempos del guion da la duración total.
- Cada palabra clave del ensayo existe en `claves.html` y en el guion.
- Todos los enlaces del índice apuntan a archivos existentes (ojo con tildes y espacios).
- Reportar qué material se usó, el reparto de tiempos y cualquier parte del material que se haya
  dejado fuera de la charla.
