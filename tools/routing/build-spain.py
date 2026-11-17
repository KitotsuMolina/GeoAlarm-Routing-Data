#!/usr/bin/env python3
"""Resumable, sequential generation of 17 communities + Ceuta and Melilla.
Only public Geofabrik inputs, no phone data. Docker has no network or published ports.
"""
import argparse, datetime, hashlib, json, os, pathlib, re, shutil, subprocess, sys, zipfile
ROOT = pathlib.Path(__file__).resolve().parents[2]
IMAGE = 'ghcr.io/valhalla/valhalla-scripted@sha256:c58f9d72ab8c99453dad83da8f0c3df483a1f577243d54d43d9dd1443de1dac5'
REPO = 'KitotsuMolina/GeoAlarm-Routing-Data'

def digest(path):
    with path.open('rb') as f: return hashlib.file_digest(f, 'sha256').hexdigest()

def run(args, log=None):
    subprocess.run([str(x) for x in args], cwd=ROOT, stdout=log, stderr=subprocess.STDOUT if log else None, check=True)

def catalogue(regions, tag):
    rows=[]
    for r in sorted(regions, key=lambda x:x['name']):
        folder=ROOT/'routing-data/spain'/r['id']; folder.mkdir(parents=True,exist_ok=True)
        meta=folder/'package.json'
        if meta.exists():
            data=json.loads(meta.read_text()); rows.append(data)
            link=data['downloadUrl']; size=data['sizeBytes']/1048576
            text=f"# {r['name']}\n\n[Descargar ZIP de rutas]({link}) · {size:.1f} MiB\n\nSHA-256: `{data['sha256']}`\n\nDatos OSM: {data['sourceUrl']}. Licencia ODbL.\n\nImportar en GeoAlarm Libre 0.3.1 o posterior desde Ajustes → Datos y privacidad → Rutas en el dispositivo. Una región activa por instalación. Consulta el [catálogo general](../README.md) para cobertura y límites.\n"
        else:
            text=f"# {r['name']}\n\nGeneración pendiente. No hay un ZIP publicado todavía.\n"
        (folder/'README.md').write_text(text)
    (ROOT/'routing-data/spain/catalog.json').write_text(json.dumps({'schemaVersion':1,'release':tag,'regions':rows},ensure_ascii=False,indent=2)+'\n')
    table = ['| Región | ZIP | Tamaño |', '|---|---|---:|']
    for r in sorted(regions, key=lambda x:x['name']):
        match=next((x for x in rows if x['id']==r['id']),None)
        table.append(f"| [{r['name']}]({r['id']}/) | " + (f"[Descargar]({match['downloadUrl']}) | {match['sizeBytes']/1048576:.1f} MiB |" if match else 'Pendiente | — |'))
    intro = """# Paquetes de rutas de España

17 comunidades autónomas y las ciudades autónomas de Ceuta y Melilla.
Cada carpeta contiene la ficha, la procedencia y la huella SHA-256 de su región.
Los ZIP se alojan en **Releases de este mismo repositorio**, porque GitHub bloquea
archivos de más de 100 MiB en Git normal. No hace falta Git LFS para descargarlos.
La copia local de los ZIP generados está en `routing-data/spain/packages/`,
excluida del historial Git.

**Requiere GeoAlarm Libre 0.3.1 o posterior**, con Valhalla integrado. La versión
0.1.2 de pruebas publicada anteriormente no admite estos paquetes.

## Descargas

"""
    ending = """

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
"""
    (ROOT/'routing-data/spain/README.md').write_text(intro+'\n'.join(table)+ending)
    return rows

def main():
    p=argparse.ArgumentParser();p.add_argument('--tag',default='routing-spain-2026-11-17');p.add_argument('--only',nargs='*');a=p.parse_args()
    if not re.fullmatch(r'routing-spain-\d{4}-\d{2}-\d{2}', a.tag):p.error('Use routing-spain-YYYY-MM-DD for the data release tag')
    regions=json.loads((ROOT/'tools/routing/spain-regions.json').read_text())
    if a.only and set(a.only)-{r['id'] for r in regions}:p.error('Unknown regional id')
    catalogue(regions,a.tag)
    outputs=ROOT/'routing-data/spain/packages';outputs.mkdir(exist_ok=True)
    for r in regions:
        if a.only and r['id'] not in a.only:continue
        folder=ROOT/'routing-data/spain'/r['id'];meta=folder/'package.json'
        archive=outputs/f"geoalarm-{r['id']}.zip"
        if meta.exists() and archive.exists() and json.loads(meta.read_text())['downloadUrl']==f'https://github.com/{REPO}/releases/download/{a.tag}/{archive.name}' and json.loads(meta.read_text())['sha256']==digest(archive):
            print('VERIFIED cached',r['id'],flush=True);continue
        if shutil.disk_usage(ROOT).free<15*1024**3:raise RuntimeError('Need at least 15 GiB free before next region')
        work=ROOT/'.build-cache/spain-regions'/a.tag/r['id'];work.mkdir(parents=True,exist_ok=True)
        source=work/'source.osm.pbf';url=f"https://download.geofabrik.de/{r['source']}-latest.osm.pbf"
        print('DOWNLOADING',r['id'],url,flush=True)
        # curl resolves retries and HTTP errors. The header records the exact source date.
        if not source.exists():
            run(['curl','-fL','--retry','3','--connect-timeout','30','--max-time','1200','-D',work/'source.headers','-o',work/'source.part',url],open(work/'download.log','w'))
            (work/'source.part').rename(source)
        source_sha=digest(source)
        print('BUILDING',r['id'],flush=True)
        with (work/'build.log').open('w') as log:
            run(['docker','run','--rm','--name',f"geoalarm-region-{r['id']}",'--network','none','--cpus','2','--memory','3g','--memory-swap','5g','--user',f'{os.getuid()}:{os.getgid()}',
                 '-v',f'{work}:/work','-v',f'{ROOT}/tools/routing/build-region.sh:/build-region.sh:ro','--entrypoint','sh',IMAGE,'/build-region.sh'],log)
        proofs={}
        lat,lon=r['probe']
        for mode in ['pedestrian','auto']:
            req={'locations':[{'lat':lat,'lon':lon},{'lat':lat+.0007,'lon':lon+.0007}], 'costing':mode,'directions_type':'none'}
            command=['docker','run','--rm','--network','none','--cpus','2','--memory','1g','--user',f'{os.getuid()}:{os.getgid()}', '-v',f'{work}:/work:ro','--entrypoint','valhalla_service',IMAGE,'/work/config.json','route',json.dumps(req)]
            result=subprocess.run(command,text=True,capture_output=True,check=True)
            # Valhalla logs may precede the final response on stdout.
            trip=None
            for line in result.stdout.splitlines():
                try:
                    value=json.loads(line)
                    if 'trip' in value:trip=value['trip']
                except ValueError:pass
            if not trip or trip['status']!=0 or not trip['legs'][0].get('shape'):raise RuntimeError(f'Invalid {mode} proof for {r["id"]}')
            proofs[mode]={'status':trip['status'],'legs':len(trip['legs']),'distanceKm':trip['summary']['length']}
        print('PACKAGING',r['id'],flush=True)
        run([sys.executable,ROOT/'tools/routing/package-region.py','--tiles',work/'tiles.tar','--output',archive,'--id',r['id'],'--name',r['name'],'--probe',f'{lat},{lon}'])
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            manifest=json.loads(z.read('manifest.json'))
            assert manifest['size']<=2*1024**3 and manifest['sha256']==digest(work/'tiles.tar')
        data={'id':r['id'],'name':r['name'],'filename':archive.name,'sizeBytes':archive.stat().st_size,'sha256':digest(archive),
              'minimumAppVersion':'0.3.1','tilesSha256':manifest['sha256'],'sourceUrl':url,'sourceSha256':source_sha,
              'sourceLastModified':next((line.split(':',1)[1].strip() for line in (work/'source.headers').read_text().splitlines() if line.lower().startswith('last-modified:')), None),
              'generatedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'builderImage':IMAGE,'builderVersion':'3.9.1-7fd2228e5',
              'mobileEngineTestedWith':'0.6.6 / Valhalla 3.9.2 (Cantabria reference)',
              'validation':proofs,'downloadUrl':f'https://github.com/{REPO}/releases/download/{a.tag}/{archive.name}', 'license':'ODbL-1.0'}
        meta.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
        (folder/'SHA256SUMS').write_text(f'{data["sha256"]}  {archive.name}\n')
        catalogue(regions,a.tag)
        print('READY',r['id'],data['sizeBytes'],flush=True)
    catalogue(regions,a.tag)

if __name__=='__main__':main()
