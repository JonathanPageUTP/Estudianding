# Genera pokedex.js y ubicaciones.js.
# Uso: python3 generar_datos.py <carpeta con monster.json, moves.json y CSV de PokeAPI> <carpeta de salida>
# Fuentes: github.com/PokeMMO-Tools/pokemmo-data (data/monster.json, data/moves.json, data/items.json -> items_mmo.json)
#          github.com/PokeAPI/pokeapi (data/v2/csv: abilities, ability_names, ability_flavor_text, moves, move_names, items, item_names)
import json, csv, re, sys, os, collections
D = sys.argv[1]; OUT = sys.argv[2]
def rd(f): return list(csv.DictReader(open(os.path.join(D, f), encoding="utf-8")))
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
mons = json.load(open(os.path.join(D, "monster.json")))
moves = {m["name"]: m for m in json.load(open(os.path.join(D, "moves.json")))}
TY = {"NORMAL":"Normal","FIRE":"Fuego","WATER":"Agua","GRASS":"Planta","ELECTRIC":"Eléctrico","ICE":"Hielo","FIGHTING":"Lucha","POISON":"Veneno","GROUND":"Tierra","FLYING":"Volador","PSYCHIC":"Psíquico","BUG":"Bicho","ROCK":"Roca","GHOST":"Fantasma","DRAGON":"Dragón","DARK":"Siniestro","STEEL":"Acero"}
# abilities
abid = {norm(r["identifier"]): r["id"] for r in rd("abilities.csv")}
abes = {r["ability_id"]: r["name"] for r in rd("ability_names.csv") if r["local_language_id"] == "7"}
abtx = {}
for r in rd("ability_flavor_text.csv"):
    if r["language_id"] != "7": continue
    vg = int(r["version_group_id"]); cur = abtx.get(r["ability_id"])
    # preferir Negro/Blanco (11) o B2/N2 (14); si no, la versión más antigua disponible
    score = 0 if vg in (11, 14) else vg
    if cur is None or score < cur[0]: abtx[r["ability_id"]] = (score, " ".join(r["flavor_text"].split()))
mvid = {norm(r["identifier"]): r["id"] for r in rd("moves.csv")}
mves = {r["move_id"]: r["name"] for r in rd("move_names.csv") if r["local_language_id"] == "7"}
miss = collections.Counter()
def ab(name):
    if not name or name == "--": return ""
    i = abid.get(norm(name)); 
    if not i or i not in abes: miss["ab:"+name] += 1; return name
    es = abes[i]; ABD[es] = abtx.get(i, (0, ""))[1]; return es
def mv(name):
    i = mvid.get(norm(name)) or {"hijumpkick":"high-jump-kick","faintattack":"feint-attack"}.get(norm(name))
    if i and not i.isdigit(): i = mvid.get(norm(i))
    if not i or i not in mves: miss["mv:"+name] += 1; return name
    return mves[i]
ABD = {}
itid = {norm(r["identifier"]): r["id"] for r in rd("items.csv")}
ites = {r["item_id"]: r["name"] for r in rd("item_names.csv") if r["local_language_id"] == "7"}
mmoit = {i["id"]: i["name"] for i in json.load(open(os.path.join(D, "items_mmo.json")))}
mvbyid = {m["id"]: m["name"] for m in moves.values()}
names = {m["id"]: m["name"] for m in mons}
def it(n):
    i = itid.get(norm(n)) or itid.get({"thunderstone":"thunderstone","deepseatooth":"deepseatooth","deepseascale":"deepseascale","upgrade":"upgrade"}.get(norm(n), ""))
    if not i or i not in ites: miss["it:"+n] += 1; return n
    return ites[i]
def how(e):
    t, v = e["type"], e["val"]; itn = e.get("item_name") or mmoit.get(v, "")
    if t == "LEVEL": return "nivel %d" % v
    if t == "ITEM": return it(itn)
    if t == "ITEM_MALE": return it(itn) + " (macho)"
    if t == "ITEM_FEMALE": return it(itn) + " (hembra)"
    if t == "TRADE": return "intercambio"
    if t == "TRADE_WITH_ITEM": return "intercambio llevando " + it(itn)
    if t == "TRADE_FOR_OPPOSITE": return "intercambio por un " + ("Shelmet" if e["name"] == "Escavalier" else "Karrablast")
    if t == "HAPPINESS": return "amistad alta"
    if t == "HAPPINESS_DAY": return "amistad alta, de día"
    if t == "HAPPINESS_NIGHT": return "amistad alta, de noche"
    if t == "LEVEL_ITEM_NIGHT": return "subir de nivel de noche llevando " + it(itn)
    if t == "LEVEL_ITEM_DAY": return "subir de nivel de día llevando " + it(itn)
    if t == "LEVEL_WITH_SKILL": return "subir de nivel sabiendo " + mv(mvbyid.get(v, ""))
    if t == "LEVEL_WITH_MONSTER": return "subir de nivel con " + names.get(v, "?") + " en el equipo"
    if t.startswith("LEVEL_LOCATION"): return "subir de nivel en un lugar especial"
    if t == "LEVEL_FEMALE": return "nivel %d (hembra)" % v
    if t == "LEVEL_MALE": return "nivel %d (macho)" % v
    if t == "ATK_GREATER_THAN_DEF": return "nivel %d con más Ataque que Defensa" % v
    if t == "ATK_LESS_THAN_DEF": return "nivel %d con menos Ataque que Defensa" % v
    if t == "ATK_EQUAL_TO_DEF": return "nivel %d con Ataque igual a Defensa" % v
    if t in ("PERSONALITY_HIGH", "PERSONALITY_LOW"): return "nivel %d (al azar)" % v
    if t == "ALLOW_MONSTER_CREATION": return "nivel %d" % v
    if t == "CREATE_EXTRA_MONSTER": return "nivel %d con hueco libre y Poké Ball" % v
    if t == "MAX_BEAUTY": return "belleza al máximo"
    miss["evo:"+t] += 1; return t
pre = {}
for m in mons:
    for e in m.get("evolutions") or []:
        if e["id"] <= 649 and m["id"] <= 649 and e["id"] != m["id"]: pre.setdefault(e["id"], m["name"])
DEX = []; LOC = {}; locs = []; li = {}
RAR = {"Very Common":"Muy común","Common":"Común","Uncommon":"Poco común","Rare":"Raro","Very Rare":"Muy raro","Horde":"Horda","Lure":"Cebo","Special":"Especial"}
TYP = {"Grass":"Hierba","Dark Grass":"Hierba alta","Water":"Surf","Cave":"Cueva","Old Rod":"Caña Vieja","Good Rod":"Caña Buena","Super Rod":"Supercaña","Headbutt":"Golpe Cabeza","Rocks":"Golpe Roca","Inside":"Interior","Shadow":"Sombra","Fishing":"Pesca","Dust Cloud":"Nube de polvo","Honey Tree":"Árbol de miel"}
REG = ["Kanto","Johto","Hoenn","Sinnoh","Unova"]
for m in sorted(mons, key=lambda x: x["id"]):
    if m["id"] > 649: continue
    s = m["stats"]; y = m["yields"]
    b = [s["hp"], s["attack"], s["defense"], s["sp_attack"], s["sp_defense"], s["speed"]]
    ev = [y["ev_hp"], y["ev_attack"], y["ev_defense"], y["ev_sp_attack"], y["ev_sp_defense"], y["ev_speed"]]
    t = list(dict.fromkeys(TY[x] for x in m["types"]))
    a = [ab(x["name"]) for x in m["abilities"]] + ["", "", ""]
    if a[1] == a[0]: a[1] = ""
    # mejor ataque con STAB que aprende subiendo de nivel, uno físico y uno especial
    best = {"PHYSICAL": None, "SPECIAL": None}
    for x in m["moves"]:
        if x["type"] != "level": continue
        mm = moves.get(x["name"])
        if not mm or mm["base_power"] <= 1 or mm["skill_damage_type"] not in ("PHYSICAL","SPECIAL") or mm["type"] not in m["types"]: continue
        if mm["base_power"] > 120: continue
        c = mm["skill_damage_type"]
        if best[c] is None or mm["base_power"] > best[c]["base_power"]: best[c] = mm
    st = [[mv(b["name"]), TY[b["type"]], b["base_power"], "F" if c == "PHYSICAL" else "E"] if b else 0 for c, b in (("PHYSICAL", best["PHYSICAL"]), ("SPECIAL", best["SPECIAL"]))]
    EG = {"field":"Campo","water a":"Agua 1","water b":"Agua 2","water c":"Agua 3","monster":"Monstruo","bug":"Bicho","plant":"Planta","humanoid":"Humanoide","chaos":"Amorfo","flying":"Volador","fairy":"Hada","dragon":"Dragón","mineral":"Mineral","genderless":"Sin género","cannot breed":"No cría","ditto":"Ditto"}
    e = [m["id"], m["name"], t, b, ev, a[:3], pre.get(m["id"], ""), st, 1 if m["obtainable"] else 0, [EG[g] for g in m["egg_groups"]], m["gender_ratio"],
         [[e["name"], how(e)] for e in m.get("evolutions") or [] if e["id"] <= 649 and e["id"] != m["id"]]]
    DEX.append(e)
    rows = []
    seen = set()
    for l in m.get("locations") or []:
        name = re.sub(r"^Route (\d+)", r"Ruta \1", l["location"])
        k = (l["region_name"], name)
        if k not in li: li[k] = len(locs); locs.append([REG.index(l["region_name"]), name])
        r = (li[k], TYP.get(l["type"], l["type"]), RAR.get(l["rarity"], l["rarity"]), l["min_level"], l["max_level"])
        if r in seen: continue
        seen.add(r); rows.append(list(r))
    if rows: LOC[m["id"]] = rows
for k in ("Reactive Gas", "Snow Plow"): ABD.setdefault(k, "Habilidad propia de PokeMMO (no existe en los juegos originales).")
print("faltan:", list(miss)[:30], len(miss), file=sys.stderr)
hdr = "/* Datos de PokeMMO (PokeMMO-Tools/pokemmo-data) con nombres en español de PokeAPI. Generado; no editar a mano. */\n"
with open(os.path.join(OUT, "pokedex.js"), "w", encoding="utf-8") as f:
    f.write(hdr + "window.PKDX=" + json.dumps(DEX, ensure_ascii=False, separators=(",", ":")) + ";\nwindow.PKAB=" + json.dumps(ABD, ensure_ascii=False, separators=(",", ":")) + ";\n")
with open(os.path.join(OUT, "ubicaciones.js"), "w", encoding="utf-8") as f:
    f.write(hdr + "window.PKREG=" + json.dumps(REG) + ";\nwindow.PKLUG=" + json.dumps(locs, ensure_ascii=False, separators=(",", ":")) + ";\nwindow.PKLOC=" + json.dumps(LOC, ensure_ascii=False, separators=(",", ":")) + ";\n")
