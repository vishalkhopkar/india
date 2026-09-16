import json, re, math
import numpy as np
from scipy.spatial import cKDTree
svg = open('../../india-borders.svg', encoding='utf-8').read()
svg = re.sub(r'<metadata>.*?</metadata>', '', svg, flags=re.S)
groups = re.findall(r'<g ([^>]*)>(.*?)</g>', svg, flags=re.S)
S = []
for attrs, body in groups:
    if '#9a9a9a' in attrs or 'dasharray' in attrs:  # skip internal + de facto lines
        continue
    for d in re.findall(r'd="([^"]*)"', body):
        S += [tuple(map(float, p.split())) for p in re.findall(r'-?[\d.]+ -?[\d.]+', d)]
S = np.array(S)
ind = json.load(open('data/ind.geojson', encoding='utf-8'))
feat = [f for f in ind['features'] if f['properties'].get('ADM0_A3_IN') == 'IND' or f['properties'].get('ADM0_A3') == 'IND'][0]
N = []
geom = feat['geometry']
polys = geom['coordinates'] if geom['type'] == 'MultiPolygon' else [geom['coordinates']]
for poly in polys:
    for ring in poly:
        N += ring
N = np.array(N)
# densify NE vertices is not needed (10m is dense). Initial guess:
def proj(P, prm):
    lon, lat = P[:, 0], P[:, 1]
    a, b, c, d, e, f = prm
    return np.c_[a * lon + b * lat + c, d * lon + e * lat + f]
prm = [33.6, 0, -67.54 * 33.6, 0, -37.1, 37.46 * 37.1]
treeinit = None
for it in range(30):
    Q = proj(N, prm)
    tree = cKDTree(Q)
    dist, idx = tree.query(S)
    keep = dist < np.percentile(dist, 90)
    A = np.c_[N[idx[keep]], np.ones(keep.sum())]
    px = np.linalg.lstsq(A, S[keep, 0], rcond=None)[0]
    py = np.linalg.lstsq(A, S[keep, 1], rcond=None)[0]
    prm = [px[0], px[1], px[2], py[0], py[1], py[2]]
Q = proj(N, prm); dist, idx = cKDTree(Q).query(S)
print('affine', [round(v, 5) for v in prm])
print('residual units: median %.2f p90 %.2f max %.2f' % (np.median(dist), np.percentile(dist, 90), dist.max()))
# try y = e*mercator(lat)+f (check if Mercator-like)
merc = lambda lat: np.degrees(np.log(np.tan(np.pi / 4 + np.radians(lat) / 2)))
N2 = N.copy(); N2[:, 1] = merc(N[:, 1])
prm2 = prm[:]
for it in range(30):
    Q = proj(N2, prm2); dist2, idx = cKDTree(Q).query(S)
    keep = dist2 < np.percentile(dist2, 90)
    A = np.c_[N2[idx[keep]], np.ones(keep.sum())]
    px = np.linalg.lstsq(A, S[keep, 0], rcond=None)[0]; py = np.linalg.lstsq(A, S[keep, 1], rcond=None)[0]
    prm2 = [px[0], px[1], px[2], py[0], py[1], py[2]]
Q = proj(N2, prm2); dist2, _ = cKDTree(Q).query(S)
print('mercator-y', [round(v, 5) for v in prm2])
print('residual units: median %.2f p90 %.2f max %.2f' % (np.median(dist2), np.percentile(dist2, 90), dist2.max()))
json.dump({'affine': prm, 'mercator': prm2, 'res_affine': float(np.median(dist)), 'res_merc': float(np.median(dist2))}, open('projection_fit.json', 'w'), indent=1)
