"""River tool: fetch, project, clip and preview rivers for the India borders map.

Run from the _build/rivers folder (set PYTHONIOENCODING=utf-8):

  python river_tool.py ne-list [REGEX]
      Natural Earth 10m river features that reach India (name, scalerank, length in India).

  python river_tool.py osm KEY --wikidata Q12345
  python river_tool.py osm KEY --name "REGEX" [--bbox S,W,N,E]
      Download a river's centre-line ways from OpenStreetMap (Overpass) and cache them in
      data/osm_KEY.json. --wikidata matches the river relation and/or ways tagged with that
      QID (best); --name matches way names/name:en (case-insensitive regex) inside the bbox.

  python river_tool.py make SYSTEM
      Read SYSTEM.spec.json, build SYSTEM.json (SVG coordinates, clipped to India plus a
      ~11 km margin, simplified) and print per-river stats and warnings.

  python river_tool.py preview SYSTEM [--bbox X0,Y0,X1,Y1]
      Render preview_SYSTEM.png: the map's borders, other systems' rivers in pale blue,
      this system's rivers in dark blue with name labels. Open it with the Read tool.
      --bbox zooms to a region in SVG units (map is 1028 x 1152.3; x grows east, y south).

  python river_tool.py summary
      List every river in every SYSTEM.json.

SYSTEM.spec.json format:
  {"system": "godavari", "title": "Godavari system",
   "rivers": [
     {"name": "Godavari", "rank": 1, "sources": [{"ne": "^God.vari$"}]},
     {"name": "Pranhita", "rank": 2, "sources": [{"osm": "pranhita"}]},
     {"name": "Wardha", "rank": 2, "sources": [{"osm": "wardha", "bbox": [18.5, 77.5, 21.5, 80.5]}]}
   ]}
  rank: 1 = main river of a major system, 2 = major tributary / notable river, 3 = minor river.
  sources: one or more of {"ne": REGEX on the Natural Earth name} or {"osm": CACHE_KEY};
  an optional "bbox": [S, W, N, E] in degrees keeps only the part inside that box.
"""
import json, math, os, re, subprocess, sys, time, unicodedata, urllib.parse, urllib.request

from shapely.geometry import LineString, MultiLineString, shape, box, mapping
from shapely.ops import linemerge, unary_union
from shapely import wkb

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')
ROOT = os.path.dirname(os.path.dirname(HERE))           # project folder (india-borders.svg)
MARGIN_DEG = 0.10                                        # ~11 km beyond India's boundary
SIMPLIFY = 0.30                                          # SVG units (1 unit ~ 3.3 km)
MIN_PIECE = 1.5                                          # drop clipped fragments shorter than this
OVERPASS = ['https://overpass-api.de/api/interpreter',
            'https://overpass.kumi.systems/api/interpreter',
            'https://overpass.private.coffee/api/interpreter']

# SVG x/y = affine(lon, lat); fitted to Natural Earth's India outline (median error ~0.55 units).
_fit = json.load(open(os.path.join(HERE, 'projection_fit.json')))['affine']
A, B, C, D, E, F = _fit


def to_svg(lon, lat):
    return (A * lon + B * lat + C, D * lon + E * lat + F)


def norm(s):
    return unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode()


# ------------------------------------------------------------------ India clip shape
def india_clip():
    # India's own coastline, unbuffered (a river reaching the sea should stop at the coast) plus
    # a MARGIN_DEG strip around land borders only (so a river is shown a few km into the
    # neighbouring country when it actually crosses a land border/LoC/LAC).
    cache = os.path.join(DATA, 'india_buffer.wkb')
    if os.path.exists(cache):
        return wkb.loads(open(cache, 'rb').read())
    g = json.load(open(os.path.join(DATA, 'ind.geojson'), encoding='utf-8'))
    feat = [f for f in g['features'] if f['properties'].get('ADM0_A3_IN') == 'IND'][0]
    poly = shape(feat['geometry'])
    lb = json.load(open(os.path.join(DATA, 'ne_10m_admin_0_boundary_lines_land.geojson'), encoding='utf-8'))
    land_lines = [shape(f['geometry']) for f in lb['features']
                  if f['properties'].get('ADM0_A3_L') == 'IND' or f['properties'].get('ADM0_A3_R') == 'IND']
    land_margin = unary_union(land_lines).buffer(MARGIN_DEG)
    buf = unary_union([poly, land_margin])
    open(cache, 'wb').write(wkb.dumps(buf))
    return buf


# ------------------------------------------------------------------ Natural Earth
def ne_features():
    g = json.load(open(os.path.join(DATA, 'ne_10m_rivers_lake_centerlines.geojson'), encoding='utf-8'))
    return g['features']


def ne_lines(regex):
    rx = re.compile(regex, re.I)
    out = []
    for f in ne_features():
        name = norm(f['properties'].get('name')) or norm(f['properties'].get('name_en'))
        if name and rx.search(name):
            geom = shape(f['geometry'])
            out += list(geom.geoms) if geom.geom_type == 'MultiLineString' else [geom]
    return out


def cmd_ne_list(regex='.'):
    clip = india_clip()
    rx = re.compile(regex, re.I)
    rows = []
    for f in ne_features():
        p = f['properties']
        name = norm(p.get('name')) or '(unnamed)'
        if not rx.search(name):
            continue
        geom = shape(f['geometry'])
        if not geom.intersects(clip):
            continue
        inside = geom.intersection(clip)
        rows.append((name, p.get('scalerank'), p.get('featurecla'), round(inside.length * 105)))
    for r in sorted(rows):
        print(f'{r[0]:<28} scalerank={r[1]}  {r[2]:<18} ~{r[3]} km in India+margin')


# ------------------------------------------------------------------ OpenStreetMap
def overpass(query):
    # curl uses the Windows certificate store; Python's bundled certificates fail on some servers.
    last = None
    for attempt in range(6):
        url = OVERPASS[attempt % len(OVERPASS)]
        try:
            r = subprocess.run(['curl', '-sS', '-m', '240', '-A', 'india-borders-map/1.0 (personal research project)',
                                '--data-urlencode', f'data={query}', url],
                               capture_output=True, timeout=260)
            text = r.stdout.decode('utf-8', 'replace')
            if r.returncode != 0 or not text.lstrip().startswith('{'):
                raise RuntimeError((r.stderr.decode('utf-8', 'replace') or text)[:200].strip())
            data = json.loads(text)
            if 'remark' in data and not data.get('elements'):
                raise RuntimeError(data['remark'][:200])
            return data
        except Exception as e:                      # rate limits, timeouts: back off and rotate
            last = e
            print(f'  overpass attempt {attempt + 1} failed ({url}): {e}', file=sys.stderr)
            time.sleep(10 * (attempt + 1))
    raise SystemExit(f'Overpass failed: {last}')


def cmd_osm(key, wikidata=None, name=None, bbox=None):
    if wikidata:
        q = (f'[out:json][timeout:200];'
             f'(rel["wikidata"="{wikidata}"];)->.r;'
             f'(way(r.r);way["wikidata"="{wikidata}"];);out geom tags;')
    elif name:
        bb = f'({bbox})' if bbox else '(6,66,37.5,98.5)'
        rx = name.replace('"', '\\"')
        q = (f'[out:json][timeout:200];'
             f'(way["waterway"="river"]["name"~"{rx}",i]{bb};'
             f'way["waterway"="river"]["name:en"~"{rx}",i]{bb};);out geom tags;')
    else:
        raise SystemExit('give --wikidata or --name')
    res = overpass(q)
    lines, names, skipped = [], {}, 0
    for el in res.get('elements', []):
        if el.get('type') != 'way' or 'geometry' not in el:
            continue
        tags = el.get('tags', {})
        if tags.get('waterway') not in ('river', 'stream', 'canal', 'tidal_channel'):
            skipped += 1                             # riverbank polygons, dams etc.
            continue
        coords = [(p['lon'], p['lat']) for p in el['geometry']]
        if len(coords) >= 2:
            lines.append(coords)
            n = tags.get('name:en') or tags.get('name') or '?'
            names[n] = names.get(n, 0) + 1
    json.dump({'key': key, 'wikidata': wikidata, 'name': name, 'bbox': bbox, 'lines': lines,
               'names': names}, open(os.path.join(DATA, f'osm_{key}.json'), 'w', encoding='utf-8'))
    ml = MultiLineString(lines) if lines else None
    b = ml.bounds if ml else None
    print(f'osm_{key}.json: {len(lines)} ways (skipped {skipped} non-river ways); '
          f'bounds lon/lat {tuple(round(v, 2) for v in b) if b else None}')
    print('  way names:', dict(sorted(names.items(), key=lambda kv: -kv[1])[:12]))


def osm_lines(key):
    path = os.path.join(DATA, f'osm_{key}.json')
    if not os.path.exists(path):
        raise SystemExit(f'missing {path}: run  python river_tool.py osm {key} ...  first')
    return [LineString(l) for l in json.load(open(path, encoding='utf-8'))['lines']]


# ------------------------------------------------------------------ make
def project_line(line):
    return LineString([to_svg(x, y) for x, y in line.coords])


def cmd_make(system):
    spec = json.load(open(os.path.join(HERE, f'{system}.spec.json'), encoding='utf-8'))
    clip = india_clip()
    others = {}
    for fn in os.listdir(HERE):
        if fn.endswith('.json') and not fn.endswith('.spec.json') and fn not in (f'{system}.json', 'projection_fit.json'):
            try:
                for r in json.load(open(os.path.join(HERE, fn), encoding='utf-8'))['rivers']:
                    others[r['name'].lower()] = fn
            except Exception:
                pass
    out, warnings = [], []
    seen = set()
    for r in spec['rivers']:
        name, rank = r['name'], int(r.get('rank', 2))
        if name.lower() in seen:
            warnings.append(f'{name}: listed twice in this spec')
        seen.add(name.lower())
        if name.lower() in others:
            warnings.append(f'{name}: also drawn in {others[name.lower()]} (avoid duplicates)')
        geoms, labels = [], []
        for src in r['sources']:
            if 'ne' in src:
                gs = ne_lines(src['ne']); labels.append('Natural Earth')
            elif 'osm' in src:
                gs = osm_lines(src['osm']); labels.append('OpenStreetMap')
            else:
                raise SystemExit(f'{name}: unknown source {src}')
            if 'bbox' in src:
                s, w, n, e = src['bbox']
                gs = [g.intersection(box(w, s, e, n)) for g in gs]
            geoms += gs
            if not gs:
                warnings.append(f'{name}: source {src} matched nothing')
        merged = linemerge(unary_union([g for g in geoms if not g.is_empty])) if geoms else None
        if merged is None or merged.is_empty:
            warnings.append(f'{name}: no geometry'); continue
        inside = merged.intersection(clip)
        parts = []
        for g in (getattr(inside, 'geoms', None) or [inside]):
            if g.geom_type == 'LineString':
                parts.append(g)
            elif hasattr(g, 'geoms'):
                parts += [x for x in g.geoms if x.geom_type == 'LineString']
        paths = []
        for p in parts:
            sp = project_line(p).simplify(SIMPLIFY)
            if sp.length >= MIN_PIECE:
                paths.append([[round(x, 1), round(y, 1)] for x, y in sp.coords])
        if not paths:
            warnings.append(f'{name}: nothing left inside India after clipping'); continue
        length = sum(LineString(p).length for p in paths)
        out.append({'name': name, 'rank': rank, 'source': ' + '.join(sorted(set(labels))), 'paths': paths})
        flag = '  <-- fragmented, check' if len(paths) > 6 else ''
        print(f'{name:<24} rank {rank}  pieces {len(paths):>2}  length {length * 3.3:>6.0f} km  '
              f'nodes {sum(len(p) for p in paths):>5}{flag}')
    json.dump({'system': spec['system'], 'title': spec.get('title', system), 'rivers': out},
              open(os.path.join(HERE, f'{system}.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print(f'wrote {system}.json: {len(out)} rivers')
    for w in warnings:
        print('WARNING:', w)


# ------------------------------------------------------------------ preview
def cmd_preview(system, bbox=None):
    svg = open(os.path.join(ROOT, 'india-borders.svg'), encoding='utf-8').read()
    svg = re.sub(r'<metadata>.*?</metadata>', '', svg, flags=re.S)
    inner = re.search(r'<svg[^>]*>(.*)</svg>', svg, flags=re.S).group(1)
    x0, y0, x1, y1 = bbox or (0, 0, 1028, 1152.3)
    k = (x1 - x0) / 1028                       # keep strokes/labels readable when zoomed
    layers = []
    for fn in sorted(os.listdir(HERE)):
        if not fn.endswith('.json') or fn.endswith('.spec.json') or fn == 'projection_fit.json':
            continue
        data = json.load(open(os.path.join(HERE, fn), encoding='utf-8'))
        if not isinstance(data, dict) or 'rivers' not in data:
            continue
        mine = data['system'] == system
        for r in data['rivers']:
            w = {1: 1.6, 2: 1.1, 3: 0.7}[r['rank']] * max(k, 0.25)
            col = '#1565c0' if mine else '#b9cfe6'
            for p in r['paths']:
                d = 'M' + 'L'.join(f'{x} {y}' for x, y in p)
                layers.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w:.2f}" stroke-linecap="round" stroke-linejoin="round"/>')
            if mine:
                longest = max(r['paths'], key=lambda p: LineString(p).length)
                mx, my = longest[len(longest) // 2]
                fs = 9 * max(k, 0.25)
                layers.append(f'<text x="{mx}" y="{my}" font-size="{fs:.1f}" font-family="Arial" fill="#b00020" '
                              f'stroke="#fff" stroke-width="{fs / 4:.2f}" paint-order="stroke">{r["name"]}</text>')
    W = 1400
    H = int(W * (y1 - y0) / (x1 - x0))
    page = (f'<html><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {x1 - x0} {y1 - y0}" '
            f'width="{W}" height="{H}">{inner}{"".join(layers)}</svg></body></html>')
    html_path = os.path.join(HERE, f'preview_{system}.html')
    png_path = os.path.join(HERE, f'preview_{system}.png')
    open(html_path, 'w', encoding='utf-8').write(page)
    chrome = r'C:/Program Files/Google/Chrome/Application/chrome.exe'
    prof = os.path.join(os.environ.get('TEMP', DATA), f'chrome-river-{system}')
    subprocess.run([chrome, '--headless=new', '--disable-gpu', '--hide-scrollbars', f'--user-data-dir={prof}',
                    f'--screenshot={png_path}', f'--window-size={W},{H}',
                    'file:///' + html_path.replace(os.sep, '/')], capture_output=True, timeout=120)
    print(png_path)


def cmd_summary():
    total = 0
    for fn in sorted(os.listdir(HERE)):
        if fn.endswith('.json') and not fn.endswith('.spec.json') and fn not in (
                'projection_fit.json', 'ref_fit.json', 'ref_rivers.json'):
            data = json.load(open(os.path.join(HERE, fn), encoding='utf-8'))
            if not isinstance(data, dict) or 'rivers' not in data:
                continue
            names = [f"{r['name']} ({r['rank']})" for r in data['rivers']]
            total += len(names)
            print(f"{data['title']}: {', '.join(names)}")
    print('total rivers:', total)


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit()
    cmd, rest = args[0], args[1:]

    def opt(flag):
        return rest[rest.index(flag) + 1] if flag in rest else None

    if cmd == 'ne-list':
        cmd_ne_list(rest[0] if rest else '.')
    elif cmd == 'osm':
        cmd_osm(rest[0], wikidata=opt('--wikidata'), name=opt('--name'), bbox=opt('--bbox'))
    elif cmd == 'make':
        cmd_make(rest[0])
    elif cmd == 'preview':
        bb = opt('--bbox')
        cmd_preview(rest[0], tuple(map(float, bb.split(','))) if bb else None)
    elif cmd == 'summary':
        cmd_summary()
    else:
        print(__doc__)
