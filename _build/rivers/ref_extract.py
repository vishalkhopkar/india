"""Extract rivers from the reference file India_rivers_and_lakes_map.svg and reproject
them into india-borders.svg's coordinate space.

Usage (from _build/rivers, PYTHONIOENCODING=utf-8):
  python ref_extract.py fit        fit the reference SVG's coordinate space to ours (ICP)
  python ref_extract.py list       list every named river label found in the reference file
  python ref_extract.py build      match labels to line-work, group into named rivers,
                                    transform + clip, write ref_rivers.json (all systems combined)
  python ref_extract.py split      split ref_rivers.json into the RIVERS.md systems as SYSTEM.json
  python ref_extract.py preview [--bbox X0,Y0,X1,Y1]   render preview_ref.png (all rivers, red labels)
"""
import json, math, os, re, subprocess, sys

from shapely.geometry import LineString, MultiLineString, Point, box
from shapely.ops import unary_union, linemerge, nearest_points
from shapely.strtree import STRtree

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
REF = os.path.join(ROOT, 'India_rivers_and_lakes_map.svg')
OUR = os.path.join(ROOT, 'india-borders.svg')
FIT = os.path.join(HERE, 'ref_fit.json')

# Names in the label list that are not rivers (seas, reservoirs/lakes, title, legend).
NOT_RIVERS = {
    'bay of bengal', 'andaman sea', 'arabian sea', 'gulf of khambhat', 'gulf of mannar',
    'palk bay', 'ten degree channel', 'bhavani sagar', 'krishna raja sagara',
    'bhadra reservoir', 'tungabhadra reservoir', 'nagarjuna sagar', 'tammileru reservoir',
    'hirakud reservoir', 'gobind ballabh pant sagar', 'gandhi sagar', 'rana pratap sagar',
    'gobind sagar', 'pangong tso', 'tso moriri', 'sambhar lake', 'nizam sagar',
    'linganmakki sagar', 'stanley reservoir', 'vembanad lake', 'india rivers and lakes map',
    'fresh water lake', 'river', 'salt water lake',
}

# Reference-file name -> the name we use on our map (only where they differ or are ambiguous).
RENAME = {
    'manjra': 'Manjira', 'shetrunjaya': 'Shetrunji', 'baghmati': 'Bagmati', 'gomati': 'Gomti',
    'hughli': 'Hooghly', 'kasai': 'Kasai (Kansai)', 'tamiraparani': 'Tamirabarani',
    'sarda': 'Sharda (Mahakali)', 'bhavani': 'Bhavani', 'beypore': 'Chaliyar',
}
# Rivers sharing a name with a different river elsewhere on the map (see RIVERS.md's naming rule).
QUALIFY = {
    'banas': 'Banas (Rajasthan)', 'parbati': 'Parbati (Chambal)', 'bhadra': 'Bhadra (Tungabhadra)',
    'tunga': 'Tunga (Tungabhadra)', 'godavari': 'Godavari',
}


# ------------------------------------------------------------------ tiny SVG path parser
_NUM = re.compile(r'[+-]?(\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?')
_FLAG = re.compile(r'[01]')
_WS = re.compile(r'[\s,]*')


class _Scanner:
    """Reads an SVG path's command letters and numbers directly off the string, so that
    arc flags (single '0'/'1' digits, often packed together with no separator) are read
    correctly instead of being swallowed by a generic number regex."""
    def __init__(self, d):
        self.s = d
        self.i = 0

    def skip_ws(self):
        self.i = _WS.match(self.s, self.i).end()

    def peek_cmd(self):
        self.skip_ws()
        if self.i < len(self.s) and self.s[self.i] in 'MLHVCSQTAZmlhvcsqtaz':
            return self.s[self.i]
        return None

    def next_cmd(self):
        c = self.peek_cmd()
        if c:
            self.i += 1
        return c

    def num(self):
        self.skip_ws()
        m = _NUM.match(self.s, self.i)
        if not m:
            raise ValueError(f'expected number at {self.i}: ...{self.s[self.i:self.i+20]!r}')
        self.i = m.end()
        return float(m.group(0))

    def nums(self, n):
        return [self.num() for _ in range(n)]

    def flag(self):
        self.skip_ws()
        m = _FLAG.match(self.s, self.i)
        if not m:
            raise ValueError(f'expected flag at {self.i}: ...{self.s[self.i:self.i+20]!r}')
        self.i = m.end()
        return int(m.group(0))

    def more_numbers_follow(self):
        """True if, after whitespace, another number (not a command letter) comes next —
        used because a command letter followed by extra coordinate pairs repeats implicitly."""
        self.skip_ws()
        return self.i < len(self.s) and (self.s[self.i] in '+-.0123456789')


def parse_path(d):
    """Return a flattened list of (x, y) point lists (one per subpath), with curves sampled."""
    sc = _Scanner(d)
    subpaths, cur = [], []
    x = y = 0.0
    sx = sy = 0.0
    cmd = None
    prev_ctrl = None  # for S/s and T/t reflection

    def bez(p0, p1, p2, p3, n=12):
        pts = []
        for t in [k / n for k in range(1, n + 1)]:
            mt = 1 - t
            bx = (mt**3 * p0[0] + 3 * mt**2 * t * p1[0] + 3 * mt * t**2 * p2[0] + t**3 * p3[0])
            by = (mt**3 * p0[1] + 3 * mt**2 * t * p1[1] + 3 * mt * t**2 * p2[1] + t**3 * p3[1])
            pts.append((bx, by))
        return pts

    def arc_to_bezier(p0, rx, ry, phi, laf, sweep, p1, n=16):
        # Standard SVG-arc -> centre-parameterisation, sampled as a polyline (good enough
        # for this map's decorative arcs; only used if the reference file has any).
        phi = math.radians(phi)
        x1, y1 = p0; x2, y2 = p1
        if rx == 0 or ry == 0 or (x1, y1) == (x2, y2):
            return [p1]
        cphi, sphi = math.cos(phi), math.sin(phi)
        dx2, dy2 = (x1 - x2) / 2, (y1 - y2) / 2
        x1p = cphi * dx2 + sphi * dy2
        y1p = -sphi * dx2 + cphi * dy2
        rx, ry = abs(rx), abs(ry)
        lam = (x1p**2) / rx**2 + (y1p**2) / ry**2
        if lam > 1:
            rx *= math.sqrt(lam); ry *= math.sqrt(lam)
        sign = -1 if laf == sweep else 1
        num = max(rx**2 * ry**2 - rx**2 * y1p**2 - ry**2 * x1p**2, 0)
        den = rx**2 * y1p**2 + ry**2 * x1p**2
        co = sign * math.sqrt(num / den) if den else 0
        cxp, cyp = co * rx * y1p / ry, -co * ry * x1p / rx
        cx = cphi * cxp - sphi * cyp + (x1 + x2) / 2
        cy = sphi * cxp + cphi * cyp + (y1 + y2) / 2

        def ang(ux, uy, vx, vy):
            d = math.hypot(ux, uy) * math.hypot(vx, vy)
            a = math.acos(max(-1, min(1, (ux * vx + uy * vy) / d))) if d else 0
            return a if ux * vy - uy * vx >= 0 else -a
        th1 = ang(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry)
        dth = ang((x1p - cxp) / rx, (y1p - cyp) / ry, (-x1p - cxp) / rx, (-y1p - cyp) / ry)
        if not sweep and dth > 0:
            dth -= 2 * math.pi
        if sweep and dth < 0:
            dth += 2 * math.pi
        pts = []
        for k in range(1, n + 1):
            t = th1 + dth * k / n
            ex = cphi * rx * math.cos(t) - sphi * ry * math.sin(t) + cx
            ey = sphi * rx * math.cos(t) + cphi * ry * math.sin(t) + cy
            pts.append((ex, ey))
        return pts

    while True:
        c = sc.next_cmd()
        if c is None:
            if cmd is None or not sc.more_numbers_follow():
                break
            c = cmd   # bare coordinates after a command repeat that command (implicit lineto etc.)
        if c in ('M', 'm'):
            dx, dy = sc.nums(2)
            x, y = (dx, dy) if c == 'M' else (x + dx, y + dy)
            if cur:
                subpaths.append(cur)
            cur = [(x, y)]
            sx, sy = x, y
            cmd = 'L' if c == 'M' else 'l'
        elif c in ('L', 'l'):
            dx, dy = sc.nums(2)
            x, y = (dx, dy) if c == 'L' else (x + dx, y + dy)
            cur.append((x, y)); prev_ctrl = None
        elif c in ('H', 'h'):
            dx = sc.num()
            x = dx if c == 'H' else x + dx
            cur.append((x, y)); prev_ctrl = None
        elif c in ('V', 'v'):
            dy = sc.num()
            y = dy if c == 'V' else y + dy
            cur.append((x, y)); prev_ctrl = None
        elif c in ('C', 'c'):
            x1, y1, x2, y2, x3, y3 = sc.nums(6)
            if c == 'c':
                x1, y1, x2, y2, x3, y3 = x + x1, y + y1, x + x2, y + y2, x + x3, y + y3
            cur += bez((x, y), (x1, y1), (x2, y2), (x3, y3))
            x, y = x3, y3
            prev_ctrl = (x2, y2)
        elif c in ('S', 's'):
            x2, y2, x3, y3 = sc.nums(4)
            if c == 's':
                x2, y2, x3, y3 = x + x2, y + y2, x + x3, y + y3
            x1, y1 = (2 * x - prev_ctrl[0], 2 * y - prev_ctrl[1]) if prev_ctrl else (x, y)
            cur += bez((x, y), (x1, y1), (x2, y2), (x3, y3))
            x, y = x3, y3
            prev_ctrl = (x2, y2)
        elif c in ('Q', 'q'):
            x1, y1, x3, y3 = sc.nums(4)
            if c == 'q':
                x1, y1, x3, y3 = x + x1, y + y1, x + x3, y + y3
            cur += bez((x, y), (x + 2 / 3 * (x1 - x), y + 2 / 3 * (y1 - y)),
                       (x3 + 2 / 3 * (x1 - x3), y3 + 2 / 3 * (y1 - y3)), (x3, y3))
            x, y = x3, y3
            prev_ctrl = (x1, y1)
        elif c in ('T', 't'):
            x3, y3 = sc.nums(2)
            if c == 't':
                x3, y3 = x + x3, y + y3
            x1, y1 = (2 * x - prev_ctrl[0], 2 * y - prev_ctrl[1]) if prev_ctrl else (x, y)
            cur += bez((x, y), (x + 2 / 3 * (x1 - x), y + 2 / 3 * (y1 - y)),
                       (x3 + 2 / 3 * (x1 - x3), y3 + 2 / 3 * (y1 - y3)), (x3, y3))
            x, y = x3, y3
            prev_ctrl = (x1, y1)
        elif c in ('A', 'a'):
            rx, ry = sc.nums(2)
            phi = sc.num()
            laf = sc.flag(); sweep = sc.flag()
            x3, y3 = sc.nums(2)
            if c == 'a':
                x3, y3 = x + x3, y + y3
            cur += arc_to_bezier((x, y), rx, ry, phi, laf, sweep, (x3, y3))
            x, y = x3, y3
            prev_ctrl = None
        elif c in ('Z', 'z'):
            cur.append((sx, sy)); x, y = sx, sy
            prev_ctrl = None
        else:
            break
    if cur:
        subpaths.append(cur)
    return subpaths


def extract_group(svg, gid, nth=0):
    starts = [m.start() for m in re.finditer(r'<g id="' + re.escape(gid) + r'"[^>]*>', svg)]
    start = starts[nth]
    depth, end = 0, None
    for mm in re.finditer(r'<g[^>]*/>|<g[^>]*>|</g>', svg[start:start + 600000]):
        tag = mm.group(0)
        if tag.startswith('<g') and not tag.endswith('/>'):
            depth += 1
        elif tag == '</g>':
            depth -= 1
            if depth == 0:
                end = start + mm.end(); break
    return svg[start:end]


def group_paths(seg, want_stroke=None):
    out = []
    for m in re.finditer(r'<path\b([^>]*)/>', seg):
        attrs = m.group(1)
        dm = re.search(r' d="([^"]+)"', attrs)
        if not dm:
            continue
        if want_stroke and f'stroke="{want_stroke}"' not in attrs:
            continue
        try:
            parsed = parse_path(dm.group(1))
        except Exception as e:
            print('PARSE FAIL:', e, '| d=', repr(dm.group(1)[:200]), '| tag attrs=', repr(attrs[:200]))
            continue
        for sp in parsed:
            if len(sp) >= 2:
                out.append(sp)
    return out


# ------------------------------------------------------------------ fit (graticule)
# The reference map draws its own latitude/longitude graticule with printed degree labels
# (parallels at 8,12,16,20,23.5,24,28,32,36 N; meridians at 68,72,76,80,84,88,92,96 E). Each
# gridline is close to straight but not exactly (a mild conic-style curvature), so instead of
# assuming a simple axis-aligned scale we compute every parallel x meridian INTERSECTION —
# an exact, known (lon, lat) at a precise reference-SVG point — and fit a 6-param affine
# through those. That gives ref_svg -> (lon, lat); composed with our own map's existing
# (lon, lat) -> our_svg affine (projection_fit.json, median residual 0.55 units), we get
# ref_svg -> our_svg without ever needing to match ambiguous boundary shapes between the
# two drawings.
PARALLELS = {8: 18, 12: 17, 16: 16, 20: 15, 23.5: 14, 24: 13, 28: 12, 32: 11, 36: 10}
MERIDIANS = {68: 7, 72: 5, 76: 4, 80: 3, 84: 2, 88: 1, 92: 0, 96: 8}
MERIDIAN_EXTRA = {68: [6]}   # extra clipped fragments that continue a meridian line


def cmd_fit():
    import numpy as np

    ref_svg = open(REF, encoding='utf-8', errors='replace').read()
    seg = extract_group(ref_svg, 'lines')
    path_ds = [re.search(r' d="([^"]*)"', a).group(1) for a in re.findall(r'<path\b([^>]*)/>', seg)]
    lines = [parse_path(d)[0] for d in path_ds]

    def curve(idx_list):
        pts = []
        for i in idx_list:
            pts += lines[i]
        return LineString(pts)

    parallels = {lat: curve([i] + MERIDIAN_EXTRA.get(lat, [])) for lat, i in PARALLELS.items()}
    meridians = {lon: curve([i] + MERIDIAN_EXTRA.get(lon, [])) for lon, i in MERIDIANS.items()}

    corr = []   # (lon, lat, ref_x, ref_y)
    for lon, mline in meridians.items():
        for lat, pline in parallels.items():
            pt = mline.intersection(pline)
            if pt.is_empty or pt.geom_type != 'Point':
                continue
            corr.append((lon, lat, pt.x, pt.y))
    print(f'{len(corr)} graticule intersections found (of up to {len(meridians) * len(parallels)})')

    lon = np.array([c[0] for c in corr]); lat = np.array([c[1] for c in corr])
    rx = np.array([c[2] for c in corr]); ry = np.array([c[3] for c in corr])

    # Quadratic in (lon, lat): captures this map's mild conic curvature almost exactly,
    # where a plain affine left a ~20-unit residual (the graticule visibly bows inward).
    def design(lo, la):
        return np.c_[np.ones_like(lo), lo, la, lo * lo, lo * la, la * la]
    A = design(lon, lat)
    px = np.linalg.lstsq(A, rx, rcond=None)[0]
    py = np.linalg.lstsq(A, ry, rcond=None)[0]
    pred = np.c_[A @ px, A @ py]
    res = np.hypot(pred[:, 0] - rx, pred[:, 1] - ry)
    print(f'(lon,lat)->ref_svg quadratic fit residual: median {np.median(res):.3f}  max {res.max():.3f} ref-svg units')

    our_affine = json.load(open(os.path.join(HERE, 'projection_fit.json')))['affine']
    json.dump({'ref_px': list(px), 'ref_py': list(py), 'our_affine': our_affine,
               'residual_ref_units': float(np.median(res)),
               'lon_range': [float(lon.min()), float(lon.max())],
               'lat_range': [float(lat.min()), float(lat.max())]}, open(FIT, 'w'))
    print('wrote', FIT)


def load_fit():
    if not os.path.exists(FIT):
        raise SystemExit('run  python ref_extract.py fit  first')
    return json.load(open(FIT))


def to_our(pt, fit):
    """Reference-SVG (x, y) -> our SVG (x, y), via inverting the quadratic ref fit to get
    (lon, lat), then applying our map's own affine. The inversion uses a few Newton steps
    from an affine-based initial guess (cheap and exact enough: the quadratic is smooth and
    the initial guess is already close)."""
    import numpy as np
    px, py = np.array(fit['ref_px']), np.array(fit['ref_py'])
    x, y = pt

    def F(lo, la):
        d = np.array([1, lo, la, lo * lo, lo * la, la * la])
        return d @ px - x, d @ py - y

    def J(lo, la):
        # partials of [f, g] wrt [lo, la]
        dfx = px[1] + 2 * px[3] * lo + px[4] * la
        dfy = px[2] + px[4] * lo + 2 * px[5] * la
        dgx = py[1] + 2 * py[3] * lo + py[4] * la
        dgy = py[2] + py[4] * lo + 2 * py[5] * la
        return dfx, dfy, dgx, dgy

    lo, la = sum(fit['lon_range']) / 2, sum(fit['lat_range']) / 2   # initial guess
    for _ in range(8):
        f, g = F(lo, la)
        a, b, c, d = J(lo, la)
        det = a * d - b * c
        if abs(det) < 1e-12:
            break
        dlo = (d * f - b * g) / det
        dla = (-c * f + a * g) / det
        lo -= dlo; la -= dla
        if abs(dlo) < 1e-6 and abs(dla) < 1e-6:
            break
    A, B, C, D, E, Fc = fit['our_affine']
    return (A * lo + B * la + C, D * lo + E * la + Fc)


# ------------------------------------------------------------------ labels
def get_labels():
    ref_svg = open(REF, encoding='utf-8', errors='replace').read()
    seg = extract_group(ref_svg, 'riv')
    pairs = re.findall(r'<path fill="none" d="([^"]+)"/>\s*<text[^>]*>(.*?)</text>', seg, flags=re.S)
    labels = []
    for d, txt in pairs:
        name = ''.join(re.findall(r'<tspan[^>]*>([^<]*)</tspan>', txt))
        key = name.strip().lower()
        if key in NOT_RIVERS:
            continue
        subpaths = parse_path(d)
        pts = [p for sp in subpaths for p in sp]
        mid = pts[len(pts) // 2]
        labels.append({'raw': name, 'mid': mid, 'pts': pts})
    return labels


def cmd_list():
    for lab in get_labels():
        print(lab['raw'])
    print(len(get_labels()), 'river labels')


# ------------------------------------------------------------------ build (match + transform + clip)
def our_country_polygon():
    """India's outline, in our SVG's coordinate space, buffered by ~11 km. Reuses
    river_tool.py's proven india_clip() (Natural Earth's India polygon, in lon/lat,
    already buffered by 0.10 deg) and reprojects it with our own (lon,lat)->our_svg
    affine — far more reliable than trying to polygonize our own hand-drawn border
    line-work, which is stored as many small disjoint segments, not one closed ring."""
    from shapely.geometry import Polygon
    import river_tool
    ll_poly = river_tool.india_clip()
    our_affine = load_fit()['our_affine']

    def ring_to_our(coords):
        return [((our_affine[0] * lo + our_affine[1] * la + our_affine[2]),
                 (our_affine[3] * lo + our_affine[4] * la + our_affine[5])) for lo, la in coords]
    polys = ll_poly.geoms if hasattr(ll_poly, 'geoms') else [ll_poly]
    out = [Polygon(ring_to_our(p.exterior.coords), [ring_to_our(r.coords) for r in p.interiors]) for p in polys]
    return unary_union(out)


def cmd_build():
    fit = load_fit()
    ref_svg = open(REF, encoding='utf-8', errors='replace').read()

    river_paths = group_paths(extract_group(ref_svg, 'rivers'), want_stroke='#0074E8')
    print(f'{len(river_paths)} raw line-work subpaths in the "rivers" group')

    lines_our = [LineString([to_our(p, fit) for p in sp]) for sp in river_paths if len(sp) >= 2]

    labels = get_labels()
    # Several rivers are labelled twice (once near the source, once near the mouth); group by
    # name up front so both labels' matched segments land in the same output river, and so a
    # name never collides with itself when two labels compete for the same nearby segment.
    for lab in labels:
        lab['key'] = lab['raw'].strip().lower()
    guides = [LineString([to_our(p, fit) for p in lab['pts']]) if len(lab['pts']) >= 2 else None for lab in labels]
    mids = [Point(to_our(lab['mid'], fit)) for lab in labels]

    # Assign each raw segment to the label(s) whose guide curve runs closest to it. At a
    # confluence, the junction segment sits almost equidistant between a river and its
    # tributary (sometimes distance 0 either way) — assigning it to only the single nearest
    # name left several rivers (Ganga among them) with no seed at all, every contact point
    # having been won by a tributary by a fraction of a unit. So a segment near-tied between
    # two or more labels (within TIE_MARGIN of the best) seeds all of them; harmless, since a
    # shared confluence pixel drawn under two names is visually identical to drawing it once.
    TIE_MARGIN = 3.0
    label_tree = STRtree(guides)
    assigned = [set() for _ in lines_our]
    for i, ln in enumerate(lines_our):
        # Buffer the whole segment, not just its midpoint — a long segment's closest
        # approach to a label's guide is often near one end, not its centre.
        cand = list(label_tree.query(ln.buffer(70))) or range(len(labels))
        dists = [(guides[li].distance(ln) if guides[li] else mids[li].distance(ln), li) for li in cand]
        dists.sort()
        if dists and dists[0][0] < 55:
            best_d = dists[0][0]
            assigned[i] = {li for d, li in dists if d <= best_d + TIE_MARGIN and d < 55}

    # Grow assignments to neighbouring unassigned segments that touch an assigned one
    # (shared endpoint), so a river keeps the parts its label doesn't sit directly on.
    endpoints = [(ln.coords[0], ln.coords[-1]) for ln in lines_our]

    def close(a, b, tol=1.2):
        return math.hypot(a[0] - b[0], a[1] - b[1]) < tol

    changed, guard = True, 0
    while changed and guard < 25:
        changed = False; guard += 1
        for i in range(len(lines_our)):
            for j in range(len(lines_our)):
                if not assigned[j] or i == j or assigned[j] <= assigned[i]:
                    continue
                if any(close(pi, pj) for pi in endpoints[i] for pj in endpoints[j]):
                    before = len(assigned[i])
                    assigned[i] |= assigned[j]
                    if len(assigned[i]) > before:
                        changed = True

    by_key = {}
    for i, lis in enumerate(assigned):
        for li in lis:
            by_key.setdefault(labels[li]['key'], []).append(lines_our[i])
    n_unassigned = sum(not a for a in assigned)
    print(f'{len(by_key)} distinct river names matched to line-work; '
          f'{n_unassigned}/{len(lines_our)} segments unmatched '
          f'(len {sum(l.length for i, l in enumerate(lines_our) if not assigned[i]):.0f} units)')

    clip = our_country_polygon()
    seen_keys, out = set(), []
    for lab in labels:
        key = lab['key']
        if key in seen_keys:
            continue
        seen_keys.add(key)
        segs = by_key.get(key)
        if not segs:
            print('  NO GEOMETRY:', lab['raw']); continue
        # Rivers are drawn as many short, disjoint hand-fit curve pieces (not one continuous
        # path per river even in the source file), so keep them as separate pieces rather
        # than forcing linemerge, which fails on anything that isn't exactly end-to-end.
        parts = []
        for seg in segs:
            inside = seg.intersection(clip)
            geoms = getattr(inside, 'geoms', None) or [inside]
            parts += [g for g in geoms if g.geom_type == 'LineString' and g.length > 1]
        if not parts:
            print('  CLIPPED AWAY:', lab['raw']); continue
        name = RENAME.get(key, QUALIFY.get(key, lab['raw'].strip()))
        out.append({'name': name, 'raw': lab['raw'],
                    'paths': [[[round(x, 1), round(y, 1)] for x, y in p.simplify(0.3).coords] for p in parts],
                    'length_units': sum(p.length for p in parts)})
    json.dump(out, open(os.path.join(HERE, 'ref_rivers.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print(f'wrote ref_rivers.json: {len(out)} named rivers')
    for r in sorted(out, key=lambda r: -r['length_units']):
        print(f"  {r['name']:<26} {r['length_units'] * 3.3:>6.0f} km  ({len(r['paths'])} pieces)")


# ------------------------------------------------------------------ preview
def cmd_preview(bbox=None):
    data = json.load(open(os.path.join(HERE, 'ref_rivers.json'), encoding='utf-8'))
    svg = re.sub(r'<metadata>.*?</metadata>', '', open(OUR, encoding='utf-8').read(), flags=re.S)
    inner = re.search(r'<svg[^>]*>(.*)</svg>', svg, flags=re.S).group(1)
    x0, y0, x1, y1 = bbox or (0, 0, 1028, 1152.3)
    k = (x1 - x0) / 1028
    layers = []
    for r in data:
        for p in r['paths']:
            d = 'M' + 'L'.join(f'{x} {y}' for x, y in p)
            layers.append(f'<path d="{d}" fill="none" stroke="#1565c0" stroke-width="{1.1 * max(k, 0.3):.2f}" stroke-linecap="round" stroke-linejoin="round"/>')
        longest = max(r['paths'], key=lambda p: LineString(p).length)
        mx, my = longest[len(longest) // 2]
        fs = 8.5 * max(k, 0.3)
        layers.append(f'<text x="{mx}" y="{my}" font-size="{fs:.1f}" font-family="Arial" fill="#b00020" '
                      f'stroke="#fff" stroke-width="{fs / 4:.2f}" paint-order="stroke">{r["name"]}</text>')
    W = 1500
    H = int(W * (y1 - y0) / (x1 - x0))
    page = (f'<html><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {x1 - x0} {y1 - y0}" '
            f'width="{W}" height="{H}">{inner}{"".join(layers)}</svg></body></html>')
    html_path = os.path.join(HERE, 'preview_ref.html')
    png_path = os.path.join(HERE, 'preview_ref.png')
    open(html_path, 'w', encoding='utf-8').write(page)
    chrome = r'C:/Program Files/Google/Chrome/Application/chrome.exe'
    prof = os.path.join(os.environ.get('TEMP', HERE), 'chrome-river-ref')
    subprocess.run([chrome, '--headless=new', '--disable-gpu', '--hide-scrollbars', f'--user-data-dir={prof}',
                    f'--screenshot={png_path}', f'--window-size={W},{H}',
                    'file:///' + html_path.replace(os.sep, '/')], capture_output=True, timeout=120)
    print(png_path)


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit()
    cmd = args[0]
    if cmd == 'fit':
        cmd_fit()
    elif cmd == 'list':
        cmd_list()
    elif cmd == 'build':
        cmd_build()
    elif cmd == 'preview':
        bb = None
        if '--bbox' in args:
            bb = tuple(map(float, args[args.index('--bbox') + 1].split(',')))
        cmd_preview(bb)
    else:
        print(__doc__)
