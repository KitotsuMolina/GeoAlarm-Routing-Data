#!/usr/bin/env python3
"""Publish only fully generated and verified regional archives as repository Release assets."""
import argparse, concurrent.futures, hashlib, json, pathlib, subprocess
ROOT=pathlib.Path(__file__).resolve().parents[2]
REPO='KitotsuMolina/GeoAlarm-Routing-Data'
p=argparse.ArgumentParser();p.add_argument('--tag',default='routing-spain-2026-11-17');a=p.parse_args()
regions=json.loads((ROOT/'tools/routing/spain-regions.json').read_text())
assets=[]
for region in regions:
    m=json.loads((ROOT/'routing-data/spain'/region['id']/'package.json').read_text())
    archive=ROOT/'routing-data/spain/packages'/m['filename']
    with archive.open('rb') as f: actual=hashlib.file_digest(f,'sha256').hexdigest()
    assert actual==m['sha256'] and archive.stat().st_size==m['sizeBytes']
    assert m['downloadUrl']==f'https://github.com/{REPO}/releases/download/{a.tag}/{archive.name}'
    assert all(m['validation'][mode]['status']==0 for mode in ['pedestrian','auto'])
    assets.append(archive)
sums=ROOT/'routing-data/spain/packages/SHA256SUMS'
sums.write_text(''.join(f"{json.loads((ROOT/'routing-data/spain'/r['id']/'package.json').read_text())['sha256']}  geoalarm-{r['id']}.zip\n" for r in regions))
notes=ROOT/'.build-cache/spain-release-notes.md'
notes.parent.mkdir(parents=True,exist_ok=True)
notes.write_text('''Paquetes regionales para GeoAlarm Libre 0.3.1 o posterior: 17 comunidades autónomas, Ceuta y Melilla.

Importar un ZIP desde Ajustes → Datos y privacidad → Rutas en el dispositivo. Una región activa. No incluye mapas visuales ni necesita un servidor de cálculo. No permite rutas fuera del extracto o entre regiones instaladas por separado.

Cada paquete ha superado comprobaciones de integridad y rutas de referencia a pie y en vehículo en Valhalla 3.9.1. La referencia de compatibilidad Android es Valhalla Mobile 0.6.6 (3.9.2), probada en Cantabria. Estas comprobaciones no garantizan todas las carreteras ni sustituyen pruebas físicas.

Datos © OpenStreetMap contributors, ODbL 1.0. Extractos: Geofabrik. Fuentes, fechas, hashes y limitaciones en el catálogo del repositorio. Descargar SHA256SUMS para comprobar integridad.
''')
def gh(*args):return subprocess.run(['gh',*map(str,args)],cwd=ROOT,check=True)
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
def lookup():
    # GitHub does not resolve /releases/tags/{tag} while the release is a draft.
    entries=json.loads(subprocess.check_output(['gh','api',f'repos/{REPO}/releases?per_page=100'],text=True))
    return next((r for r in entries if r['tag_name']==a.tag),None)

old=lookup()
if old is not None and not old['draft']:
    raise SystemExit('This release is already published. Use a new dated tag for updated data.')
if old is None:
    gh('release','create',a.tag,'--repo',REPO,'--target',head,'--draft','--title',f'Rutas de España · {a.tag}','--notes-file',notes)
else:
    gh('release','edit',a.tag,'--repo',REPO,'--target',head,'--notes-file',notes)
remote={x['name']:x for x in lookup()['assets']}
def upload(path):
    with path.open('rb') as f: expected='sha256:'+hashlib.file_digest(f,'sha256').hexdigest()
    existing=remote.get(path.name)
    if existing and existing['size']==path.stat().st_size and existing.get('digest')==expected:
        print('VERIFIED remote',path.name,flush=True);return
    gh('release','upload',a.tag,path,'--repo',REPO,'--clobber')
    print('UPLOADED',path.name,flush=True)

# Three independent files at a time; a resumed run skips completed, hash-verified assets.
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    list(pool.map(upload,assets+[sums,ROOT/'routing-data/spain/catalog.json']))
view=lookup()
remote={x['name']:x for x in view['assets']}
for path in assets+[sums,ROOT/'routing-data/spain/catalog.json']:
    assert remote[path.name]['size']==path.stat().st_size
    with path.open('rb') as f: expected='sha256:'+hashlib.file_digest(f,'sha256').hexdigest()
    assert remote[path.name].get('digest')==expected, f'Hash mismatch for {path.name}'
# Publish only after every regional archive is present and verified by the API.
gh('release','edit',a.tag,'--repo',REPO,'--draft=false','--latest=false')
print(f'https://github.com/{REPO}/releases/tag/{a.tag}',flush=True)
