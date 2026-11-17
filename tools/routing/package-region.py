#!/usr/bin/env python3
"""Package an operator-prepared Valhalla extract. No routing service is required on Android."""
import argparse, hashlib, json, pathlib, tarfile, zipfile
p = argparse.ArgumentParser()
p.add_argument('--tiles', type=pathlib.Path, required=True)
p.add_argument('--output', type=pathlib.Path, required=True)
p.add_argument('--name', default='Cantabria')
p.add_argument('--id', default='cantabria')
p.add_argument('--probe', default='43.4435,-3.4578', help='Known routable point lat,lon inside region')
a = p.parse_args()
with tarfile.open(a.tiles, 'r:') as t:
    entries = t.getmembers()
    assert any(x.name.endswith('.gph') for x in entries), 'No graph tiles'
    assert all(x.isfile() for x in entries), 'Only regular files allowed'
lat, lon = map(float, a.probe.split(','))
m = dict(schemaVersion=1, id=a.id, name=a.name, size=a.tiles.stat().st_size,
         sha256=hashlib.file_digest(a.tiles.open('rb'), 'sha256').hexdigest(),
         probe=dict(lat=lat, lon=lon), attribution='Data © OpenStreetMap contributors, ODbL')
a.output.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(a.output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    z.writestr('manifest.json', json.dumps(m, ensure_ascii=False))
    z.write(a.tiles, 'tiles.tar')
print(f'{a.output}: {a.output.stat().st_size} bytes')
