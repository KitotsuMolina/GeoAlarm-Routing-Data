# GeoAlarm Routing Data

Paquetes regionales de caminos de España para calcular rutas dentro de Android
con GeoAlarm Libre **0.3.1 o posterior**, sin un servidor de rutas.

➡️ **[Catálogo por comunidad autónoma y ciudad autónoma](routing-data/spain/README.md)**

Los ZIP se descargan desde las Releases de este repositorio. Cada región tiene su
carpeta con enlace, tamaño, procedencia y SHA-256. Los datos cartográficos visuales
no están incluidos. La aplicación admite una sola región activa por instalación.

## Uso

1. Descargar el ZIP de la región y comprobar su huella SHA-256.
2. Abrir GeoAlarm → Ajustes → Datos y privacidad → Rutas en el dispositivo.
3. Pulsar «Instalar o actualizar región» y elegir el ZIP.

GeoAlarm Libre 0.1.2 y otras versiones anteriores al motor integrado no admiten
estos paquetes. Para regiones densas como Madrid se requiere la caché ampliada
de 0.3.1. Este repositorio distribuye datos; no incluye el código ni el historial
del repositorio privado de la aplicación.

## Licencia y procedencia

Datos © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright),
[Open Database License 1.0](https://opendatacommons.org/licenses/odbl/1-0/).
Extractos de [Geofabrik](https://download.geofabrik.de/). Los datos de caminos
se procesan con [Valhalla](https://github.com/valhalla/valhalla).
La atribución y las condiciones de la base de datos deben conservarse al redistribuir.

Las herramientas específicas de generación están en `tools/routing/`. No se
publican credenciales, datos de usuarios, alarmas ni claves de la aplicación.
