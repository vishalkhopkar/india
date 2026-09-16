"""Re-clip already-cached OSM rivers to the map's own frame (not india_clip's small
land-border margin), for rivers whose OSM cache already extends further than what got
drawn. Companion to extend_transboundary.py (which handles the Natural-Earth-covered
rivers); this one is for smaller transboundary rivers only available via OSM.

Run once from _build/rivers, PYTHONIOENCODING=utf-8: python reclip_transboundary.py
"""
import json, os

from shapely.geometry import box, LineString
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


W, H = 1028.0, 1152.3
corners = [to_lonlat(x, y) for x in (0, W) for y in (0, H)]
lons = [c[0] for c in corners]
lats = [c[1] for c in corners]
PAD = 1.0
FRAME = box(min(lons) - PAD, min(lats) - PAD, max(lons) + PAD, max(lats) + PAD)

SIMPLIFY = 0.3
MIN_PIECE = 1.5


def build_paths(lines):
    u = unary_union(lines)
    u = u if u.geom_type == 'LineString' else linemerge(u)
    parts = list(u.geoms) if hasattr(u, 'geoms') else [u]
    clipped = []
    for p in parts:
        c = p.intersection(FRAME)
        if c.is_empty:
            continue
        clipped += list(c.geoms) if hasattr(c, 'geoms') else [c]
    paths = []
    for p in clipped:
        if p.geom_type != 'LineString':
            continue
        proj = LineString([to_svg(lon, lat) for lon, lat in p.coords]).simplify(SIMPLIFY)
        if proj.length >= MIN_PIECE:
            paths.append([[round(x, 1), round(y, 1)] for x, y in proj.coords])
    return paths


# our river name -> (system file, osm cache key)
TARGETS = {
    'Shyok': ('indus.json', 'shyok'),
    'Ghaggar': ('west.json', 'ghaggar'),
    'Raidak': ('brahmaputra.json', 'raidak'),
    'Sankosh': ('brahmaputra.json', 'sankosh'),
    'Jaldhaka': ('brahmaputra.json', 'jaldhaka'),
    'Barak': ('brahmaputra.json', 'barak'),
    'Subansiri': ('brahmaputra.json', 'subansiri'),
}

for name, (sysfile, key) in TARGETS.items():
    path = os.path.join(HERE, sysfile)
    data = json.load(open(path, encoding='utf-8'))
    river = next((r for r in data['rivers'] if r['name'] == name), None)
    assert river, f'{name} not found in {sysfile}'
    cache = json.load(open(os.path.join(DATA, f'osm_{key}.json'), encoding='utf-8'))
    lines = [LineString(l) for l in cache['lines'] if len(l) >= 2]
    paths = build_paths(lines)
    if not paths:
        print(f'{name}: nothing after re-clip, leaving as-is')
        continue
    old_len = sum(LineString(p).length for p in river['paths'])
    new_len = sum(LineString(p).length for p in paths)
    river['paths'] = paths
    json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f'{name:12s} {len(paths):2d} pieces  {old_len * 3.3:6.0f} km -> {new_len * 3.3:6.0f} km')
