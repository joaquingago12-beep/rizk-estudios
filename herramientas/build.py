import json, glob, csv, re, unicodedata
VERIFIED = "2026-09-29"
TYPES = {"R":"Recording Studio","H":"Home Studio","P":"Music Production","M":"Mixing","S":"Mastering",
         "E":"Rehearsal / Sala de ensayo","C":"Podcast Studio","O":"Other"}
SERV = {"R":"Grabación","H":"Grabación en home studio","P":"Producción musical","M":"Mezcla","S":"Mastering",
        "E":"Sala de ensayo","C":"Grabación de podcast","O":""}
GTYPE_ES = {"":"","art_studio":"Estudio de arte","manufacturer":"Fabricante","educational_institution":"Institución educativa",
            "school":"Escuela","live_music_venue":"Lugar de música en vivo","concert_hall":"Sala de conciertos",
            "consultant":"Consultor","service":"Servicio","television_studio":"Estudio de televisión"}
NAME_OVERRIDE = {
 "..:: HaceTuMusica ::.. Estudio de Producción Musical":"HaceTuMusica",
 "Producción y Mezcla de Audio. Servicios con video IA - Martín Misenta":"Martín Misenta Producción y Mezcla",
 "Clases de canto - Producción musical - Grabación - Estudio magma":"Estudio Magma",
 "CLASES DE GUITARRA Y BAJO , Producción Musical y Grabación VILLA DEL PARQUE / DEVOTO":"Clases de Guitarra y Bajo, Producción y Grabación (Villa del Parque)",
 "Sala de Ensayo y Luthería | No Music":"No Music",
 "HomeStudio | Grabación y Producción - SANTANA PRODUCE":"Santana Produce",
 "Records Mcl S.R.L.":"Records Mcl",
 "Producción musical , estudio de grabacion":"Producción musical, estudio de grabación (Las Heras)",
}
def norm_addr(a):
    a = a.replace(", Argentina","").replace("Cdad. Autónoma de Buenos Aires","Ciudad Autónoma de Buenos Aires")
    if a.endswith(" CABA"): a = a[:-5] + ", Ciudad Autónoma de Buenos Aires"
    a = re.sub(r"(C?\d{4}[A-Z]{0,3})\s+Ciudad", r"\1, Ciudad", a)
    return re.sub(r"\s+"," ",a).strip()
# --- raw records (first seen wins; keep the search label of first appearance)
recs, order, seen_count = {}, [], {}
for f in sorted(glob.glob("raw/batch0*.jsonl")):
    for line in open(f):
        r = json.loads(line)
        seen_count[r["pid"]] = seen_count.get(r["pid"],0)+1
        if r["pid"] not in recs:
            recs[r["pid"]] = r; order.append(r["pid"])
# --- decisions from later batches (by name)
dec_discard, dec_flag = {}, {}
for f in glob.glob("raw/batch0*_decisions.json"):
    d = json.load(open(f))
    dec_discard.update(d.get("discard",{})); dec_flag.update(d.get("flag",{}))
dec_discard.update({
 "Onix Mastering Studio":"Fuera de CABA (Haedo, Provincia de Buenos Aires)",
 "LcnPro":"Estudio de filmación/fotografía (ciclorama), no de audio",
})
# --- manual metadata
meta = {}
for line in open("raw/meta.tsv"):
    line=line.rstrip("\n")
    if not line or line.startswith("#"): continue
    name, barrio, conf, types, desc = line.rsplit("|",4)
    meta[name.strip()] = (barrio.strip(), conf.strip(), types.strip(), desc.strip())
valid, discarded, dups, missing = [], [], [], []
for pid in order:
    r = recs[pid]; nm = r["name"]
    reason = r.get("discard") or dec_discard.get(nm)
    if reason:
        discarded.append({"google_place_id":pid,"name":nm,"address":r["addr"],"reason":reason}); continue
    if r.get("dup_of"):
        dups.append({"google_place_id":pid,"name":nm,"merged_into":r["dup_of"],
                     "reason":"Misma ubicación exacta y mismos horarios que otro registro; se consolidó"}); continue
    if nm not in meta: missing.append(nm); continue
    valid.append(r)
assert not missing, missing
def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+","-",s).strip("-")[:40]
rows=[]
aliases = {d["merged_into"]: d["name"] for d in dups}
for i, r in enumerate(sorted(valid, key=lambda r:(meta[r["name"]][0], r["name"].lower())), 1):
    barrio, conf, tcodes, desc = meta[r["name"]]
    codes = [c for c in tcodes.split(",") if c]
    flag = r.get("flag") or dec_flag.get(r["name"],"")
    notes = []
    if flag: notes.append(flag)
    if conf == "media": notes.append("Barrio asignado por dirección/coordenadas; zona límite, verificar")
    if r["pid"] in aliases: notes.append(f"Consolidado con ficha duplicada '{aliases[r['pid']]}'")
    commercial = NAME_OVERRIDE.get(r["name"]) or re.split(r"\s[|/]\s|\s-\s", r["name"])[0].strip(" .:")
    gcat = ", ".join(GTYPE_ES.get(t,t) for t in r.get("types","").split(",") if t) or "Estudio de grabación (según búsqueda)"
    rows.append({
      "id": f"caba-{i:04d}",
      "name": commercial,
      "google_maps_name": r["name"],
      "address": norm_addr(r["addr"]),
      "neighborhood": barrio,
      "neighborhood_confidence": conf,
      "city": "Ciudad Autónoma de Buenos Aires",
      "country": "Argentina",
      "latitude": round(r["lat"],7), "longitude": round(r["lng"],7),
      "phone": r["phone"],
      "website": "", "instagram": "", "facebook": "", "email": "",
      "google_place_id": r["pid"],
      "google_maps_url": f"https://www.google.com/maps/place/?q=place_id:{r['pid']}",
      "google_category": gcat,
      "rating": r["rating"] if r["rating"] is not None else "",
      "review_count": r["n"] if r["n"] is not None else "",
      "opening_hours": r["hours"],
      "services": "; ".join(s for s in (SERV[c] for c in codes) if s),
      "studio_type": "; ".join(TYPES[c] for c in codes),
      "description": desc,
      "source": "Google Maps",
      "verified_at": VERIFIED,
      "needs_review": "sí" if flag else "no",
      "review_notes": " | ".join(notes),
      "times_found_in_searches": seen_count[r["pid"]],
    })
json.dump(rows, open("out/estudios_caba.json","w"), ensure_ascii=False, indent=2)
with open("out/estudios_caba.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
json.dump({"discarded":discarded,"duplicates_merged":dups}, open("out/descartados_y_duplicados.json","w"), ensure_ascii=False, indent=2)
# repeated appearances (same place_id in several searches)
rep = sum(1 for r in rows if r["times_found_in_searches"]>1)
print("validos",len(rows),"| descartados",len(discarded),"| duplicados consolidados",len(dups),"| repetidos entre busquedas",rep)
from collections import Counter
print(Counter(r["neighborhood"] for r in rows).most_common())
print(Counter(t for r in rows for t in r["studio_type"].split("; ")).most_common())
print("a revisar:", sum(r["needs_review"]=="sí" for r in rows), "| barrio media:", sum(r["neighborhood_confidence"]=="media" for r in rows))
