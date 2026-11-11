"""Genera los MP3 de la guía y el resumen para escucharlos con la pantalla apagada.

Uso:  python generar_paginas.py            (guia y resumen)
      python generar_paginas.py resumen    (solo una página)
Requiere:  pip install edge-tts playwright   (usa el Edge o Chrome instalado)

Abre cada página en un navegador sin ventana y le pide a audio/voz.js los
textos exactos que lee (Voz.dump()), así el resaltado coincide con el audio.
Crea audio/<pagina>/<seccion>.mp3 y audio/<pagina>.js con los tiempos de
inicio de cada bloque. Solo regenera las secciones cuyo texto cambió.
"""
import asyncio, hashlib, json, re, sys
from pathlib import Path

import edge_tts
from playwright.async_api import async_playwright

VOICE = "es-PA-MargaritaNeural"
HERE = Path(__file__).resolve().parent
PAGES = ["guia", "resumen"]
BYTES_PER_SEC = 48000 / 8  # edge-tts entrega MP3 mono a 48 kbps
PARALLEL = 6


async def dump(page_name):
    url = (HERE.parent / f"{page_name}.html").as_uri()
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(channel="msedge")
        except Exception:
            browser = await p.chromium.launch(channel="chrome")
        page = await browser.new_page(viewport={"width": 412, "height": 900})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        await page.goto(url)
        await page.wait_for_function("window.Voz && document.readyState === 'complete'")
        data = await page.evaluate("Voz.dump()")
        await browser.close()
    if errors:
        print("  errores JS en la página:", *errors, sep="\n   ")
    return data


async def synth_one(text, sem, tries=4):
    async with sem:
        for k in range(tries):
            try:
                buf = b""
                async for chunk in edge_tts.Communicate(text, VOICE).stream():
                    if chunk["type"] == "audio":
                        buf += chunk["data"]
                return buf
            except Exception:
                if k == tries - 1:
                    raise
                await asyncio.sleep(2 + 3 * k)


async def build(page_name):
    print(f"== {page_name}")
    data = await dump(page_name)
    folder = HERE / page_name
    folder.mkdir(exist_ok=True)
    manifest = HERE / f"{page_name}.js"
    old = {}
    if manifest.exists():
        m = re.search(r"=\s*(\{.*\})\s*;", manifest.read_text(encoding="utf-8"), re.S)
        if m:
            old = json.loads(m.group(1))
    sem = asyncio.Semaphore(PARALLEL)
    out, total = {}, 0.0
    for key, sec in data.items():
        texts = sec["texts"]
        h = hashlib.sha1((VOICE + "\n".join(texts)).encode()).hexdigest()[:12]
        mp3 = folder / f"{key}.mp3"
        if old.get(key, {}).get("h") == h and mp3.exists():
            out[key] = old[key]
            total += mp3.stat().st_size / BYTES_PER_SEC
            print(f"  {key}: sin cambios")
            continue
        chunks = await asyncio.gather(*[synth_one(t, sem) if t else asyncio.sleep(0, b"") for t in texts])
        starts, t = [], 0.0
        for c in chunks:
            starts.append(round(t, 2))
            t += len(c) / BYTES_PER_SEC
        mp3.write_bytes(b"".join(chunks))
        total += t
        out[key] = {"src": f"audio/{page_name}/{key}.mp3", "t": starts, "h": h}
        print(f"  {key}: {len(texts)} bloques, {t / 60:.1f} min · {sec['title'][:50]}")
    for f in folder.glob("*.mp3"):
        if f.stem not in out:
            f.unlink()
    manifest.write_text("window.VOZ_AUDIO = " + json.dumps(out, ensure_ascii=False) + ";\n", encoding="utf-8")
    print(f"  total {total / 60:.0f} min")


async def main():
    for name in sys.argv[1:] or PAGES:
        await build(name)


asyncio.run(main())
