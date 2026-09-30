import json, math
NAMES = {"AGRONOMIA":"Agronomía","ALMAGRO":"Almagro","BALVANERA":"Balvanera","BARRACAS":"Barracas","BELGRANO":"Belgrano","BOEDO":"Boedo",
 "CABALLITO":"Caballito","CHACARITA":"Chacarita","COGHLAN":"Coghlan","COLEGIALES":"Colegiales","CONSTITUCION":"Constitución","FLORES":"Flores",
 "FLORESTA":"Floresta","BOCA":"La Boca","LA BOCA":"La Boca","PATERNAL":"La Paternal","LA PATERNAL":"La Paternal","LINIERS":"Liniers","MATADEROS":"Mataderos",
 "MONTE CASTRO":"Monte Castro","MONSERRAT":"Monserrat","NUEVA POMPEYA":"Nueva Pompeya","NUÑEZ":"Núñez","NUNEZ":"Núñez","PALERMO":"Palermo",
 "PARQUE AVELLANEDA":"Parque Avellaneda","PARQUE CHACABUCO":"Parque Chacabuco","PARQUE CHAS":"Parque Chas","PARQUE PATRICIOS":"Parque Patricios",
 "PUERTO MADERO":"Puerto Madero","RECOLETA":"Recoleta","RETIRO":"Retiro","SAAVEDRA":"Saavedra","SAN CRISTOBAL":"San Cristóbal","SAN NICOLAS":"San Nicolás",
 "SAN TELMO":"San Telmo","VELEZ SARSFIELD":"Vélez Sarsfield","VERSALLES":"Versalles","VILLA CRESPO":"Villa Crespo","VILLA DEL PARQUE":"Villa del Parque",
 "VILLA DEVOTO":"Villa Devoto","VILLA GRAL. MITRE":"Villa General Mitre","VILLA GENERAL MITRE":"Villa General Mitre","VILLA LUGANO":"Villa Lugano","VILLA LURO":"Villa Luro",
 "VILLA ORTUZAR":"Villa Ortúzar","VILLA PUEYRREDON":"Villa Pueyrredón","VILLA REAL":"Villa Real","VILLA RIACHUELO":"Villa Riachuelo",
 "VILLA SANTA RITA":"Villa Santa Rita","VILLA SOLDATI":"Villa Soldati","VILLA URQUIZA":"Villa Urquiza"}
KX = math.cos(math.radians(34.62))
def _rings(geom):
    if geom["type"]=="Polygon": return [geom["coordinates"]]
    return geom["coordinates"]
_d = json.load(open("/home/claude/raw/caba_barrios.geojson"))
POLYS=[]
for f in _d["features"]:
    n=f["properties"]["BARRIO"].strip().upper()
    POLYS.append((NAMES.get(n,n.title()), int(f["properties"]["COMUNA"]), _rings(f["geometry"])))
def _in_ring(x,y,ring):
    inside=False; j=len(ring)-1
    for i in range(len(ring)):
        xi,yi=ring[i][0],ring[i][1]; xj,yj=ring[j][0],ring[j][1]
        if (yi>y)!=(yj>y) and x < (xj-xi)*(y-yi)/(yj-yi)+xi: inside=not inside
        j=i
    return inside
def _in_poly(x,y,polys):
    for poly in polys:
        if _in_ring(x,y,poly[0]) and not any(_in_ring(x,y,h) for h in poly[1:]): return True
    return False
def _seg_dist(px,py,ax,ay,bx,by):
    px*=KX; ax*=KX; bx*=KX
    dx,dy=bx-ax,by-ay; L=dx*dx+dy*dy
    t=0 if L==0 else max(0,min(1,((px-ax)*dx+(py-ay)*dy)/L))
    return math.hypot(px-(ax+t*dx),py-(ay+t*dy))*111320
def _dist(x,y,polys):
    best=1e18
    for poly in polys:
        for ring in poly:
            for i in range(len(ring)-1):
                d=_seg_dist(x,y,ring[i][0],ring[i][1],ring[i+1][0],ring[i+1][1])
                if d<best: best=d
    return best
BBOX=[min(c[0] for _,_,ps in POLYS for p in ps for r in p for c in r), min(c[1] for _,_,ps in POLYS for p in ps for r in p for c in r),
      max(c[0] for _,_,ps in POLYS for p in ps for r in p for c in r), max(c[1] for _,_,ps in POLYS for p in ps for r in p for c in r)]
def barrio(lat,lng):
    """-> (barrio, comuna, metres outside CABA (0 if inside), metres to the barrio edge)"""
    for n,c,ps in POLYS:
        if _in_poly(lng,lat,ps): return n,c,0.0,_dist(lng,lat,ps)
    n,c,ps=min(POLYS,key=lambda t:_dist(lng,lat,t[2]))
    return n,c,_dist(lng,lat,ps),0.0
def in_caba(lat,lng): return any(_in_poly(lng,lat,ps) for _,_,ps in POLYS)
