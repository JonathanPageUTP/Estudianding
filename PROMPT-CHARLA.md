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
- Fecha:          <dd/mm/aaaa>             (opcional: para el plan de repaso y las flashcards)
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
librerías externas, sin build), en español y **responsive** (mobile-first, pero bien adaptados a
tablet y PC).

| Archivo | Botón en el índice | Qué es |
|---|---|---|
| `guion.html` | Guion | El guion de la charla, punto por punto, con modos Oficina/Transporte y 🔊 Escuchar |
| `claves.html` | Palabras Clave | Palabras y frases que no pueden faltar, por punto, con modo práctica |
| `resumen.html` | Resumen General | La charla completa en una sola pantalla: idea central + mapa de puntos |
| `puntos.html` | Resumen por Punto | Un resumen denso de cada punto específico, plegable |
| `flash.html` | FlashCards | Tarjetas con repetición espaciada hasta el día de la charla |
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
6. Commit por página o por bloque, con mensajes como los del historial:
   `Charla <SIGLA> <tema corto>: guion, palabras clave, resúmenes, flashcards y ensayo`.
7. Hacer push.

## Estilo visual común

Igual que en `PROMPT-PARCIAL.md` (secciones *Estilo visual común* y *Diseño responsive*): tema
oscuro con tokens en `:root`, viewport con `maximum-scale=5.0, viewport-fit=cover`, sin scroll
horizontal, inputs a 16px, botones ≥ 44px, `:hover` solo dentro de `@media (hover:hover)`,
`:focus-visible`, `prefers-reduced-motion` y `localStorage` siempre en `try/catch`.
Claves con prefijo: `<sigla>_charla<N>_…_v1` (ej. `gpi_charla1_flash_v1`).

Breakpoints (detalle en `PROMPT-PARCIAL.md`): teléfono ≤ 560px una columna; tablet 561–1023px
columna de ~720px; PC ≥ 1024px contenedor de ~1100–1200px. En PC:
- `guion.html` y `puntos.html`: índice de bloques como **barra lateral fija** a la izquierda.
- `claves.html`: items en 2 columnas.
- `flash.html` y `ensayo.html`: tarjeta / bloque centrado (máx. ~640px) con atajos de teclado.

## Modos de estudio y lectura en voz alta (`guion.html` y `puntos.html`)

La charla se practica en la oficina (laptop) y en el transporte (celular con audífonos). Aplicar lo
de `PROMPT-PARCIAL.md` (*Selector de modo* y *Lectura en voz alta*), adaptado:
- Interruptor **🏢 Oficina / 🚌 Transporte** (`<sigla>_charla<N>_modo_v1`; por defecto
  Transporte si el ancho es ≤ 560px). En Transporte: bloques plegados, aviso "Activa No Molestar"
  y botón **▶ Continuar donde quedé** (`<sigla>_charla<N>_pos_v1`). En Oficina: todo desplegado.
- Botón **🔊 Escuchar** por bloque con `speechSynthesis` (voz `es-*`, 0.9×–1.3×), que lee las
  viñetas de "Qué decir" y la **transición**, resaltando lo que se lee, más un **🔊 Escuchar toda
  la charla** que recorre los bloques en orden. Sin emojis; símbolos dichos en palabras; siglas
  expandidas la primera vez.
- Reproductor con botones **solo de icono** (⏸ / ▶ / ⏹). **No usar `pause()`/`resume()`**: en
  Chrome de Android reanudar no funciona; pausar = `cancel()` recordando el párrafo actual y
  reanudar = volver a leer ese párrafo (ver `PROMPT-PARCIAL.md`).

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
- Al final de cada bloque, **🧠 Recuerda sin mirar**: 2–3 preguntas (qué viene después, palabras
  clave, el dato del punto) con la respuesta dentro de `<details>`, nunca visible junto a la pregunta.

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
- **La presentación, parte por parte**: un resumen corto (2–3 viñetas) de **cada parte del PPT**,
  en su orden, con el expositor y las láminas de cada una; mi parte resaltada. Así sé qué dicen
  los demás y puedo enlazar con ellos. Las láminas que son solo imagen hay que renderizarlas y leerlas.
- **Mapa de la charla**: flujo vertical con los puntos numerados, cada uno con su frase-resumen
  de una línea y su tiempo.
- **Mensaje de cierre** / llamado a la acción.
- Resumen del contenido general en 5–8 viñetas.
- **📅 Plan de repaso** si hay fecha de la charla (`<sigla>_charla<N>_fecha_v1`, editable en la
  página): hoy leer el guion, +1 día escuchar 🔊 y flashcards, +3 días primer ensayo
  cronometrado, día anterior ensayo completo + modo escenario. Si la fecha está cerca, comprimir
  sin pasar del día anterior.

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
  progreso en localStorage). `cat` = número y nombre del punto.
- **Repetición espaciada** como en el parcial: "Aprendida" 1 → 3 → 7 → 14 días, "Difícil" vuelve
  a 1 día y reaparece al final de la sesión; pestañas **📅 Hoy · N** (por defecto), Todas, Por
  repasar, Aprendidas. Con fecha de la charla, nada se programa después del día anterior.
- Filtro por punto (`flash.html#cat-<slug>`), botón **⬇️ Exportar a Anki** (TSV) y atajos de
  teclado en PC (← → navegar, espacio girar, 1 difícil, 2 aprendida).
- **En el teléfono todo cabe en una pantalla, sin scroll**: `height:100svh`, solo la tarjeta se
  encoge, opciones secundarias detrás de un botón ⚙️ (ver `PROMPT-PARCIAL.md`).
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
- En cada punto débil del resultado, enlaces rápidos "📜 Ver en el guion" y "🃏 Tarjetas del punto"
  (`flash.html#cat-<slug>`).
- Opción **⚡ Ensayo rápido**: solo los puntos marcados como débiles en el último ensayo.
- **En el teléfono todo cabe en una pantalla**, sin scroll (`100svh`): cronómetro, bloque actual y
  botones Revelar / Siguiente siempre visibles, porque se ensaya de pie con el teléfono en la mano.
  Si se puede, pantalla siempre encendida (`navigator.wakeLock` en `try/catch`).

### `index.html` — Menú de la charla
Copiar `semestre2/gr/parcial1/index.html` tal cual (estilo, modo oscuro, botones ← y ⌂),
asegurando que cumpla *Diseño responsive*, y cambiar:
- `<title>Charla | <Tema></title>` y `<h1>` con el tema de la charla.
- Enlaces: volver = `../index.html`, inicio = `../../../index.html`.
- Botones en este orden: Guion, Palabras Clave, Resumen General, Resumen por Punto, FlashCards,
  Ensayo; luego `<div class="separator"></div>` y un botón por cada archivo del material
  (`<Nombre corto> (PDF)`).

## Verificación antes de terminar

- Cada página en **412px**, **768px** y **1366px** (emular con `Emulation.setDeviceMetricsOverride`,
  ver `PROMPT-PARCIAL.md`): sin scroll horizontal, nada oculto ni cortado; en PC la barra lateral
  del guion y de los puntos se ve y funciona. El modo escenario se lee bien con el teléfono a un
  brazo de distancia.
- `flash.html` y `ensayo.html` en el teléfono (412×740, 412×600 y 360×560): sin scroll de página
  y con los botones de abajo completos.
- Modos 🏢/🚌 y "Continuar donde quedé" funcionan; 🔊 lee en español los bloques en orden, pausa y
  reanuda (también en el teléfono) y se oculta si no hay `speechSynthesis`.
- Flashcards: la pestaña "Hoy" respeta las fechas, y el filtro `#cat-…` y el TSV funcionan.
- Los puntos aparecen **en el mismo orden y con el mismo nombre** en todas las páginas.
- La suma de los tiempos del guion da la duración total.
- Cada palabra clave del ensayo existe en `claves.html` y en el guion.
- Todos los enlaces del índice apuntan a archivos existentes (ojo con tildes y espacios).
- Reportar qué material se usó, el reparto de tiempos y cualquier parte del material que se haya
  dejado fuera de la charla.
