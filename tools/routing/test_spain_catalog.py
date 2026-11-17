import json, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[2]
class RegionsTest(unittest.TestCase):
    def test_complete_unique_territorial_list(self):
        regions=json.loads((ROOT/'tools/routing/spain-regions.json').read_text())
        self.assertEqual(19,len(regions))
        self.assertEqual(19,len({r['id'] for r in regions}))
        self.assertEqual(17,len([r for r in regions if r['id'] not in ['ceuta','melilla']]))
        self.assertEqual('africa/canary-islands',next(r['source'] for r in regions if r['id']=='canarias'))
        for region in regions:
            self.assertRegex(region['id'],r'^[a-z0-9-]+$')
            lat,lon=region['probe'];self.assertTrue(-90<=lat<=90 and -180<=lon<=180)
    def test_completed_catalogue_is_consistent(self):
        entries=json.loads((ROOT/'routing-data/spain/catalog.json').read_text())['regions']
        for m in entries:
            self.assertEqual(m,json.loads((ROOT/'routing-data/spain'/m['id']/'package.json').read_text()))
            self.assertRegex(m['sha256'],r'^[a-f0-9]{64}$')
            self.assertTrue(m['downloadUrl'].startswith('https://github.com/KitotsuMolina/GeoAlarm-Routing-Data/releases/download/'))
            self.assertTrue(0<m['sizeBytes']<2*1024**3)
            for mode in ['pedestrian','auto']:self.assertEqual(0,m['validation'][mode]['status'])
if __name__=='__main__':unittest.main()
