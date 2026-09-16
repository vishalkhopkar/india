"""Extend transboundary rivers already drawn on the map to their full length outside
India (as far as it fits the map's own frame — same idea as extend_coastline.py),
using Natural Earth's global 10m river centre-lines already cached for this project.
Purely-domestic rivers need no change and are left alone; this only touches rivers
that already appear in a SYSTEM.json and whose real course extends beyond India.

Run once from _build/rivers, PYTHONIOENCODING=utf-8: python extend_transboundary.py
"""
import json, os

from shapely.geometry import shape, box, LineString
from shapely.ops import unary_union, linemerge

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')

fit = json.load(open(os.path.join(HERE, 'projection_fit.json')))['affine']
A, B, C, D, E, F = fit


def to_svg(lon, lat):
    return (A * lon + B * lat + C, D * lon + E * lat + F)


def to_lonlat(x, y):
    det = A * E - B * D
    lon = ((x - C) * E - B * (y - F)) / det
    lat = (A * (y - F) - D * (x - C)) / det
    return lon, lat


# The map's own lon/lat frame (identical approach to extend_coastline.py) — rivers get
# clipped to this, not to India's border, so they run "however far it fits the map".
W, H = 1028.0, 1152.3
corners = [to_lonlat(x, y) for x in (0, W) for y in (0, H)]
lons = [c[0] for c in corners]
lats = [c[1] for c in corners]
PAD = 1.0
FRAME = box(min(lons) - PAD, min(lats) - PAD, max(lons) + PAD, max(lats) + PAD)

SIMPLIFY = 0.3
MIN_PIECE = 1.5

ne_data = json.load(open(os.path.join(DATA, 'ne_10m_rivers_lake_centerlines.geojson'), encoding='utf-8'))


def ne_geoms(*names):
    out = []
    for f in ne_data['features']:
        n = f['properties'].get('name') or f['properties'].get('name_en')
        if n in names:
            g = shape(f['geometry'])
            out += list(g.geoms) if g.geom_type == 'MultiLineString' else [g]
    return out


def build_paths(geoms):
    clipped = []
    for g in geoms:
        c = g.intersection(FRAME)
        if c.is_empty:
            continue
        clipped += list(c.geoms) if hasattr(c, 'geoms') else [c]
    clipped = [g for g in clipped if g.geom_type == 'LineString' and not g.is_empty]
    if not clipped:
        return []
    merged = unary_union(clipped)
    merged = merged if merged.geom_type == 'LineString' else linemerge(merged)
    parts = list(merged.geoms) if hasattr(merged, 'geoms') else [merged]
    paths = []
    for p in parts:
        if p.geom_type != 'LineString':
            continue
        proj = LineString([to_svg(lon, lat) for lon, lat in p.coords]).simplify(SIMPLIFY)
        if proj.length >= MIN_PIECE:
            paths.append([[round(x, 1), round(y, 1)] for x, y in proj.coords])
    return paths


# our river name -> (system file, [Natural Earth 'name' values to merge])
# Natural Earth already carries these at (or close to) their full real-world length —
# no OSM fetching needed. Names with non-ASCII characters are matched by decoding NE's
# own mangled encoding for "Ghāghara".
GHAGHARA = [n for n in {f['properties'].get('name') for f in ne_data['features']}
            if n and n.startswith('Gh') and n.endswith('ghara')][0]
TARGETS = {
    'Indus': ('indus.json', ['Indus']),
    'Sutlej': ('indus.json', ['Sutlej']),
    'Jhelum': ('indus.json', ['Jhelum']),
    'Chenab': ('indus.json', ['Chenab']),
    'Ravi': ('indus.json', ['Ravi']),
    'Ganga': ('ganga_north.json', ['Ganges']),
    'Gandak': ('ganga_north.json', ['Gandak']),
    'Ghaghra': ('ganga_north.json', [GHAGHARA]),
    'Kosi': ('ganga_north.json', ['Sapt']),
    'Brahmaputra': ('brahmaputra.json', ['Yarlung', 'Maquan', 'Brahmaputra', 'Dihang']),
}

for name, (sysfile, ne_names) in TARGETS.items():
    path = os.path.join(HERE, sysfile)
    data = json.load(open(path, encoding='utf-8'))
    river = next((r for r in data['rivers'] if r['name'] == name), None)
    assert river, f'{name} not found in {sysfile}'
    geoms = ne_geoms(*ne_names)
    assert geoms, f'no Natural Earth geometry found for {name} ({ne_names})'
    paths = build_paths(geoms)
    assert paths, f'{name}: nothing left after clipping to the map frame'
    old_len = sum(LineString(p).length for p in river['paths'])
    new_len = sum(LineString(p).length for p in paths)
    river['paths'] = paths
    river['source'] = 'Natural Earth (full length within the map frame)'
    json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f'{name:20s} {len(river["paths"]):2d} pieces  '
          f'{old_len * 3.3:6.0f} km -> {new_len * 3.3:6.0f} km')
