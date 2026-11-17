# Paquetes de rutas de España

17 comunidades autónomas y las ciudades autónomas de Ceuta y Melilla.
Cada carpeta contiene la ficha, la procedencia y la huella SHA-256 de su región.
Los ZIP se alojan en **Releases de este mismo repositorio**, porque GitHub bloquea
archivos de más de 100 MiB en Git normal. No hace falta Git LFS para descargarlos.
La copia local de los ZIP generados está en `routing-data/spain/packages/`,
excluida del historial Git.

**Requiere GeoAlarm Libre 0.3.1 o posterior**, con Valhalla integrado. La versión
0.1.2 de pruebas publicada anteriormente no admite estos paquetes.

## Descargas

| Región | ZIP | Tamaño |
|---|---|---:|
| [Andalucía](andalucia/) | [Descargar](https://github.com/KitotsuMolina/GeoAlarm-Routing-Data/releases/download/routing-spain-2026-11-17/geoalarm-andalucia.zip) | 119.8 MiB |
| [Aragón](aragon/) | [Descargar](https://github.com/KitotsuMolina/GeoAlarm-Routing-Data/releases/download/routing-spain-2026-11-17/geoalarm-aragon.zip) | 46.0 MiB |
| [Canarias](canarias/) | [Descargar](https://github.com/KitotsuMolina/GeoAlarm-Routing-Data/releases/download/routing-spain-2026-11-17/geoalarm-canarias.zip) | 29.3 MiB |
| [Cantabria](cantabria/) | [Descargar](https://github.com/KitotsuMolina/GeoAlarm-Routing-Data/releases/download/routing-spain-2026-11-17/geoalarm-cantabria.zip) | 16.0 MiB |
| [Castilla y León](castilla-y-leon/) | [Descargar](https://github.com/KitotsuMolina/GeoAlarm-Routing-Data/releases/download/routing-spain-2026-11-17/geoalarm-castilla-y-leon.zip) | 112.4 MiB |
| [Castilla-La Mancha](castilla-la-mancha/) | [Descargar](https://github.com/KitotsuMolina/GeoAlarm-Routing-Data/releases/download/routing-spain-2026-11-17/geoalarm-castilla-la-mancha.zip) | 60.4 MiB |
| [Cataluña](cataluna/) | [Descargar](https://github.com/KitotsuMolina/GeoAlarm-Routing-Data/releases/download/routing-spain-2026-11-17/geoalarm-cataluna.zip) | 134.7 MiB |
| [Ceuta](ceuta/) | [Descargar](https://github.com/KitotsuMolina/GeoAlarm-Routing-Data/releases/download/routing-spain-2026-11-17/geoalarm-ceuta.zip) | 0.4 MiB |
| [Comunidad Foral de Navarra](navarra/) | [Descargar](https://github.com/KitotsuMolina/GeoAlarm-Routing-Data/releases/download/routing-spain-2026-11-17/geoalarm-navarra.zip) | 23.7 MiB |
| [Comunidad de Madrid](madrid/) | [Descargar](https://github.com/KitotsuMolina/GeoAlarm-Routing-Data/releases/download/routing-spain-2026-11-17/geoalarm-madrid.zip) | 52.7 MiB |
| [Comunitat Valenciana](valencia/) | [Descargar](https://github.com/KitotsuMolina/GeoAlarm-Routing-Data/releases/download/routing-spain-2026-11-17/geoalarm-valencia.zip) | 82.5 MiB |
| [Extremadura](extremadura/) | [Descargar](https://github.com/KitotsuMolina/GeoAlarm-Routing-Data/releases/download/routing-spain-2026-11-17/geoalarm-extremadura.zip) | 26.0 MiB |
| [Galicia](galicia/) | [Descargar](https://github.com/KitotsuMolina/GeoAlarm-Routing-Data/releases/download/routing-spain-2026-11-17/geoalarm-galicia.zip) | 75.3 MiB |
| [Illes Balears](islas-baleares/) | [Descargar](https://github.com/KitotsuMolina/GeoAlarm-Routing-Data/releases/download/routing-spain-2026-11-17/geoalarm-islas-baleares.zip) | 19.9 MiB |
| [La Rioja](la-rioja/) | [Descargar](https://github.com/KitotsuMolina/GeoAlarm-Routing-Data/releases/download/routing-spain-2026-11-17/geoalarm-la-rioja.zip) | 7.6 MiB |
| [Melilla](melilla/) | [Descargar](https://github.com/KitotsuMolina/GeoAlarm-Routing-Data/releases/download/routing-spain-2026-11-17/geoalarm-melilla.zip) | 0.5 MiB |
| [País Vasco](pais-vasco/) | [Descargar](https://github.com/KitotsuMolina/GeoAlarm-Routing-Data/releases/download/routing-spain-2026-11-17/geoalarm-pais-vasco.zip) | 35.8 MiB |
| [Principado de Asturias](asturias/) | [Descargar](https://github.com/KitotsuMolina/GeoAlarm-Routing-Data/releases/download/routing-spain-2026-11-17/geoalarm-asturias.zip) | 20.3 MiB |
| [Región de Murcia](murcia/) | [Descargar](https://github.com/KitotsuMolina/GeoAlarm-Routing-Data/releases/download/routing-spain-2026-11-17/geoalarm-murcia.zip) | 26.5 MiB |

## Instalación y límites

1. Descargar el ZIP de la región y comprobar su SHA-256 con la ficha o SHA256SUMS de la Release.
2. En GeoAlarm: Ajustes → Datos y privacidad → Rutas en el dispositivo → Instalar o actualizar región.
3. Seleccionar el ZIP. Al finalizar, se puede borrar la copia de Descargas.

Solo hay **una región activa** por instalación: importar otra sustituye la anterior.
Los ZIP contienen datos de caminos para Valhalla, no mapas visuales ni un archivo
OSM sin procesar. El mapa sigue cargándose por Internet. No se necesita ningún
servidor Valhalla para calcular. Fuera de la cobertura, entre regiones separadas
o entre islas sin conexión vial no se garantiza un recorrido; no se ofrecen
rutas de transporte público. Los extractos tienen los límites definidos por
Geofabrik y pueden incluir márgenes territoriales, sin garantizar recorridos
transfronterizos. La fecha de datos no es necesariamente la de generación del ZIP.

Cada paquete supera una prueba de integridad y una ruta de referencia a pie y en
vehículo con Valhalla 3.9.1. Cantabria sirve como referencia Android para Valhalla
Mobile 0.6.6 (3.9.2). Eso no significa que se hayan comprobado todas las calles ni
que se haya realizado una caminata física en cada comunidad.

## Datos, licencia y reproducción

Datos © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright),
licencia [ODbL 1.0](https://opendatacommons.org/licenses/odbl/1-0/).
Extractos preparados por [Geofabrik](https://download.geofabrik.de/europe/spain.html).
Canarias procede de [su extracto separado](https://download.geofabrik.de/africa/canary-islands.html).
No se convierte la licencia de la base de datos en la del código de la aplicación.

Cada `package.json` indica fuente, fecha HTTP de origen, SHA-256 del PBF y del ZIP,
imagen del generador y resultado de validación. Los PBF originales se pueden
obtener de la fuente indicada; los intermedios locales no se publican en Git.

Desde la raíz del proyecto, en Linux o WSL, con Python 3.11+, Docker y curl:

```sh
python3 tools/routing/build-spain.py
# Para una región concreta:
python3 tools/routing/build-spain.py --only cantabria
```

El proceso es secuencial y reanudable: verifica hashes de archivos terminados,
limita cada contenedor a 2 CPU, 3 GiB de RAM y hasta 5 GiB incluyendo swap.
No abre puertos ni ejecuta un servicio HTTP. Necesita al menos 15 GiB libres al
comenzar cada región. `tools/routing/publish-spain.py` verifica todos los ZIP antes
de publicar una Release; no ejecutarlo para un catálogo parcial.
