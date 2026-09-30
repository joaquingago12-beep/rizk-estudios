# Bloque 2: agrega los estudios nuevos de la búsqueda profunda SIN renumerar los existentes
import json, csv, re, sys
sys.path.insert(0,'/home/claude/tools'); sys.path.insert(0,'/home/claude/raw')
from geo import barrio
from deep_decisions import DEC
from build_consts import TYPES, SERV, GTYPE_ES, norm_addr, commercial
VERIFIED="2026-09-29"
OVR={"Sala de Ensayo - Salas de la Flor":"Salas de la Flor","Sala de ensayo Palermo - villa crespo":"Sala de ensayo Palermo - Villa Crespo",
 "🎤Estudio Horizon":"Estudio Horizon","(Clases de música, grabaciones y shows)":"Clases de música, grabaciones y shows",
 "Estudios Naranja // Rec • Mix • Mastering • Audio Post":"Estudios Naranja","Rocket- Salas de Ensayo & Bar":"Rocket Salas de Ensayo & Bar"}
old=json.load(open('raw/estudios_caba_bloque1_backup.json'))
disc_old=json.load(open('raw/descartados_bloque1_backup.json'))
t=json.load(open('raw/triage.json'))
OLDNOTE="Barrio asignado por dirección/coordenadas; zona límite, verificar"
EDGE="Muy cerca del límite entre barrios (menos de 60 m); verificar"
changes=[]
for o in old:
    b,c,out,edge=barrio(o['latitude'],o['longitude'])
    conf='alta' if edge>=60 else 'media'
    notes=[n for n in o['review_notes'].split(' | ') if n and n!=OLDNOTE]
    if conf=='media': notes.append(EDGE)
    newnotes=' | '.join(notes)
    if b!=o['neighborhood'] or conf!=o['neighborhood_confidence'] or newnotes!=o['review_notes']:
        changes.append({'id':o['id'],'old_barrio':o['neighborhood'],'new_barrio':b,'old_conf':o['neighborhood_confidence'],'new_conf':conf,'old_notes':o['review_notes'],'new_notes':newnotes})
    o['neighborhood']=b; o['neighborhood_confidence']=conf; o['review_notes']=newnotes
MERGE={59:58,113:112}
MERGE_OLD={90:'caba-0029'}
SHARED_PHONE={77:218,218:77}
new=[]; discarded=[]; dups=[]
for i,r in enumerate(t):
    if r['auto']:
        discarded.append({"google_place_id":r['pid'],"name":r['name'],"address":r['addr'],"reason":r['auto'],"bloque":2}); continue
    d,codes,desc,flag=DEC[i]
    if d=='D':
        discarded.append({"google_place_id":r['pid'],"name":r['name'],"address":r['addr'],"reason":desc,"bloque":2}); continue
    if i in MERGE or i in MERGE_OLD or d.startswith('DUP'):
        tgt=MERGE.get(i) or int(d.split(':')[1]) if d.startswith('DUP') else MERGE.get(i)
        into = MERGE_OLD.get(i) or t[tgt]['pid']
        dups.append({"google_place_id":r['pid'],"name":r['name'],"merged_into":into,"reason":"Misma dirección y mismo teléfono que otro registro; se consolidó","bloque":2}); continue
    new.append((i,r,codes.split(','),desc,flag))
aliases={}
for dd in dups: aliases.setdefault(dd['merged_into'],[]).append(dd['name'])
b_of=lambda r: barrio(r['lat'],r['lng'])
new.sort(key=lambda x:(b_of(x[1])[0], x[1]['name'].lower()))
start=max(int(o['id'].split('-')[1]) for o in old)+1
rows=[]
for k,(i,r,codes,desc,flag) in enumerate(new):
    b,c,out,edge=b_of(r); conf='alta' if edge>=60 else 'media'
    notes=[]
    if flag: notes.append(flag)
    if i in SHARED_PHONE: notes.append(f"Comparte teléfono con '{t[SHARED_PHONE[i]]['name']}' (otra dirección); puede ser el mismo dueño")
    if conf=='media': notes.append(EDGE)
    if r['pid'] in aliases: notes.append("Consolidado con ficha duplicada '"+"', '".join(aliases[r['pid']])+"'")
    gcat=", ".join(GTYPE_ES.get(x,x) for x in (r.get('types') or '').split(',') if x) or "Estudio (según búsqueda)"
    rows.append({
      "id":f"caba-{start+k:04d}","name":OVR.get(r['name']) or commercial(r['name']),"google_maps_name":r['name'],
      "address":norm_addr(r['addr']),"neighborhood":b,"neighborhood_confidence":conf,
      "city":"Ciudad Autónoma de Buenos Aires","country":"Argentina",
      "latitude":round(r['lat'],7),"longitude":round(r['lng'],7),"phone":r['phone'] or "",
      "website":"","instagram":"","facebook":"","email":"",
      "google_place_id":r['pid'],"google_maps_url":f"https://www.google.com/maps/place/?q=place_id:{r['pid']}",
      "google_category":gcat,"rating":r['rating'] if r['rating'] is not None else "","review_count":r['n'] if r['n'] is not None else "",
      "opening_hours":r['hours'],"services":"; ".join(s for s in (SERV[c] for c in codes) if s),
      "studio_type":"; ".join(TYPES[c] for c in codes),"description":desc,"source":"Google Maps","verified_at":VERIFIED,
      "needs_review":"sí" if flag else "no","review_notes":" | ".join(notes),"times_found_in_searches":r.get('hits',1)})
allrows=old+rows
json.dump(allrows,open('out/estudios_caba.json','w'),ensure_ascii=False,indent=2)
with open('out/estudios_caba.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=list(allrows[0].keys())); w.writeheader(); w.writerows(allrows)
for x in disc_old['discarded']: x.setdefault('bloque',1)
for x in disc_old['duplicates_merged']: x.setdefault('bloque',1)
json.dump({"discarded":disc_old['discarded']+discarded,"duplicates_merged":disc_old['duplicates_merged']+dups},open('out/descartados_y_duplicados.json','w'),ensure_ascii=False,indent=2)
json.dump({'new':rows,'changes':changes},open('raw/block2_delta.json','w'),ensure_ascii=False,indent=1)
from collections import Counter
print('existentes',len(old),'| nuevos',len(rows),'| total',len(allrows),'| descartados bloque2',len(discarded),'| duplicados bloque2',len(dups))
print('cambios en existentes',len(changes),'| de ellos cambio de barrio',sum(c['old_barrio']!=c['new_barrio'] for c in changes))
print('nuevos a revisar',sum(r['needs_review']=='sí' for r in rows),'| barrio media (todos)',sum(r['neighborhood_confidence']=='media' for r in allrows))
print(sorted(Counter(r['neighborhood'] for r in allrows).items(),key=lambda x:-x[1]))
print('barrios sin estudios:', sorted(set(__import__('geo').NAMES.values())-set(r['neighborhood'] for r in allrows)))
