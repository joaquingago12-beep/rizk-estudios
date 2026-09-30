# Registro de avance — Base de estudios de CABA

Última actualización: 29/09/2026 · Bloque 2 (búsqueda profunda) terminado

## Archivos

| Archivo | Qué contiene |
|---|---|
| `estudios_caba.csv` | La base lista para importar (una fila por estudio, 29 columnas fijas, UTF-8). |
| `estudios_caba.json` | Exactamente los mismos datos en formato JSON (lista de objetos con las mismas claves). |
| `descartados_y_duplicados.json` | Lo que se revisó y NO entró, con el motivo, y los duplicados que se unificaron. |
| `registro_de_avance.md` | Este archivo. |

## Números del bloque 1

- Resultados revisados en Google Maps: 188 fichas únicas (muchas aparecieron varias veces).
- Registros válidos: **157**
- Descartados: 30 (fuera de CABA, fuera de Argentina, tiendas, peluquerías, estudios de TV/video sin audio, fichas sin datos).
- Duplicados consolidados: 1 (GAMA + Salas La Mansión: misma ubicación y horario).
- Mismo estudio encontrado en más de una búsqueda: 41 (se guardó una sola vez; la columna `times_found_in_searches` lo indica).
- Marcados para revisión (`needs_review = sí`): 24
- Barrio asignado por dirección en zona límite (`neighborhood_confidence = media`): 60

## Términos de búsqueda usados

- "estudio de grabación" + cada uno de los 48 barrios
- "recording studio" (Palermo, Villa Crespo, Belgrano)
- "estudio de mastering" / "estudio de mezcla y mastering" (CABA, Palermo)
- "home studio" (Palermo, Villa Crespo, Villa Urquiza, trap CABA)
- "estudio de podcast" (Palermo)
- "productora musical" (Almagro), "estudio de producción musical" (Belgrano)
- "estudio de audio" (Colegiales), "sala de grabación" (Caballito), "estudio de música" (Balvanera)
- Búsquedas generales: "estudio de grabación Capital Federal", "estudios de grabación Buenos Aires profesional", Palermo Hollywood, Recoleta/Barrio Norte, Boedo

## Barrios

Revisados con al menos una búsqueda (48/48): todos los de la lista.

Sin ningún estudio encontrado hasta ahora: Villa Real, Villa Riachuelo, Villa Soldati.

Revisados con un solo término (conviene repetir con otros términos en el bloque 2): todos excepto Palermo, Villa Crespo, Belgrano, Colegiales, Almagro, Caballito, Balvanera, Recoleta, Boedo, Villa Urquiza.

## Bloque 2 — búsqueda profunda barrio por barrio

Motivo: faltaban estudios que sí están en Google Maps (ejemplo: Estudio Santa Marta, Caballito). Cada búsqueda de Maps devuelve como máximo ~10 resultados, así que una sola búsqueda por barrio no alcanzaba.

Qué se hizo:
- Búsquedas con el nombre de cada barrio y varios términos: "sala de ensayo", "estudio de grabación", "home studio", "productor musical", "estudio de mezcla y mastering", "estudio de podcast", "estudio de música", "estudio de audio", más sub-zonas (Abasto, Once, Congreso, Barrio Norte, Las Cañitas, Parque Centenario, Palermo Soho/Hollywood) y términos generales (recording studio, rehearsal room, estudio de mastering, trap, rap, rock, jazz, tango, folklore).
- En las últimas tandas casi no aparecían lugares nuevos: señal de que la cobertura de Maps quedó cerca del techo.
- El barrio de cada estudio ahora se calcula con el mapa oficial de barrios de la Ciudad (polígonos de GCBA), no por dirección a ojo.

Números:
- Fichas únicas revisadas en el bloque 2: 255
- Estudios nuevos válidos: **112** (ids caba-0158 a caba-0269)
- Descartados: 140 (fuera de CABA, alojamientos, peluquerías/uñas, pilates, clases particulares, tiendas, estudios de foto/video, etc.)
- Duplicados consolidados: 3 (Sala Tony Succar = Sala Palermo-Villa Crespo; Salas Washington = Ala Norte Música; Sala La Comu = Calacuta)
- Nuevos marcados para revisar: 32
- Barrio corregido en registros del bloque 1: 27 (con el mapa oficial)
- Total acumulado: **269** estudios válidos

Estudios por barrio: Palermo 26, Villa Crespo 19, Caballito 15, Almagro 12, Belgrano 11, Balvanera 10, Flores 10, San Nicolás 10, Villa Urquiza 10, Chacarita 9, Saavedra 9, Colegiales 8, Monte Castro 8, Constitución 6, Villa General Mitre 6, Recoleta 6, Villa Ortúzar 6, Villa del Parque 6, Monserrat 6, Boedo 5, Mataderos 5, Parque Chacabuco 5, Retiro 5, San Telmo 5, Villa Luro 5, Coghlan 4, Villa Devoto 4, Villa Lugano 4, Villa Santa Rita 4, Agronomía 3, Floresta 3, La Boca 3, Núñez 3, Barracas 2, Parque Avellaneda 2, La Paternal 2, Parque Chas 2, Versalles 2, Parque Patricios 2, San Cristóbal 2, Liniers 1, Puerto Madero 1, Vélez Sarsfield 1, Villa Pueyrredón 1.

Barrios sin ningún estudio en Maps: Nueva Pompeya, Villa Real, Villa Riachuelo, Villa Soldati.

Por tipo: Recording Studio 151, Rehearsal / Sala de ensayo 101, Music Production 57, Other 56, Mixing 33, Mastering 24, Podcast Studio 17, Home Studio 6.

## Límites honestos
- Google Maps no muestra todo: hay productores y home studios que no tienen ficha, o que la tienen sin la palabra "estudio". Ninguna búsqueda garantiza el 100%.
- Si conocés uno que falta, se carga desde la web (Importar o alta manual) y el sistema avisa si ya existía.

## Pendiente
1. Completar web, Instagram, Facebook y email (Maps no los devuelve).
2. Confirmar los registros marcados para revisión.
