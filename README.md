# RIZK — Estudios de CABA

Base de datos de estudios de grabación, salas de ensayo, productores, estudios de mezcla/mastering y de podcast de la Ciudad de Buenos Aires, y la web privada de contacto comercial para trabajarla.

## Qué hay en cada carpeta

| Carpeta / archivo | Qué es |
|---|---|
| `web/index.html` | La web de contacto comercial (panel, "Hoy", lista de estudios, mapa, importar/exportar). Funciona publicada como artefacto de Claude, que le da la base de datos compartida. |
| `datos/estudios_caba.csv` | La base de estudios en planilla (se abre con Excel o Google Sheets). |
| `datos/estudios_caba.json` | Los mismos datos en formato JSON. |
| `datos/descartados_y_duplicados.json` | Lo que se revisó y no entró, con el motivo. |
| `registro_de_avance.md` | Cómo se armó la base, números por bloque y pendientes. |
| `herramientas/` | Scripts usados para armar la base (asignación de barrio con el mapa oficial, consolidación). |

## Importante

- Lo que se carga en la web (estados, notas, seguimientos) vive en la base de datos del artefacto, **no** en este repositorio. Para respaldarlo, exportar desde la web y subir el archivo acá.
- Fuente de los datos de estudios: Google Maps (revisado al 29/09/2026). Repositorio privado.
