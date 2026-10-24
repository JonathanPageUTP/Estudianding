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
- PDF principal (define el orden): <nombre del PDF>   (si no lo indico, elige el más completo y dímelo)

Usa como referencia de diseño y estructura semestre2/gr/parcial1. Todo el contenido
sale SOLO de los PDF que están en la carpeta: no inventes datos.
```

---

## Qué hay que generar

Todo dentro de la carpeta del parcial, en archivos HTML **autocontenidos** (CSS y JS inline, sin
librerías externas, sin build), en español y pensados primero para el celular.

| Archivo | Botón en el índice | Qué es |
|---|---|---|
| `guia.html` | Guia | Guía de estudio completa, por temas, para memorizar rápido |
| `flash.html` | FlashCards | Tarjetas pregunta/respuesta con progreso guardado |
| `resumen.html` | Resumen | Cheat sheet mnemotécnico con buscador |
| `resumen-express.html` | Resumen Express | Todo el PDF principal, en su orden, lo más corto posible |
| `siglas.html` | Siglas y Mnemotecnias | Siglas inventadas + mnemotecnias, con modo práctica |
| `siglas-titulos.html` | Siglas con Títulos | Igual que `siglas.html` + el título del PDF de cada sigla |
| `parcial.html` | Simulacro de Parcial | Examen simulado de 100 puntos con temporizador y calificación |
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
   Las mnemotecnias sí son inventadas, pero deben codificar exactamente lo que dice el PDF.
4. Generar las páginas, luego el `index.html`, luego revisar (ver *Verificación*).
5. Commit por página o por bloque, con mensajes como los del historial:
   `Parcial <N> <SIGLA>: guía, flashcards, resúmenes, siglas y simulacro`.

## Estilo visual común (páginas de estudio)

- Tema oscuro propio de cada página con tokens en `:root` (`--bg`, `--surface`, `--line`,
  `--text`, `--text-dim`, `--accent` verde, `--cyan`, `--amber`, `--red`, `--violet` y sus `-dim`),
  fondo con cuadrícula sutil, fuente del sistema (`--sans`) y monoespaciada (`--mono`) para siglas.
- Columna centrada `max-width ≈ 460px`, gutter de 16px, nada de scroll horizontal
  (las tablas van dentro de `.tblwrap` con scroll propio).
- `<html lang="es">`, `<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">`.
- Bloque `@media (max-width:560px)` para teléfonos (~412px): header compacto, flujos de pasos
  en vertical, inputs a 16px para que iOS no haga zoom, botones ≥ 44px.
- Todo acceso a `localStorage` dentro de `try/catch`. Claves con prefijo de la materia y versión:
  `<sigla>_flashcards_status_v1`, `<sigla>_parcial_sim_v1`, `<sigla>_parcial_hist_v1`
  (si ya existe un parcial anterior de la misma materia, incluir el número: `gr_p2_…`).
- Si se usan animaciones al hacer scroll con `IntersectionObserver`, usar `threshold: 0` y un
  respaldo por scroll; en móvil las secciones largas nunca llegan al 10% visible y quedan ocultas.

## Detalle de cada página

### `guia.html` — Guía de estudio
- Barra de progreso de lectura arriba, header fijo con título y **buscador** que resalta y
  filtra, hero con "Todo el material del Parcial <N>, organizado para memorizar rápido".
- Índice (overlay TOC) y **barra de navegación inferior** fija.
- Cada tema es `<section class="topic">` con kicker, título y contenido usando: tarjetas
  (`.card` con icono, título, descripción), definiciones textuales en `<blockquote class="q">`,
  tablas, acordeones para detalle, flujos de pasos numerados, cajas `mnemo` (palabra
  mnemotécnica grande + explicación), cajas `error` ("no confundir"), glosario desplegable.
- Al final: ruta de estudio y mapa mental de cierre.

### `flash.html` — FlashCards
- Datos en `var CARDS = [{cat, q, a}, …]` (la respuesta admite `<b>`, `<br>`, `<i>Mnemotecnia:</i>`).
  Apuntar a ~80 tarjetas que cubran todo el material.
- Tarjeta que gira al tocarla; botones anterior / siguiente / 🔀 mezclar; marcar como
  difícil o aprendida; pestañas de filtro **Todas · N**, **Por repasar**, **Aprendidas**;
  contador "X de Y"; estado vacío con mensaje. Estado guardado en localStorage.

### `resumen.html` — Cheat sheet
- Header "Cheat Sheet · <SIGLA> Parcial <N>" con subtítulo "<Materia> · resumen mnemotécnico".
- Buscador (con "😶 Sin resultados. Prueba con otra sigla o palabra."), chips con emoji por
  sección, secciones plegables `<section class="section" data-nav="🧭 Tema">` con resumen
  denso y cajas `.mnemo`. Última sección: glosario y acrónimos.

### `resumen-express.html` — Resumen express
- "Todo **<PDF principal>**, en su orden, lo más corto posible. Toca un título para plegarlo."
- Chips de navegación, botón **Plegar todo**, etiquetas de unidad, secciones numeradas
  plegables (`1 El curso ▾`). Viñetas cortas, sin párrafos. Cubre el PDF entero.

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
  <Profesor> · <Periodo>". Campos opcionales nombre y cédula, selector de duración
  (60 / 90 recomendado / 120 / sin límite), indicaciones, tabla de puntos, historial de intentos,
  aviso "⏸️ Tienes un intento en curso" con Continuar / Descartar.
- **Distribución (100 pts)**:
  | Parte | Tipo | Cantidad × puntos |
  |---|---|---|
  | I | Verdadero o falso | 10 × 2 = 20 |
  | II | Selección múltiple | 15 × 2 = 30 |
  | III | Pareo (8 pares + 2 distractores) | 8 × 2.5 = 20 |
  | IV | Ordenamiento | 2 × 5 = 10 |
  | V | Desarrollo | 2 × 10 = 20 |
- **Bancos** más grandes que lo que se pregunta, para que cada intento sea una variante distinta:
  `VF` (`{q, a:true/false, e}`), `MC` (`{q, o:[correcta primero, …], e}` — las opciones se
  barajan), `PAREO` (varios sets `{title, pairs:[[término, definición]…], extra:[…]}`),
  `ORD` (`{q, items:[en orden correcto]}`), `DES` (`{q, model, rubric:[[criterio, pts]…]}`).
  `e` = explicación que se muestra en la revisión.
- **Examen**: temporizador (ámbar a ≤10 min, rojo pulsante a ≤1 min, entrega automática en 0),
  contador "X de Y respondidas", botón Entregar con modal de confirmación, todo guardado en
  localStorage para poder recargar.
- **Autoevaluación de la Parte V**: respuesta modelo + rúbrica con casillas que suman puntos.
- **Resultados**: nota /100 y letra, puntaje por parte, revisión detallada con filtros
  (Todas / ❌ Incorrectas / ⚠️ Parciales / ✅ Correctas), botones "🔄 Nuevo intento (otra
  variante)", "📘 Repasar en la guía", "← Índice del parcial".
- Pie: "Simulacro generado solo a partir de los <n> PDF del Parcial <N> · UTP · FISC · uso académico."

### `index.html` — Menú del parcial
Copiar `semestre2/gr/parcial1/index.html` tal cual (estilo blanco/negro minimalista, modo
oscuro con botón luna/sol y `localStorage("theme")`, botones circulares de volver ← y de inicio ⌂)
y cambiar solo:
- `<title>Parcial <N> | <Materia></title>` y el `<h1>` con el nombre de la materia.
- Enlaces: volver = `../index.html`, inicio = `../../../index.html`.
- Botones en este orden: Guia, FlashCards, Resumen, Resumen Express, Siglas y Mnemotecnias,
  Siglas con Títulos, Simulacro de Parcial; luego `<div class="separator"></div>` y un botón
  por cada PDF (`<Nombre corto> (PDF)`), con el PDF principal primero.

## Verificación antes de terminar

- Abrir cada página (o revisar el código) a ~412px de ancho: sin scroll horizontal, nada oculto.
  Chrome headless no baja de 500px con `--window-size`; para emular 412px usar el protocolo
  DevTools (`Emulation.setDeviceMetricsOverride`). La plantilla de `resumen.html` trae
  `table{min-width:520px}`: cambiarlo a `0` para que las tablas quepan en el teléfono.
- Comprobar que cada enlace del índice apunta a un archivo que existe (ojo con tildes y espacios
  en los nombres de los PDF).
- `siglas.html` y `siglas-titulos.html` tienen las mismas siglas en el mismo orden.
- El simulacro: los bancos tienen al menos las cantidades que se eligen por intento, la suma da
  100 y un intento completo se puede entregar y calificar sin errores en consola.
- Reportar qué PDF se usó como principal y cualquier tema del material que se haya dejado fuera.
