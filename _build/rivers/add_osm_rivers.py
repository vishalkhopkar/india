"""Append OSM-sourced rivers to an existing SYSTEM.json (the ones built by split_systems.py
from the reference-file extraction) without touching the rivers already in it.

Usage (from _build/rivers, PYTHONIOENCODING=utf-8):
  python add_osm_rivers.py SYSTEM ADD.json

ADD.json is a list of:
  {"name": "River name", "rank": 2, "osm": "cache_key", "bbox": [S, W, N, E]}   (bbox optional)

"osm" must have a data/osm_KEY.json cache already (see river_tool.py's `osm` command for how
those were made). Names are checked case-insensitively against every SYSTEM.json already on
disk (matching build.py's own uniqueness check) and skipped with a warning if already drawn.
Uses river_tool.py's own projection and the corrected india_clip() (land-border margin only,
no margin across the coastline), so a river's mouth stops at the coast unless it also happens
to cross a real land border.
"""
import json, os, sys

from shapely.geometry import LineString, box
from shapely.ops import linemerge, unary_union

import river_tool as rt

HERE = os.path.dirname(os.path.abspath(__file__))


def all_drawn_names():
    names = {}
    for fn in os.listdir(HERE):
        if fn.endswith('.json') and not fn.endswith('.spec.json') and fn not in (
                'projection_fit.json', 'ref_fit.json', 'ref_rivers.json'):
            d = json.load(open(os.path.join(HERE, fn), encoding='utf-8'))
            if isinstance(d, dict) and 'rivers' in d:
                for r in d['rivers']:
                    names[r['name'].lower()] = fn
    return names


def main(system, add_path):
    sys_path = os.path.join(HERE, f'{system}.json')
    data = json.load(open(sys_path, encoding='utf-8'))
    additions = json.load(open(add_path, encoding='utf-8'))
    existing_names = all_drawn_names()
    clip = rt.india_clip()
    for r in additions:
        name, rank = r['name'], int(r.get('rank', 3))
        key = name.lower()
        if key in existing_names:
            print(f'SKIP {name}: already drawn in {existing_names[key]}')
            continue
        lines = rt.osm_lines(r['osm'])
        if 'bbox' in r:
            s, w, n, e = r['bbox']
            lines = [g.intersection(box(w, s, e, n)) for g in lines]
        lines = [g for g in lines if not g.is_empty]
        if lines:
            u = unary_union(lines)
            # linemerge() rejects a bare LineString (only valid on Multi*); a single surviving
            # way, or several ways that unioned into one continuous line, needs no merging anyway.
            merged = u if u.geom_type == 'LineString' else linemerge(u)
        else:
            merged = None
        if merged is None or merged.is_empty:
            print(f'WARN {name}: no geometry'); continue
        inside = merged.intersection(clip)
        parts = []
        for g in (getattr(inside, 'geoms', None) or [inside]):
            if g.geom_type == 'LineString':
                parts.append(g)
            elif hasattr(g, 'geoms'):
                parts += [x for x in g.geoms if x.geom_type == 'LineString']
        paths = []
        for p in parts:
            sp = rt.project_line(p).simplify(rt.SIMPLIFY)
            if sp.length >= rt.MIN_PIECE:
                paths.append([[round(x, 1), round(y, 1)] for x, y in sp.coords])
        if not paths:
            print(f'WARN {name}: nothing left inside India after clipping'); continue
        length = sum(LineString(p).length for p in paths)
        data['rivers'].append({'name': name, 'rank': rank, 'source': 'OpenStreetMap', 'paths': paths})
        existing_names[key] = f'{system}.json'
        flag = '  <-- fragmented, check' if len(paths) > 6 else ''
        print(f'{name:<24} rank {rank}  pieces {len(paths):>2}  length {length * 3.3:>6.0f} km  '
              f'nodes {sum(len(p) for p in paths):>5}{flag}')
    json.dump(data, open(sys_path, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f'wrote {sys_path}: {len(data["rivers"])} rivers total')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(__doc__); sys.exit()
    main(sys.argv[1], sys.argv[2])
