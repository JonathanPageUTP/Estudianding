# Prompt: material para aprenderse una charla (modelo `semestre2/gr/parcial2`)

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

Usa como referencia de diseño semestre2/gr/parcial2 (incluida la carpeta audio/: copia
voz.js y los generadores) y semestre2/gpi/parcial3/como-estudiar.html. Todo el contenido
sale SOLO del material de la carpeta y de lo que te escribo aquí: no inventes datos.
```

---

## Qué hay que generar

Todo dentro de la carpeta de la charla, en archivos HTML **autocontenidos** (CSS y JS inline, sin
librerías externas, sin build), en español y **responsive** (mobile-first, pero bien adaptados a
tablet y PC).

| Archivo | Botón en el índice | Qué es |
|---|---|---|
| `como-estudiar.html` | Cómo Estudiar | Reglas y rutinas para ensayar según el lugar (🏢/🚌) y el tiempo disponible, con ejemplos de la charla |
| `guion.html` | Guion | El guion de la charla, punto por punto, con modos Oficina/Transporte y 🔊 Escuchar (MP3) |
| `claves.html` | Palabras Clave | Palabras y frases que no pueden faltar, por punto, con modo práctica |
| `tema.html` | Resumen Completo del Tema | **Todo** el contenido de la presentación (todas las láminas, de todos los expositores) completado con el trabajo escrito, para entender el tema entero, con 🔊 (MP3) |
| `resumen.html` | Resumen General | La charla completa en una sola pantalla: idea central + mapa de puntos, con 🔊 (MP3) |
| `puntos.html` | Resumen por Punto | Un resumen denso de cada punto específico, plegable, con 🔊 (MP3) |
| `flash.html` | FlashCards | Tarjetas con repetición espaciada hasta el día de la charla |
| `ensayo.html` | Ensayo | Modo práctica con cronómetro: decir cada punto de memoria y autoevaluarse |
| `dudas.html` | Mis Dudas | Mis preguntas mientras preparo la charla, explicadas corto y simple (empieza vacía) |
| `index.html` | — | Menú de la charla (ver abajo) |
| `audio/` | — | Reproductor compartido `voz.js`, generadores de MP3 y los MP3 de cada página (ver *Lectura en voz alta*) |

Además: si la materia aún no enlaza esta charla, agrega el botón en `<materia>/index.html`.

## Proceso

1. **Leer todo el material** de la carpeta completo (PDF, PPTX, transcripciones, notas).
   - PDF: `pdftotext -raw -enc UTF-8` (el modo `-layout` pierde fragmentos en diapositivas).
     Las láminas que salen vacías son **solo imagen** (diagramas, matrices, organigramas):
     renderizarlas (`pip install --user pypdfium2`) y mirarlas; ahí suele haber contenido.
   - PPTX: usar el skill de pptx; leer también las **notas del orador** si existen.
2. **Puntos específicos**: son el esqueleto de todo. Cada página sigue ese orden, numerado
   (`1 · PUNTO`, `2 · PUNTO`…), con una apertura (`0 · INTRO`) y un cierre (`FIN · CIERRE`).
   Si no los di, proponerlos a partir del material y confirmarlos antes de generar.
3. **Tiempo**: repartir la duración total entre intro, puntos y cierre (≈10 % intro, 80 % puntos,
   10 % cierre, ajustado al peso de cada punto). Ese reparto aparece en el guion y en el ensayo.
4. **Fidelidad**: usar la terminología del material. No agregar datos, cifras ni ejemplos que no
   estén en el material o en mi mensaje. Las mnemotecnias, frases de transición y preguntas de
   repaso (🎯, 🧠) sí son inventadas, pero deben codificar exactamente lo que dice el material.
5. Generar las páginas, luego el `index.html`, luego revisar (ver *Verificación*).
6. Generar los MP3 (`python audio/generar_paginas.py` y, si hay dudas, `python audio/generar_audio.py`)
   y commitearlos junto con los `audio/*.js`.
7. Commit por página o por bloque, con mensajes como los del historial:
   `Charla <SIGLA> <tema corto>: guion, palabras clave, resúmenes, flashcards y ensayo`.
   Las dudas van una por commit: `Dudas <SIGLA> charla<N>: #NN <tema>`.
8. Hacer push.

## Estilo visual común

Igual que en `PROMPT-PARCIAL.md` (secciones *Estilo visual común* y *Diseño responsive*): tema
oscuro con tokens en `:root`, viewport con `maximum-scale=5.0, viewport-fit=cover`, sin scroll
horizontal (tablas en `.tblwrap` con `overflow-x:auto` y sin `min-width` fijo), inputs a 16px,
botones ≥ 44px, `:hover` solo dentro de `@media (hover:hover)`, `:focus-visible`,
`env(safe-area-inset-*)` en barras fijas, `prefers-reduced-motion` y `localStorage` siempre en
`try/catch`. Si hay animaciones con `IntersectionObserver`, usar `threshold: 0` y respaldo por
scroll (en móvil los bloques largos nunca llegan al 10 % visible y quedan ocultos).
Claves con prefijo: `<sigla>_charla<N>_…_v1` (ej. `gpi_charla1_flash_v1`).

Breakpoints (detalle en `PROMPT-PARCIAL.md`): teléfono ≤ 560px una columna; tablet 561–1023px
columna de ~720px; PC ≥ 1024px contenedor de ~1100–1200px. En PC:
- `guion.html`, `puntos.html` y `tema.html`: índice de bloques como **barra lateral fija** a la izquierda.
- `claves.html`: items en 2 columnas.
- `flash.html` y `ensayo.html`: tarjeta / bloque centrado (máx. ~640px) con atajos de teclado.

## Modos de estudio (`guion.html`, `puntos.html` y `tema.html`)

La charla se practica en la oficina (laptop, se puede hablar en voz alta) y en el transporte
(celular con audífonos, sesiones cortas que se cortan en cada parada). Priorizar **recordar
activamente** (decirlo sin mirar) sobre releer.
- Interruptor **🏢 Oficina / 🚌 Transporte** (`<sigla>_charla<N>_modo_v1`; por defecto
  Transporte si el ancho es ≤ 560px, siempre cambiable a mano).
- **Transporte**: bloques plegados, aviso de una línea "Activa No Molestar · repasa en
  silencio o susurrando" y botón **▶ Continuar donde quedé** (`<sigla>_charla<N>_pos_v1`).
- **Oficina**: todo desplegado, aviso "Teléfono fuera de la vista · ensaya de pie y en voz alta"
  y temporizador opcional que sugiere una pausa cada 25–30 min.

## Lectura en voz alta con MP3 (`guion.html`, `puntos.html`, `tema.html`, `resumen.html` y `dudas.html`)

La voz del navegador (`speechSynthesis`) **se corta al apagar la pantalla del teléfono**. Por eso
cada página trae audio MP3 pregenerado, que sigue sonando con la pantalla apagada y en el bus.
Aplicar lo de `PROMPT-PARCIAL.md` (*Lectura en voz alta con MP3*), adaptado:

- **Reproductor compartido `audio/voz.js`** copiado del parcial, configurado con
  `Voz.init({sections, key, title, blocks, skip, target, onOpen, playerId, btnClass, allTarget,
  rateKey, artist})`. Cada página carga antes su manifiesto `<script src="audio/<pagina>.js">`
  (define `window.VOZ_AUDIO`) y luego `<script src="audio/voz.js">`.
  - Con MP3: lo reproduce con `<audio>` y **Media Session** (título y controles en la pantalla
    de bloqueo). Sin MP3: respaldo `speechSynthesis`. Sin ninguno: no se muestra el botón.
  - **🔊 Escuchar** por bloque (en el guion lee las viñetas de "Qué decir" y la **transición**)
    y sigue con los siguientes como un podcast; **🎧 Escuchar toda la charla** en la barra.
  - Reproductor fijo con botones **solo de icono** (⏮ ⏸/▶ ⏭ ⏹) con `aria-label`; velocidad de
    0.8× a 1.3× en `<sigla>_charla<N>_tts_rate_v1`; en ≤ 430px se oculta el título.
  - Resalta el bloque que se oye con los tiempos del manifiesto y abre el bloque si estaba plegado.
  - Respaldo `speechSynthesis`: **no usar `pause()`/`resume()`** (en Chrome de Android no
    reanuda). Pausar = `cancel()` recordando el párrafo; reanudar = volver a leer ese párrafo;
    ignorar el `onend`/`onerror` de la frase cancelada (contador de generación).
- **Generar los MP3**: `python audio/generar_paginas.py [guion|puntos|resumen|tema]` con
  `PAGES = ["guion", "puntos", "resumen", "tema"]` (`pip install edge-tts playwright`, usa el Edge
  instalado). Pide a `Voz.dump()` los textos exactos, sintetiza con la voz neural
  **`es-PA-MargaritaNeural`**, crea `audio/<pagina>/<bloque>.mp3` (clave = `id` del bloque) y
  `audio/<pagina>.js` con `{src, t, h}`; solo regenera los bloques cuyo texto cambió.
  **Cada vez que se edite el texto de una de esas páginas, volver a correr el script y
  commitear los MP3 y el `.js`.**
- `dudas.html` usa su propio reproductor y `audio/generar_audio.py` (crea `audio/dudaNN.mp3` y
  `audio/dudas.js`), con 🎧 Escuchar todas.
- Lo que se lee debe sonar bien: sin emojis, símbolos (→, ↔, ≥, ≠, ×, %, ·, =, /) dichos en
  palabras, siglas expandidas la primera vez en cada bloque (diccionario `EXPAND` en `voz.js` y
  en `generar_audio.py`: ampliarlo con las siglas de la charla) y `data-tts` cuando el texto
  visible tenga símbolos raros.

## Detalle de cada página

### `como-estudiar.html` — Cómo estudiar la charla
Partir de `semestre2/gpi/parcial3/como-estudiar.html` (mismo estilo, header con ← y chips de
secciones) y adaptarlo a preparar una exposición:
- **⏱️ Elige tu sesión**: selector 🚌 Transporte / 🏢 Oficina × 5 / 15 / 30 / 60–90 min que muestra
  una rutina paso a paso con tiempos, un **ejemplo con un punto de esta charla** y un consejo
  (guardado en `<sigla>_charla<N>_metodo_sel_v1`). Ej.: 🚌 5 min = 🎧 escuchar un bloque y decir
  mentalmente la transición; 🏢 30 min = ensayo cronometrado completo + repasar los 2 puntos más débiles.
- **Reglas** (8–10) con ejemplo de la charla: decir antes de leer, ensayar en voz alta de pie,
  aprender el orden y las transiciones antes que los detalles, no memorizar palabra por palabra
  sino las palabras clave, grabarse y escucharse, ensayar con el tiempo real, repaso espaciado.
- **🏢 Oficina vs. 🚌 Transporte**, tabla **para qué sirve cada página**, técnicas (palacio de la
  memoria con los puntos, explicarlo a alguien, hoja en blanco con el mapa, anticipar preguntas
  del público), **plan hasta la charla**, **lo que debes evitar** y **✅ checklist de hoy**
  (`<sigla>_charla<N>_metodo_check_v1`, se reinicia cada día, con barra de progreso).

### `guion.html` — Guion
- Header fijo "Guion · <Tema>" con duración total, barra de progreso de lectura e interruptor 🏢/🚌.
- Una tarjeta por bloque (`0 · Intro`, `1 · …`, …, `Cierre`), cada una con:
  - **🎯 Antes de leer**: 1–2 preguntas ("¿qué dato respalda este punto?") con la respuesta en
    `<details>`, con la indicación "Intenta responder aunque no sepas".
  - **Tiempo** asignado (`⏱ 1:30`) y tiempo acumulado (`→ 3:00`).
  - **Objetivo** del punto en una línea ("Que entiendan que…").
  - **Qué decir**: 3–6 viñetas cortas en orden, no párrafos para leer.
  - **Palabras clave** del punto como chips resaltados.
  - **Dato / ejemplo** que lo respalda (con la fuente: lámina o página del material).
  - **Transición** al siguiente punto: una frase lista para decir ("Ahora que sabemos X, veamos Y").
  - Si hay lámina asociada: "🖼 Lámina <n>".
  - En Transporte, bloques largos partidos con "🚏 Pausa segura: si llegas a tu parada, retoma aquí".
- Botón **🎤 Modo escenario**: letra grande, solo viñetas y palabras clave, pantalla siempre
  encendida si el navegador lo permite (`navigator.wakeLock` dentro de `try/catch`), se pasa de
  bloque tocando la mitad derecha/izquierda.
- Si es en grupo: marcar con color qué bloques son míos y quién habla antes/después.
- Al final de cada bloque, **🧠 Recuerda sin mirar**: 2–3 preguntas (qué viene después, palabras
  clave, el dato del punto) con la respuesta dentro de `<details>`, nunca visible junto a la pregunta.
- Cierre del guion: **🔀 Repaso mezclado** (5–8 preguntas sin seguir el orden), **✍️ Dilo en 3
  frases** (la charla completa) y **frase de arranque editable** ("Cuando me siente en el bus /
  llegue a la oficina, abro ▶ Continuar y digo la transición del último punto").

### `claves.html` — Palabras clave
- Agrupadas por punto, con chips de anclas arriba.
- Cada item, mismo formato que `siglas-titulos.html` del parcial:
  ```html
  <div class="s"><span class="k">PIRA</span><div class="b">
    <div class="tt">Estrategias de respuesta al riesgo</div>
    <div class="x"><b>P</b>revenir · <b>I</b>mpacto reducido · <b>R</b>edistribuir · <b>A</b>ceptar</div>
    <div class="m">"Pira" = fogata: hay que apagar el riesgo</div>
  </div></div>
  ```
  `k` = término clave o sigla, `tt` = punto de la charla, `x` = definición corta / expansión,
  `m` = mnemotecnia o frase para recordarlo. Variantes de color `a`/`c`/`v` para números/listas,
  contrastes y pares.
- Botón **🙈 Modo práctica** (oculta las definiciones; tocar revela).
- Al final: **SECUENCIA DE LA CHARLA** (una sigla/frase que codifica el orden de todos los
  puntos), **NÚMEROS Y DATOS CLAVE** y **NO CONFUNDIR**.

### `resumen.html` — Resumen general
- Cabe idealmente en una o dos pantallas del celular. Es solo un vistazo: **no sustituye** a
  `tema.html`, que es donde se explica todo el tema (enlazarlo desde "parte por parte").
- **Idea central** en una frase grande (lo que el público debe recordar).
- **La presentación, parte por parte**: un resumen corto (2–3 viñetas) de **cada parte del PPT**,
  en su orden, con el expositor y las láminas de cada una; mi parte resaltada. Así sé qué dicen
  los demás y puedo enlazar con ellos. Las láminas que son solo imagen hay que renderizarlas y leerlas.
- **Mapa de la charla**: flujo vertical con los puntos numerados, cada uno con su frase-resumen
  de una línea y su tiempo.
- **Mensaje de cierre** / llamado a la acción.
- Resumen del contenido general en 5–8 viñetas.
- 🔊 por sección y 🎧 Escuchar todo con MP3 (manifiesto `audio/resumen.js`).
- **📅 Plan de repaso** si hay fecha de la charla (`<sigla>_charla<N>_fecha_v1`, editable en la
  página): hoy leer el guion, +1 día escuchar 🎧 y flashcards, +3 días primer ensayo
  cronometrado, día anterior ensayo completo + modo escenario. Si la fecha está cerca, comprimir
  sin pasar del día anterior.

### `tema.html` — Resumen completo del tema
Mi parte es solo un trozo de la exposición: para responder preguntas y enlazar con los demás
necesito **entender todo el tema**, no solo mis láminas. Esta página resume **todo el contenido
de la presentación** (todas las láminas, de todos los expositores), en el orden del PPT y
completado con el trabajo escrito donde la lámina se queda corta.
- Misma estructura que `puntos.html` (buscador, chips, barra lateral en PC, **Plegar todo**,
  🏢/🚌, pausas 🚏, ▶ Continuar donde quedé con `<sigla>_charla<N>_tema_pos_v1`).
- Primera sección **★ Todo el tema en 1 minuto**: la idea general en 6–8 viñetas (qué es, sus
  vías o regímenes, requisitos, cifras y plazos clave, la idea ética o de cierre del grupo) y una
  tabla **Quién expone qué** (láminas · expositor · tema).
- Luego **una sección por tema del PPT** (no por expositor: si alguien tiene 4 láminas de temas
  distintos, van separadas), cada una con: `🎤 expositor · 🖥️ diap. X–Y · 📄 sección del trabajo`,
  viñetas densas con **todo** lo que dice la lámina (no 2–3 viñetas), definiciones textuales en
  `blockquote`, **las tablas de la lámina como tablas** (líneas de tiempo, comparativas, plazos,
  cálculos de casos paso a paso), caja `mnemo`, caja `error` y, si el material tiene cuestionario,
  la pregunta que corresponde a esa sección con su respuesta en `<details>`.
- Mis secciones van **resaltadas** (borde de acento y etiqueta "TU PARTE") y en versión corta, con
  enlace a `puntos.html` para el detalle.
- Termina con conclusiones y recomendaciones del grupo.
- 🔊 por sección y 🎧 Escuchar todo con MP3 (manifiesto `audio/tema.js`).
- Las láminas que son solo imagen se renderizan y se leen: también van aquí.

### `puntos.html` — Resumen por punto
- Buscador (con mensaje "😶 Sin resultados"), chips de navegación, botón **Plegar todo** e
  interruptor 🏢/🚌.
- Una sección plegable por punto (`1 Qué es un riesgo ▾`) con:
  - Resumen denso en viñetas (lo que dice el material sobre ese punto, completo).
  - Definiciones textuales en `<blockquote class="q">` cuando el material las tenga.
  - Tabla, flujo o lista si el contenido lo pide.
  - Caja `mnemo` y caja `error` ("no confundir") cuando aplique.
  - **Posibles preguntas del público** sobre ese punto con respuesta corta.
- 🔊 por punto y 🎧 Escuchar todo con MP3 (manifiesto `audio/puntos.js`).
- Indicar arriba "Basado en **<material base>**".

### `flash.html` — FlashCards
- Igual que en el parcial (`var CARDS = [{cat, q, a}, …]`, giro, mezclar, difícil/aprendida,
  contador "X de Y", estado vacío, progreso en localStorage). `cat` = número y nombre del punto.
- **Repetición espaciada** como en el parcial: "Aprendida" 1 → 3 → 7 → 14 días, "Difícil" vuelve
  a 1 día y reaparece al final de la sesión; pestañas **📅 Hoy · N** (por defecto), Todas, Por
  repasar, Aprendidas. Con fecha de la charla, nada se programa después del día anterior.
- Filtro por punto (`flash.html#cat-<slug>`), botón **⬇️ Exportar a Anki** (TSV) y atajos de
  teclado en PC (← → navegar, espacio girar, 1 difícil, 2 aprendida).
- **En el teléfono todo cabe en una pantalla, sin scroll**: `height:100vh; height:100svh`
  (`vh`/`dvh` dejan los botones por fuera en Android), `html,body{overflow:hidden}`, columna flex
  donde **solo la tarjeta se encoge** (`min-height` ~150px, la respuesta larga se desplaza dentro),
  encabezado sin subtítulo y fecha + exportar detrás de un botón **⚙️**.
- Tipos de tarjeta: "¿Qué punto va después de X?", "¿Cuáles son las palabras clave de X?",
  "¿Con qué frase paso de X a Y?", definiciones, datos/cifras, ejemplos y preguntas probables
  del público. ~30–50 tarjetas.

### `ensayo.html` — Ensayo
- Cronómetro general con la duración objetivo; cada bloque muestra solo su **título** y su
  tiempo asignado.
- Flujo por bloque: decir el punto en voz alta → **Revelar** (aparecen viñetas y palabras clave)
  → marcar con casillas qué palabras clave sí dije → siguiente. La revelación queda bloqueada:
  no se puede volver a ocultar para "repetir" el mismo bloque sin dejarlo registrado.
- Marcador en vivo en el header: % de palabras clave dichas hasta ahora.
- El tiempo por bloque se colorea (verde dentro del tiempo, ámbar +20 %, rojo más).
- El estado del ensayo en curso se guarda (`<sigla>_charla<N>_ensayo_v1`) para sobrevivir a una
  recarga, con aviso "⏸️ Tienes un ensayo en curso" con Continuar / Descartar.
- Resultado final: tiempo total vs. objetivo, % de palabras clave dichas por punto, puntos más
  débiles, historial de ensayos en localStorage (`_hist_v1`), botón "🔄 Ensayar otra vez".
- En cada punto débil del resultado, enlaces rápidos "📜 Ver en el guion" y "🃏 Tarjetas del punto"
  (`flash.html#cat-<slug>`).
- Opciones: **⚡ Ensayo rápido** (solo los puntos débiles del último ensayo) y **🚌 Ensayo
  mental** para el transporte (sin cronómetro por bloque: se repasa en silencio y se marca igual;
  en el historial se etiqueta "🚌 mental" para distinguirlo del ensayo en voz alta).
- **En el teléfono todo cabe en una pantalla**, sin scroll (`100svh`): cronómetro, bloque actual y
  botones Revelar / Siguiente siempre visibles, porque se ensaya de pie con el teléfono en la mano.
  Si se puede, pantalla siempre encendida (`navigator.wakeLock` en `try/catch`).

### `dudas.html` — Mis dudas
- Copiar `semestre2/gr/parcial2/dudas.html` (estilo blanco/negro del índice, modo oscuro con
  luna/sol, botones ← y ⌂). Título "Mis Dudas" y subtítulo "Preguntas que surgieron preparando
  la charla · <Tema>".
- Se crea **vacía**, con estado vacío, plantilla comentada (`<details class="qa">` con número,
  pregunta, tema, respuesta y cajas "Para memorizar" / "Ojo al exponer") y buscador que se oculta
  si no hay dudas. `audio/dudas.js` empieza como `window.DUDAS_AUDIO = {};`.
- Cuando pida explicar una duda: **corto y simple**, legible en menos de un minuto: la idea en
  una frase, una analogía concreta, 3–5 viñetas o una tabla pequeña, una mnemotecnia y cómo
  decirlo en la charla. Todo fiel al material.
- 🔊 por duda y 🎧 Escuchar todas, con MP3 (`python audio/generar_audio.py` tras cada duda).

### `index.html` — Menú de la charla
Copiar `semestre2/gr/parcial2/index.html` tal cual (estilo, modo oscuro, botones ← y ⌂),
asegurando que cumpla *Diseño responsive*, y cambiar:
- `<title>Charla | <Tema></title>` y `<h1>` con el tema de la charla.
- Enlaces: volver = `../index.html`, inicio = `../../../index.html`.
- Botones en este orden: Cómo Estudiar, Guion, Palabras Clave, Resumen Completo del Tema,
  Resumen General, Resumen por
  Punto, FlashCards, Ensayo, Mis Dudas; luego `<div class="separator"></div>` y un botón por cada
  archivo del material (`<Nombre corto> (PDF)`).

## Verificación antes de terminar

- Cada página en **412px**, **768px** y **1366px** (Playwright con el Edge instalado,
  `channel='msedge'` y `viewport`; o `Emulation.setDeviceMetricsOverride`, porque Chrome headless
  no baja de 500px con `--window-size`): sin scroll horizontal, nada oculto ni cortado, ningún
  error JS en consola; en PC la barra lateral del guion, de los puntos y del tema se ve (comprobar con
  `getComputedStyle`, no con `offsetParent`, que es `null` en elementos `fixed`). El modo
  escenario se lee bien con el teléfono a un brazo de distancia.
- `flash.html` y `ensayo.html` en el teléfono (412×740, 412×600 y 360×560, con la tarjeta girada /
  el bloque revelado): sin scroll de página y con los botones de abajo completos.
- Modos 🏢/🚌, pausas 🚏 y "Continuar donde quedé" funcionan; ninguna respuesta de 🎯/🧠 se ve
  sin tocarla.
- Audio: cada bloque del guion, los puntos, el tema y el resumen tiene su MP3 (el script muestra
  "N bloques, X min" por página). Al tocar 🔊 suena el MP3, se resalta el bloque correcto, ⏮/⏭
  cambian de bloque, sigue con la pantalla apagada y aparecen los controles en la pantalla de
  bloqueo. Sin MP3, la voz del navegador pausa y reanuda. Los MP3 y `audio/*.js` están commiteados.
- `como-estudiar.html`: las 8 combinaciones lugar × tiempo muestran su rutina y el checklist se
  guarda y se reinicia al día siguiente.
- Flashcards: la pestaña "Hoy" respeta las fechas, y el filtro `#cat-…` y el TSV funcionan.
- Ensayo: un ensayo completo, uno rápido y uno mental se terminan sin errores; el estado
  sobrevive a una recarga y el historial los distingue.
- Los puntos aparecen **en el mismo orden y con el mismo nombre** en todas las páginas.
- La suma de los tiempos del guion da la duración total.
- Cada palabra clave del ensayo existe en `claves.html` y en el guion.
- Todos los enlaces del índice apuntan a archivos existentes (ojo con tildes y espacios).
- Reportar qué material se usó, el reparto de tiempos y cualquier parte del material que se haya
  dejado fuera de la charla.
