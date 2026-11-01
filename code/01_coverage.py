"""Build data/coverage.geojson (one outline per national lidar layer) and data/layers.json for the page."""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__)); from layers import LAYERS
from shapely.geometry import shape, mapping, box
from shapely.ops import unary_union
A0 = json.load(open('/home/claude/world/raw/ne_50m_admin_0_countries.geojson'))
A0U = json.load(open('/home/claude/world/raw/ne_50m_admin_0_map_units.geojson'))
A1 = json.load(open('/home/claude/world/raw/ne_10m_admin_1_states_provinces.geojson'))
def get(kind, name):
    if kind == 'a0': fs = [f for f in A0['features'] if f['properties']['ADMIN'] == name or f['properties']['NAME'] == name]
    elif kind == 'a0u': fs = [f for f in A0U['features'] if f['properties']['GEOUNIT'] == name]
    else: fs = [f for f in A1['features'] if f['properties']['name'] == name]
    assert fs, (kind, name)
    return unary_union([shape(f['geometry']) for f in fs])
feats, out = [], []
for L in LAYERS:
    g = unary_union([get(k, n) for k, n in L['units']])
    if L['id'] == 'fr': g = g.intersection(box(-6, 41, 10, 52))          # metropolitan France and Corsica
    g = g.simplify(0.02, preserve_topology=True)
    w, s, e, n = g.bounds
    if L['id'] == 'us': w = max(w, -179.5)
    feats.append({'type': 'Feature', 'properties': {'id': L['id'], 'name': L['name'], 'res': L['res'], 'by': L['by']}, 'geometry': mapping(g)})
    o = {k: L[k] for k in ('id', 'name', 'res', 'by', 'lic', 'link', 'kind', 'url', 'minzoom') if k in L}
    for k in ('layer', 'style', 'maxzoom', 'ts', 'grey'):
        if k in L: o[k] = L[k]
    o['bounds'] = [round(w - .05, 2), round(s - .05, 2), round(e + .05, 2), round(n + .05, 2)]
    out.append(o)
def rnd(c):
    return [rnd(x) for x in c] if isinstance(c[0], (list, tuple)) else [round(c[0], 3), round(c[1], 3)]
for f in feats: f['geometry']['coordinates'] = rnd(f['geometry']['coordinates'])
json.dump({'type': 'FeatureCollection', 'features': feats}, open('data/coverage.geojson', 'w'), separators=(',', ':'))
json.dump(out, open('data/layers.json', 'w'), ensure_ascii=False, indent=1)
print(len(out), os.path.getsize('data/coverage.geojson'))
