#!/usr/bin/env python3
"""Reject a published tag before regenerating or committing metadata for that tag."""
import argparse,re,subprocess
p=argparse.ArgumentParser();p.add_argument('--tag',required=True);a=p.parse_args()
if not re.fullmatch(r'routing-spain-\d{4}-\d{2}-\d{2}',a.tag):p.error('Use routing-spain-YYYY-MM-DD')
rows=subprocess.check_output(['gh','api','--paginate','repos/KitotsuMolina/GeoAlarm-Routing-Data/releases?per_page=100',
    '--jq','.[] | [.tag_name, .draft] | @tsv'],text=True)
for row in rows.splitlines():
    tag,draft=row.split('\t')
    if tag==a.tag and draft=='false':
        raise SystemExit('This tag is already published. Choose a new dated tag; the existing catalogue will not be changed.')
print('New tag or unpublished draft: generation may proceed.')
