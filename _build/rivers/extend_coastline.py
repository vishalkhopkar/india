"""Extend india-borders.svg's coastline layer to cover neighbouring coastlines (Pakistan,
Bangladesh, Myanmar, Sri Lanka) that fall within the map's frame, using the same
Natural Earth coastline data and lon/lat -> SVG affine already used for the rivers.

Run once from _build/rivers, PYTHONIOENCODING=utf-8: python extend_coastline.py
"""
import json, os, re

import numpy as np
from shapely.geometry import shape, box, LineString, MultiLineString, Point
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SVG_PATH = os.path.join(ROOT, 'india-borders.svg')
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


# ------------------------------------------------------------ the map's lon/lat frame
W, H = 1028.0, 1152.3
corners = [to_lonlat(x, y) for x in (0, W) for y in (0, H)]
lons = [c[0] for c in corners]
lats = [c[1] for c in corners]
PAD = 1.0   # degrees of slack beyond the exact corners
minlon, maxlon = min(lons) - PAD, max(lons) + PAD
minlat, maxlat = min(lats) - PAD, max(lats) + PAD
frame = box(minlon, minlat, maxlon, maxlat)
print(f'map frame: lon {minlon:.2f}..{maxlon:.2f}  lat {minlat:.2f}..{maxlat:.2f}')

# ------------------------------------------------------------ India's own polygon (to exclude)
countries = json.load(open(os.path.join(DATA, 'ind.geojson'), encoding='utf-8'))
india = unary_union([shape(f['geometry']) for f in countries['features']
                      if f['properties'].get('ADM0_A3_IN') == 'IND'])
india_coast = india.boundary.buffer(0.03)   # a thin ring around India's own coast to cut out

# ------------------------------------------------------------ world coastline, clipped + cut
coast = json.load(open(os.path.join(DATA, 'ne_10m_coastline.geojson'), encoding='utf-8'))
kept = []
for feat in coast['features']:
    geom = shape(feat['geometry'])
    if not geom.intersects(frame):
        continue
    clipped = geom.intersection(frame)
    remainder = clipped.difference(india_coast)
    if remainder.is_empty:
        continue
    parts = remainder.geoms if hasattr(remainder, 'geoms') else [remainder]
    for p in parts:
        if p.geom_type == 'LineString' and p.length > 0:
            kept.append(p)

print(f'{len(kept)} coastline pieces kept after clipping to frame and cutting India\'s own coast')

# ------------------------------------------------------------ project, simplify, build path data
SIMPLIFY = 0.3   # SVG units, matching the rivers' own simplification tolerance
MIN_LEN = 2.0    # drop tiny fragments (SVG units)
paths = []
for ls in kept:
    svg_pts = [to_svg(lon, lat) for lon, lat in ls.coords]
    proj = LineString(svg_pts).simplify(SIMPLIFY)
    if proj.length < MIN_LEN:
        continue
    d = 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in proj.coords)
    paths.append(d)

print(f'{len(paths)} paths after simplifying and dropping fragments under {MIN_LEN} units')

# ------------------------------------------------------------ splice into india-borders.svg
svg = open(SVG_PATH, encoding='utf-8').read()
existing = svg.count('stroke="#1f6fd0"')
assert existing == 1, f'expected exactly one existing coastline <g>, found {existing}'

new_group = (
    '  <g fill="none" stroke="#1f6fd0" stroke-width="0.9" stroke-linejoin="round" '
    'stroke-linecap="round" class="coastline-extended">\n'
    + '\n'.join(f'    <path d="{d}"/>' for d in paths)
    + '\n  </g>\n'
)

marker = re.search(r'  <g fill="none" stroke="#1f6fd0"[^>]*>.*?</g>\n', svg, flags=re.S)
assert marker, 'could not find the existing coastline <g> block'
insert_at = marker.end()
svg = svg[:insert_at] + new_group + svg[insert_at:]

open(SVG_PATH, 'w', encoding='utf-8', newline='\n').write(svg)
print(f'wrote {SVG_PATH} (+{len(new_group)} bytes)')
