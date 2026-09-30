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

def commercial(n):
    return NAME_OVERRIDE.get(n) or re.split(r"\s[|/]\s|\s-\s", n)[0].strip(" .:")
