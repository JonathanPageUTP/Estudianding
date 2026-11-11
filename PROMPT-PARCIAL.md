# Prompt: material de estudio de un parcial (modelo `semestre2/gr/parcial1`)

Copia el bloque de abajo, cambia los valores entre `<…>` y pégalo en Claude Code.
Ejemplo: `Aplica PROMPT-PARCIAL.md a semestre2/gr/parcial2, materia "Gerencia de Recursos de TIC", sigla GR, parcial 2`.

---

```text
Lee PROMPT-PARCIAL.md y aplícalo a:

- Carpeta:      <semestre2/gr/parcial2>
- Materia:      <Gerencia de Recursos de TIC>
- Sigla corta:  <GR>                      (para títulos y claves de localStorage)
- Parcial:      <2>
- Profesor:     <Ing. Nombre Apellido>    (opcional, para la portada del simulacro)
- Periodo:      <II Semestre 2026>
- Fecha del examen: <dd/mm/aaaa>          (opcional, para el plan de repaso espaciado)
- PDF principal (define el orden): <nombre del PDF>   (si no lo indico, elige el más completo y dímelo)

Usa como referencia de diseño y estructura semestre2/gr/parcial1. Todo el contenido
sale SOLO de los PDF que están en la carpeta: no inventes datos.
```

---

## Qué hay que generar

Todo dentro de la carpeta del parcial, en archivos HTML **autocontenidos** (CSS y JS inline, sin
librerías externas, sin build), en español y **responsive** (mobile-first, pero bien adaptados a
tablet y PC).

| Archivo | Botón en el índice | Qué es |
|---|---|---|
| `guia.html` | Guia | Guía de estudio completa, por temas, con aprendizaje activo y modos Oficina/Transporte |
| `flash.html` | FlashCards | Tarjetas pregunta/respuesta con repetición espaciada y progreso guardado |
| `resumen.html` | Resumen | Cheat sheet mnemotécnico con buscador |
| `resumen-express.html` | Resumen Express | Todo el PDF principal, en su orden, lo más corto posible |
| `siglas.html` | Siglas y Mnemotecnias | Siglas inventadas + mnemotecnias, con modo práctica |
| `siglas-titulos.html` | Siglas con Títulos | Igual que `siglas.html` + el título del PDF de cada sigla |
| `parcial.html` | Simulacro de Parcial | Examen simulado de 100 puntos (y mini simulacro) con temporizador, calificación y verificación inmediata opcional |
| `index.html` | — | Menú del parcial (ver abajo) |

Además: si la materia aún no enlaza este parcial, agrega el botón en `<materia>/index.html`.

## Proceso

1. **Leer todos los PDF** de la carpeta completos (usa el skill de PDF si hace falta). Anotar
   temas, definiciones, listas, pasos, números clave, siglas oficiales y cosas fáciles de confundir.
   - Texto: `pdftotext -raw -enc UTF-8` (el modo `-layout` pierde fragmentos en diapositivas).
   - Muchas láminas son **solo imagen** (diagramas, organigramas, matrices): las páginas que salen
     vacías hay que renderizarlas (`pip install --user pypdfium2`) y mirarlas; ahí suele haber
     contenido preguntable.
2. **Orden**: todas las páginas siguen el orden del PDF principal, agrupadas por unidad con una
   etiqueta tipo `UNIDAD I · …` y secciones numeradas (`1 · TEMA`, `2 · TEMA`…). Indicar en la
   página "Orden según **<PDF principal>**". Si no hay un PDF "general" (todos son temas sueltos),
   ordenar por PDF/tema, usar etiquetas `TEMA 1 · …` y decir el orden elegido.
3. **Fidelidad**: usar la terminología del material. No agregar contenido que no esté en los PDF.
   Las mnemotecnias sí son inventadas, pero deben codificar exactamente lo que dice el PDF. Las
   preguntas de aprendizaje activo (🎯, 🤔, 🧠, repaso mezclado) y sus respuestas también salen
   solo de los PDF.
4. Generar las páginas, luego el `index.html`, luego revisar (ver *Verificación*).
5. Commit por página o por bloque, con mensajes como los del historial:
   `Parcial <N> <SIGLA>: guía, flashcards, resúmenes, siglas y simulacro`.
6. Hacer push.

## Estilo visual común (páginas de estudio)

- Tema oscuro propio de cada página con tokens en `:root` (`--bg`, `--surface`, `--line`,
  `--text`, `--text-dim`, `--accent` verde, `--cyan`, `--amber`, `--red`, `--violet` y sus `-dim`),
  fondo con cuadrícula sutil, fuente del sistema (`--sans`) y monoespaciada (`--mono`) para siglas.
- `<html lang="es">`, `<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, viewport-fit=cover">`.
- Todo acceso a `localStorage` dentro de `try/catch`. Claves con prefijo de la materia y versión:
  `<sigla>_flashcards_status_v2`, `<sigla>_parcial_sim_v1`, `<sigla>_parcial_hist_v1`, etc.
  (si ya existe un parcial anterior de la misma materia, incluir el número: `gr_p2_…`).
- Si se usan animaciones al hacer scroll con `IntersectionObserver`, usar `threshold: 0` y un
  respaldo por scroll; en móvil las secciones largas nunca llegan al 10% visible y quedan ocultas.

### Diseño responsive (obligatorio en todas las páginas, incluido `index.html`)

Mobile-first, pero cada página debe verse bien y aprovechar el espacio en teléfono, tablet y PC.

- Layout fluido con unidades relativas (`rem`, `%`, `clamp()`), flexbox o grid; nunca anchos fijos
  en px para contenedores. Imágenes y SVG con `max-width: 100%; height: auto`.
- Tipografía fluida: `font-size: clamp(15px, 1rem + 0.2vw, 18px)` en el cuerpo y títulos con
  `clamp()`. Largo de línea legible: máx. ~70 caracteres (`max-width: 70ch`) en párrafos.
- Nada de scroll horizontal en ningún tamaño: tablas dentro de `.tblwrap` con `overflow-x: auto`,
  código y textos largos con `overflow-wrap: anywhere`.
- Breakpoints:
  - **Teléfono (≤ 560px)**: una columna, gutter de 16px, header compacto, pasos en vertical,
    barra de navegación inferior fija, inputs a 16px para que iOS no haga zoom, botones ≥ 44px.
  - **Tablet (561–1023px)**: una columna centrada de `max-width ≈ 720px`; tarjetas en grid de
    2 columnas; pasos en horizontal si caben.
  - **PC (≥ 1024px)**: contenedor de `max-width ≈ 1100–1200px`.
    - `guia.html` y `resumen.html`: índice/TOC como **barra lateral fija** (sticky) a la
      izquierda y contenido a la derecha; la barra inferior móvil se oculta.
    - Tarjetas en grid de 2–3 columnas (`repeat(auto-fit, minmax(280px, 1fr))`).
    - `flash.html`: tarjeta centrada más grande (máx. ~640px) y atajos de teclado
      (← → anterior/siguiente, espacio para girar, 1 = difícil, 2 = aprendida).
    - `parcial.html`: preguntas en una columna de ~800px, con temporizador y contador de
      respondidas fijos en un panel lateral o en el header.
    - `siglas.html` y `siglas-titulos.html`: items en grid de 2 columnas.
- Interacción para ambos: todo lo que se toca también funciona con mouse y teclado; estados
  `:hover` solo dentro de `@media (hover: hover)`; foco visible (`:focus-visible`) en botones
  y enlaces.
- Respetar el área segura del teléfono: `env(safe-area-inset-*)` en el header y la barra
  inferior fijos.
- Respetar `prefers-reduced-motion`: sin animaciones si el sistema lo pide.

## Técnicas de aprendizaje activo y modos de estudio

Estudio a veces en la oficina (laptop, sesiones de 25–50 min) y a veces en transporte público
(celular, audífonos, sesiones de 10–25 min que se cortan en cada parada). Las páginas deben servir
para ambos casos y priorizar **recordar activamente** sobre releer.

### Selector de modo (`guia.html` y `resumen-express.html`)

- Interruptor en el header **🏢 Oficina / 🚌 Transporte**, guardado en `<sigla>_modo_v1`.
  Por defecto: Transporte si el ancho es ≤ 560px, Oficina si no. Siempre se puede cambiar a mano.
- **Transporte**:
  - Cada tema se parte en bloques de ~400–700 palabras (5–7 min) con la marca
    "🚏 Pausa segura: si llegas a tu parada, retoma aquí".
  - Tablas grandes y acordeones de detalle plegados por defecto.
  - Botón **▶ Continuar donde quedé**, que guarda el último bloque visto en `<sigla>_guia_pos_v1`.
  - Aviso de una línea al abrir: "Activa No Molestar · música instrumental o silencio, nada con letra".
- **Oficina**:
  - Todo desplegado, con tablas y diagramas completos.
  - Las preguntas de "¿Por qué?" y "Explícalo" traen un `<textarea>` para responder por escrito.
  - Aviso de una línea: "Teléfono fuera de la vista y notificaciones en silencio".
  - Temporizador opcional que sugiere una pausa cada 25–30 min.

### Lectura en voz alta (`guia.html` y `resumen-express.html`)

- Botón **🔊 Escuchar** por sección usando `speechSynthesis`:
  - Voz `es-*`, velocidad ajustable de 0.9× a 1.3×, pausar y reanudar.
  - Botones del reproductor **solo con icono** (⏸ / ▶ y ⏹), con `aria-label` para accesibilidad.
  - **No usar `speechSynthesis.pause()` / `resume()`**: en Chrome de Android el reanudar no
    funciona. Pausar = `speechSynthesis.cancel()` recordando el párrafo actual (que queda
    resaltado); reanudar = volver a leer ese mismo párrafo y seguir. Ignorar el `onend`/`onerror`
    de la frase cancelada (contador de generación) para que no salte al siguiente párrafo.
  - Resalta el párrafo que se está leyendo.
  - Si el navegador no tiene `speechSynthesis`, ocultar el botón.
- Lo que se lee debe sonar bien: sin emojis, y los símbolos (→, ≥, ≠, ·) dichos en palabras.
  Las siglas se expanden la primera vez. Cuando el texto visible tenga símbolos, poner la
  versión hablada en `data-tts`.

### Aprendizaje activo en `guia.html`

Cada `<section class="topic">` agrega, en este orden:
1. **🎯 Antes de leer**: 2–3 preguntas concretas (factuales) sobre lo que viene, con la
   indicación "Intenta responder aunque no sepas".
2. El contenido del tema.
3. **🤔 ¿Por qué?**: una pregunta que obligue a explicar por qué algo es así o cómo se conecta
   con otro tema del parcial.
4. **🧠 Recuerda sin mirar**: 3 preguntas de recuperación.

Todas las respuestas van dentro de `<details>`, nunca visibles junto a la pregunta, y salen del PDF.

Cierre de la guía, antes del mapa mental:
- **🔀 Repaso mezclado**: 8–10 preguntas que combinen temas distintos, sin seguir el orden.
- **✍️ Explícalo en 3 frases**: autoexplicación del parcial completo.
- **📅 Plan de repaso espaciado**:
  - Toma la fecha del examen del input o de un campo en la página (`<sigla>_examen_v1`).
  - Fechas: lectura (hoy), +1 día, +3 días, +7 días, simulacro a 2 días del examen y
    siglas + "No confundir" el día anterior.
  - Si el examen está cerca, comprimir las fechas sin pasar del día anterior al examen.
- **Frase de arranque editable**: "Cuando me siente en el bus / llegue a la oficina, abro
  ▶ Continuar y respondo las preguntas de 🎯".

## Detalle de cada página

### `guia.html` — Guía de estudio
- Barra de progreso de lectura arriba, header fijo con título, **buscador** que resalta y
  filtra, e interruptor de modo 🏢/🚌. Hero con "Todo el material del Parcial <N>, organizado
  para memorizar rápido".
- Índice (overlay TOC en teléfono/tablet, barra lateral en PC) y **barra de navegación inferior**
  fija solo en teléfono.
- Cada tema es `<section class="topic">` con kicker, título y contenido usando: tarjetas
  (`.card` con icono, título, descripción), definiciones textuales en `<blockquote class="q">`,
  tablas, acordeones para detalle, flujos de pasos numerados, cajas `mnemo` (palabra
  mnemotécnica grande + explicación), cajas `error` ("no confundir"), glosario desplegable.
  Más los bloques 🎯 / 🤔 / 🧠 descritos en *Aprendizaje activo*.
- Botón 🔊 Escuchar por sección.
- Al final: cierre activo (repaso mezclado, explícalo en 3 frases, plan de repaso espaciado,
  frase de arranque) y mapa mental de cierre.

### `flash.html` — FlashCards
- Datos en `var CARDS = [{cat, q, a}, …]` (la respuesta admite `<b>`, `<br>`, `<i>Mnemotecnia:</i>`).
  Apuntar a ~80 tarjetas que cubran todo el material.
- Tarjeta que gira al tocarla; botones anterior / siguiente / 🔀 mezclar; marcar como
  difícil o aprendida; contador "X de Y"; estado vacío con mensaje.
- **Repetición espaciada**:
  - Cada tarjeta guarda su nivel y la fecha del próximo repaso. "Aprendida" avanza a
    1 → 3 → 7 → 14 días; "Difícil" vuelve a 1 día y reaparece al final de la sesión actual.
  - Si hay fecha de examen, ninguna tarjeta se programa después del día anterior al examen.
  - Pestañas de filtro: **📅 Hoy · N** (vencidas + nuevas, pestaña por defecto),
    **Todas · N**, **Por repasar**, **Aprendidas**.
  - Estado en `<sigla>_flashcards_status_v2`, migrando lo que haya en `_v1`.
- Filtro por categoría (`cat`) accesible por URL (`flash.html#cat-<slug>`) para que el simulacro
  pueda enlazar a las tarjetas de un tema.
- Botón **⬇️ Exportar a Anki**: descarga un TSV pregunta⇥respuesta.
- Atajos de teclado en PC (ver *Diseño responsive*).

### `resumen.html` — Cheat sheet
- Header "Cheat Sheet · <SIGLA> Parcial <N>" con subtítulo "<Materia> · resumen mnemotécnico".
- Buscador (con "😶 Sin resultados. Prueba con otra sigla o palabra."), chips con emoji por
  sección, secciones plegables `<section class="section" data-nav="🧭 Tema">` con resumen
  denso y cajas `.mnemo`. Última sección: glosario y acrónimos.
- En PC, la navegación por secciones va en una barra lateral fija.

### `resumen-express.html` — Resumen express
- "Todo **<PDF principal>**, en su orden, lo más corto posible. Toca un título para plegarlo."
- Chips de navegación, botón **Plegar todo**, etiquetas de unidad, secciones numeradas
  plegables (`1 El curso ▾`). Viñetas cortas, sin párrafos. Cubre el PDF entero.
- Interruptor de modo 🏢/🚌 (en Transporte: "Continuar donde quedé" y secciones plegadas) y
  botón 🔊 Escuchar por sección.

### `siglas.html` — Siglas y mnemotecnias
- Header con botón **🙈 Modo práctica** (oculta los significados para adivinarlos; tocar una
  sigla la revela) y chips de anclas por sección.
- Cada item:
  ```html
  <div class="s"><span class="k [a|c|v]">DOET</span><div class="b">
    <div class="x"><b>D</b>irectivas · <b>O</b>perativas · <b>E</b>stratégicas · <b>T</b>ácticas</div>
    <div class="m">Suena a "do it" (¡hazlo!)</div>
  </div></div>
  ```
  `k` = sigla (inicial de cada elemento, número clave tipo `8 F`, o contraste tipo `E ≠ T`),
  `x` = expansión con la letra inicial en negrita, `m` = frase mnemotécnica. Las variantes de
  color `a`/`c`/`v` distinguen números/listas, contrastes y pares.
- Al final, dos secciones: **NÚMEROS CLAVE** y **NO CONFUNDIR**.

### `siglas-titulos.html` — Siglas con títulos
- Copia exacta de `siglas.html` (mismas siglas, mismo orden), pero cada item agrega
  `<div class="tt">…</div>` antes de `.x` con el **título textual** del PDF al que corresponde
  esa sigla (ej. "Pasos para la toma de decisión").

### `parcial.html` — Simulacro de parcial
- **Portada** estilo examen UTP: "UNIVERSIDAD TECNOLÓGICA DE PANAMÁ · Facultad de Ingeniería de
  Sistemas Computacionales · <Materia> · <Primer/Segundo…> Examen Parcial · Simulacro ·
  <Profesor> · <Periodo>". Campos opcionales nombre y cédula, indicaciones, tabla de puntos,
  historial de intentos, aviso "⏸️ Tienes un intento en curso" con Continuar / Descartar.
- **Opciones de la portada**:
  - Tipo: **📝 Simulacro completo (100 pts)** o **⚡ Mini simulacro (10 min)**.
  - Duración (solo completo): 60 / 90 recomendado / 120 / sin límite.
  - Interruptor **⚡ Respuestas instantáneas** (verificación inmediata; apagado por defecto, para
    simular el examen real). La preferencia se guarda en `<sigla>_parcial_verif_v1`. La
    estructura del examen es exactamente la misma: solo cambia que cada respuesta se corrige en
    el momento de elegirla o escribirla.
- **Distribución del simulacro completo (100 pts)**:
  | Parte | Tipo | Cantidad × puntos |
  |---|---|---|
  | I | Verdadero o falso | 10 × 2 = 20 |
  | II | Selección múltiple | 15 × 2 = 30 |
  | III | Pareo (8 pares + 2 distractores) | 8 × 2.5 = 20 |
  | IV | Ordenamiento | 2 × 5 = 10 |
  | V | Desarrollo | 2 × 10 = 20 |
- **Mini simulacro**: 5 V/F + 5 de selección múltiple tomadas de los mismos bancos, 10 min,
  nota sobre 100 (proporcional), con su propio historial (`<sigla>_parcial_mini_v1`).
  Pensado para el transporte.
- **Bancos** más grandes que lo que se pregunta, para que cada intento sea una variante distinta:
  `VF` (`{q, a:true/false, e, cat}`), `MC` (`{q, o:[correcta primero, …], e, cat}` — las opciones
  se barajan), `PAREO` (varios sets `{title, pairs:[[término, definición]…], extra:[…]}`),
  `ORD` (`{q, items:[en orden correcto]}`), `DES` (`{q, model, rubric:[[criterio, pts]…]}`).
  `e` = explicación que se muestra en la revisión; `cat` = tema, igual que en `flash.html`, para
  enlazar a la guía y a las tarjetas.
- **Examen**: temporizador (ámbar a ≤10 min, rojo pulsante a ≤1 min, entrega automática en 0),
  contador "X de Y respondidas", botón Entregar con modal de confirmación, todo guardado en
  localStorage para poder recargar (incluido el estado de las preguntas ya verificadas).
- **⚡ Respuestas instantáneas (si están activas)**:
  - También se pueden **activar o desactivar durante el examen** con un botón **⚡ Instantáneas**
    en la barra superior, sin empezar de nuevo (solo afecta lo que se responda después).
  - **V/F y selección múltiple**: al elegir una opción se corrige al instante: ✅ verde o
    ❌ rojo, se marca cuál era la correcta y se muestra la explicación `e`. La respuesta queda
    **bloqueada** (no se puede cambiar después de verla).
  - **Llenar espacios en blanco** (si el simulacro tiene esa parte): se corrige solo cuando la
    pregunta está completa, al pulsar **Enter** en el último espacio o al **pasar a otra pregunta**
    (Enter con espacios vacíos solo salta al siguiente). Se mantiene un botón **✅ Verificar**.
    Muestra ✅/❌ por espacio, las respuestas aceptadas y una casilla para ajustar si se escribió
    lo mismo con otras palabras; los espacios quedan bloqueados.
  - **Pareo**: cada par se corrige al asignarlo (✅/❌ y la definición correcta si falló);
    el par queda bloqueado.
  - **Ordenamiento**: botón **Verificar orden** por pregunta; marca cada elemento en su
    posición correcta o incorrecta y muestra el orden correcto. Se bloquea tras verificar.
  - **Desarrollo**: botón **Ya respondí, ver respuesta** que muestra la respuesta modelo y la
    rúbrica para autoevaluarse en ese momento.
  - Marcador en vivo en el header: puntos obtenidos / puntos verificados y racha de aciertos.
  - En cada fallo, enlaces rápidos "📘 Ver en la guía" y "🃏 Tarjetas del tema".
  - El temporizador sigue corriendo y al final se entrega igual que en modo normal.
  - En el historial, los intentos en los que se activó en algún momento se marcan con la etiqueta "✅ con
    verificación" para distinguirlos de los intentos tipo examen real.
- **Autoevaluación de la Parte V**: respuesta modelo + rúbrica con casillas que suman puntos.
- **Resultados**: nota /100 y letra, puntaje por parte, revisión detallada con filtros
  (Todas / ❌ Incorrectas / ⚠️ Parciales / ✅ Correctas). Cada pregunta fallada enlaza a su tema
  en la guía y a sus tarjetas en `flash.html`. Botones "🔄 Nuevo intento (otra variante)",
  "📘 Repasar en la guía", "← Índice del parcial".
- Pie: "Simulacro generado solo a partir de los <n> PDF del Parcial <N> · UTP · FISC · uso académico."

### `index.html` — Menú del parcial
Copiar `semestre2/gr/parcial1/index.html` (estilo blanco/negro minimalista, modo oscuro con
botón luna/sol y `localStorage("theme")`, botones circulares de volver ← y de inicio ⌂),
asegurando que cumpla *Diseño responsive*, y cambiar solo:
- `<title>Parcial <N> | <Materia></title>` y el `<h1>` con el nombre de la materia.
- Enlaces: volver = `../index.html`, inicio = `../../../index.html`.
- Botones en este orden: Guia, FlashCards, Resumen, Resumen Express, Siglas y Mnemotecnias,
  Siglas con Títulos, Simulacro de Parcial; luego `<div class="separator"></div>` y un botón
  por cada PDF (`<Nombre corto> (PDF)`), con el PDF principal primero.

## Verificación antes de terminar

- Revisar cada página en tres anchos: **412px** (teléfono), **768px** (tablet) y **1366px** (PC).
  En los tres: sin scroll horizontal, nada oculto ni cortado, texto legible y botones
  alcanzables. En PC, el TOC lateral de la guía y el resumen se ve y funciona, y la barra
  inferior móvil está oculta.
  Chrome headless no baja de 500px con `--window-size`; para emular 412px y 768px usar el
  protocolo DevTools (`Emulation.setDeviceMetricsOverride`). La plantilla de `resumen.html`
  trae `table{min-width:520px}`: cambiarlo a `0` para que las tablas quepan en el teléfono.
- Probar `guia.html` y `resumen-express.html` en ambos modos (🏢/🚌): los bloques, las pausas y
  "Continuar donde quedé" funcionan, y ninguna respuesta se ve sin tocarla.
- El botón 🔊 lee en español, pausa y reanuda (también en el teléfono: al reanudar repite el
  párrafo donde quedó) y se oculta si no hay `speechSynthesis`.
- `flash.html`: la pestaña "Hoy" respeta las fechas, el progreso de `_v1` se migra, el TSV se
  descarga, el filtro por `#cat-…` funciona y los atajos de teclado responden en PC.
- Comprobar que cada enlace del índice apunta a un archivo que existe (ojo con tildes y espacios
  en los nombres de los PDF).
- `siglas.html` y `siglas-titulos.html` tienen las mismas siglas en el mismo orden.
- El simulacro: los bancos tienen al menos las cantidades que se eligen por intento, la suma da
  100, y un intento completo y un mini simulacro se pueden entregar y calificar sin errores en
  consola, **con y sin verificación inmediata**. Con verificación: las respuestas quedan
  bloqueadas tras corregirse, el marcador en vivo suma bien, el estado sobrevive a una recarga,
  los espacios en blanco se corrigen solos con Enter o al salir de la pregunta, y el botón
  ⚡ de la barra superior lo activa a mitad de un intento.
- Reportar qué PDF se usó como principal y cualquier tema del material que se haya dejado fuera.