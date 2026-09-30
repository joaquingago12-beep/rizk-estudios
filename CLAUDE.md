# RIZK — contexto para Claude Code

## Qué es RIZK
Marketplace de la industria musical para Argentina que conecta tres tipos de usuario: **Artistas**, **Productores** (freelance o con estudio propio) y **Estudios**. Se organizan en un hub comprador y un hub vendedor, cada uno con sus niveles de membresía. El objetivo es pasar del mockup actual a una app real (móvil y web) con datos reales, persistencia y backend compartido. El modelo de negocio (comisiones, membresías) todavía se está definiendo.

## Sobre el dueño del proyecto
Joaquín no programa. Explicale cambios y resultados en lenguaje simple, en castellano rioplatense, sin asumir que puede leer o evaluar código.

## Qué hay en este repo hoy
| Ruta | Qué es |
|---|---|
| `datos/estudios_caba.csv` / `.json` | Base de 269 estudios de CABA (grabación, salas de ensayo, productores, mezcla/mastering, podcast). Fuente: Google Maps, revisada al 29/09/2026. Ids `caba-0001`…`caba-0269`, **estables** (no renumerar). |
| `datos/descartados_y_duplicados.json` | Lo revisado que no entró, con motivo; duplicados consolidados. |
| `web/index.html` | CRM privado de contacto comercial (vanilla JS, un solo archivo). Pestañas: Panel, Hoy, Estudios, Mapa (SVG esquemático), Importar/Exportar. |
| `herramientas/` | Scripts Python de armado: `geo.py` (barrio por punto con polígonos oficiales de CABA; necesita `caba_barrios.geojson` de github.com/OpenDataCordoba/barrios), `build.py` (bloque 1), `build2.py` (bloque 2, agrega sin renumerar). Dependen de archivos crudos que no están en el repo; sirven como referencia. |
| `registro_de_avance.md` | Cómo se armó la base, criterios y pendientes. |

## Cómo funciona `web/index.html` hoy (importante)
Está hecha para correr **publicada como artefacto de Claude** (claude.ai). No tiene backend propio: usa el runtime del artefacto.
- `claude.use("db")` → base compartida con API tipo Firestore: `db.collection(x).onSnapshot(...)`, `db.doc("col/id").set(obj)`.
- `claude.use("user")` → quién está viendo.
- `claude.use("downloads")` → descargar archivos de exportación.

Colecciones:
- `studios/{caba-####}`: datos públicos del estudio (mismas claves que el JSON, con `lat`/`lng`, `services` y `studio_type` como listas, `needs_review` booleano).
- `crm/{caba-####}`: relación comercial, **privada** (solo editores). Campos: `status`, `contact_person`, `next_contact` (fecha ISO), `notes`, historial de contactos, `updated_at`. Estados: `sin_contactar`, `contactado`, `no_responde`, `respondio`, `volver`, `interesado`, `reunion`, `demo`, `negociacion`, `cliente`, `no_interesado`.

Fuera de Claude, `claude.use` no existe: para correrla standalone hay que reemplazar esa capa por un backend real (por ejemplo Supabase/Firebase) manteniendo la separación **studios (datos del estudio) / crm (relación comercial)**.

Los datos del CRM (lo que cargan Joaquín y su socio) viven en la base del artefacto y **no** están en este repo. Se exportan desde la pestaña Importar/Exportar.

## Reglas al trabajar
- No inventar datos de estudios. Si algo no se puede verificar, marcarlo para revisión (`needs_review`, `review_notes`).
- No borrar registros ni perder datos del CRM al importar; detectar duplicados por teléfono, dirección cercana o `google_place_id`.
- No renumerar ids existentes.
- Términos de Google Maps: a largo plazo, guardar solo `google_place_id` y datos propios; no copiar reseñas.
