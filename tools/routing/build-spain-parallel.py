#!/usr/bin/env python3
"""Two independent builders for standard public GitHub runners; no artifact storage needed."""
import importlib.util,json,os,pathlib,re,subprocess,sys,time
root=pathlib.Path(__file__).resolve().parents[2]
tag=os.environ.get('DATA_TAG','routing-spain-2026-11-17')
if not re.fullmatch(r'routing-spain-\d{4}-\d{2}-\d{2}',tag):raise SystemExit('Invalid data tag')
regions=json.loads((root/'tools/routing/spain-regions.json').read_text())
cache=root/'.build-cache';cache.mkdir(exist_ok=True)
processes=[];logs=[]
for index in range(2):
    path=cache/f'batch-{index}.log';log=path.open('w');logs.append(path)
    ids=[r['id'] for r in regions[index::2]]
    process=subprocess.Popen([sys.executable,str(root/'tools/routing/build-spain.py'),'--tag',tag,'--only',*ids],cwd=root,
        env={**os.environ,'REGIONS_SKIP_CATALOGUE':'1'},stdout=log,stderr=subprocess.STDOUT)
    log.close();processes.append(process)
while any(p.poll() is None for p in processes):
    ready=sum(sum(line.startswith('READY ') or line.startswith('VERIFIED cached') for line in p.read_text().splitlines()) for p in logs)
    print(f'Regions verified: {ready}/19',flush=True)
    time.sleep(10)
for path in logs:print(path.read_text(),flush=True)
if any(p.returncode for p in processes):raise SystemExit('A regional builder failed; nothing will be published')
spec=importlib.util.spec_from_file_location('builder',root/'tools/routing/build-spain.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
assert len(module.catalogue(regions,tag))==19
