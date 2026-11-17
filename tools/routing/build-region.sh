#!/bin/sh
# Runs inside the pinned image, offline, without a listening HTTP service.
set -eu
cd /work
valhalla_build_config --mjolnir-tile-dir /work/tiles \
  --mjolnir-tile-extract /work/tiles.tar \
  --mjolnir-admin /work/admins.sqlite \
  --mjolnir-timezone /work/timezones.sqlite > config.json
python3 - <<'PY'
import json
p='config.json'
c=json.load(open(p))
c['mjolnir']['concurrency']=2
c['mjolnir']['id_table_size']=100000000
c['mjolnir']['max_cache_size']=268435456
c['mjolnir']['use_lru_mem_cache']=True
json.dump(c,open(p,'w'))
PY
valhalla_build_admins -c config.json source.osm.pbf
valhalla_build_tiles -c config.json -j 2 source.osm.pbf
valhalla_build_extract -c config.json -O -v
