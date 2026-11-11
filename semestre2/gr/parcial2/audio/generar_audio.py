"""Genera los MP3 de dudas.html para escucharlos con la pantalla apagada.

Uso (desde cualquier carpeta):  python generar_audio.py
Requiere:  pip install edge-tts beautifulsoup4

Crea audio/dudaNN.mp3 (una por duda) y audio/dudas.js con los tiempos de
inicio de cada bloque, para resaltar en pantalla lo que se va leyendo.
Solo regenera las dudas cuyo texto cambió.
"""
import asyncio, hashlib, json, re
from pathlib import Path

import edge_tts
from bs4 import BeautifulSoup

VOICE = "es-PA-MargaritaNeural"
HERE = Path(__file__).resolve().parent
HTML = HERE.parent / "dudas.html"
MANIFEST = HERE / "dudas.js"
BYTES_PER_SEC = 48000 / 8  # edge-tts entrega MP3 mono a 48 kbps

EXPAND = {
    "COBIT": "COBIT, Control Objectives for Information and related Technology,",
    "ITIL": "ITIL, IT Infrastructure Library,",
    "RACI": "RACI, matriz de responsabilidades,",
    "DRSEI": "D, R, S, E, I,",
    "PDCA": "PDCA, planificar, hacer, verificar, actuar,",
}
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿⬀-⯿️‍⃣]")


def speakable(t, said):
    t = EMOJI.sub(" ", t)
    for a, b in [("↔", " y viceversa "), ("→", " lleva a "), ("·", ", "), ("—", ", "), ("–", ", "),
                 ("|", ", y "), ("\t", ": ")]:
        t = t.replace(a, b)
    for a, b in [(r"\bRRHH\b", "recursos humanos"), (r"\bTI\b", "T I"), (r"\bHW\b", "hardware"),
                 (r"\bSW\b", "software"), (r"\bCOM\b", "comunicaciones"), (r"\bJA\b", "Junta de Andalucía"),
                 (r"(\d)\s?×", r"\1 por")]:
        t = re.sub(a, b, t)

    def exp(m):
        k = m.group(0)
        if k in said:
            return k
        said.add(k)
        return EXPAND[k]

    t = re.sub(r"\b(COBIT|ITIL|RACI|DRSEI|PDCA)\b", exp, t)
    return re.sub(r"\s+", " ", t).strip()


def text_of(el):
    if el.name == "tr":
        return "\t".join(c.get_text(" ") for c in el.find_all(["td", "th"]))
    return el.get_text(" ")


def blocks_of(d):
    """Mismo orden y filtro que blocksOf() en dudas.html."""
    ans = d.find(class_="ans")
    cands = [el for el in ans.find_all(True) if el.name in ("p", "li", "tr") or "clave" in (el.get("class") or [])]
    lst = [d.find("summary")] + cands
    lst = [el for el in lst if el.get_text().strip()]
    return [el for el in lst if not any(p in lst for p in el.parents)]


async def synth(text, path):
    await edge_tts.Communicate(text, VOICE).save(str(path))


async def main():
    soup = BeautifulSoup(HTML.read_text(encoding="utf-8"), "html.parser")
    old = {}
    if MANIFEST.exists():
        m = re.search(r"=\s*(\{.*\})\s*;", MANIFEST.read_text(encoding="utf-8"), re.S)
        if m:
            old = json.loads(m.group(1))
    out = {}
    for d in soup.select("details.qa"):
        num = d.find(class_="num").get_text().strip()
        said = set()
        texts = []
        for i, el in enumerate(blocks_of(d)):
            raw = text_of(el)
            if i == 0:
                raw = "Duda " + raw
            texts.append(speakable(raw, said))
        h = hashlib.sha1((VOICE + "\n".join(texts)).encode()).hexdigest()[:12]
        mp3 = HERE / f"duda{num}.mp3"
        if old.get(num, {}).get("h") == h and mp3.exists():
            out[num] = old[num]
            print(f"duda {num}: sin cambios")
            continue
        tmp = HERE / "_tmp"
        tmp.mkdir(exist_ok=True)
        starts, t, data = [], 0.0, b""
        for i, txt in enumerate(texts):
            p = tmp / f"{i}.mp3"
            if txt:
                await synth(txt, p)
                chunk = p.read_bytes()
                p.unlink()
            else:
                chunk = b""
            starts.append(round(t, 2))
            t += len(chunk) / BYTES_PER_SEC
            data += chunk
        tmp.rmdir()
        mp3.write_bytes(data)
        out[num] = {"src": f"audio/duda{num}.mp3", "t": starts, "h": h}
        print(f"duda {num}: {len(texts)} bloques, {t:.0f} s")
    MANIFEST.write_text("window.DUDAS_AUDIO = " + json.dumps(out, ensure_ascii=False) + ";\n", encoding="utf-8")


asyncio.run(main())
