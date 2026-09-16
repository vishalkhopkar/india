"""Shared pieces used by both build.py (india-borders.html) and build_rivers.py
(india-rivers.html): the raw SVG, the place-name labels, and the river data."""
import json, os


def load_svg(root):
    return open(root + 'india-borders.svg', encoding='utf-8').read().strip()


# ------------------------------------------------------------------------- labels
# x, y in SVG user units. lead = point the leader line points at.
S, U, C, SUB = 'state', 'ut', 'country', 'sub'
LABELS = [
    # states
    (S, 'Rajasthan', 205, 392), (S, 'Gujarat', 120, 560), (S, 'Madhya\nPradesh', 400, 530),
    (S, 'Maharashtra', 262, 672), (S, 'Uttar\nPradesh', 472, 400), (S, 'Karnataka', 272, 810),
    (S, 'Andhra\nPradesh', 395, 842), (S, 'Odisha', 578, 622), (S, 'Chhattisgarh', 505, 575),
    (S, 'Tamil\nNadu', 360, 984), (S, 'Telangana', 388, 730), (S, 'Bihar', 628, 438),
    (S, 'Arunachal\nPradesh', 918, 330), (S, 'West\nBengal', 675, 545), (S, 'Assam', 845, 414),
    (S, 'Jharkhand', 590, 518), (S, 'Himachal\nPradesh', 330, 205), (S, 'Uttarakhand', 405, 278),
    (S, 'Punjab', 262, 252), (S, 'Haryana', 290, 305), (S, 'Kerala', 305, 1018),
    (S, 'Meghalaya', 790, 443), (S, 'Manipur', 890, 478), ('state lead', 'Mizoram', 905, 562, (860, 540)),
    (S, 'Nagaland', 913, 426), ('state lead end', 'Tripura', 790, 500, (816, 508)), ('state lead', 'Sikkim', 708, 336, (708, 368)),
    ('state lead end', 'Goa', 200, 824, (219, 821)),
    # union territories
    (U, 'Jammu and\nKashmir', 258, 150), (U, 'Ladakh', 335, 118),
    ('ut lead', 'Delhi', 352, 330, (323, 327)), ('ut lead end', 'Chandigarh', 302, 233, (311, 250)),
    ('ut lead', 'Puducherry', 432, 944, (414, 947)),
    ('ut lead mid', 'Dadra and\nNagar Haveli and\nDaman and Diu', 100, 695, (182, 640), (112, 621)),
    ('ut lead', 'Lakshadweep', 190, 1072, (182.5, 1082.5)), ('ut end', 'Andaman and\nNicobar Islands', 836, 1000),
    # Puducherry's other districts
    ('sub lead', 'Karaikal', 432, 987, (415, 985)), ('sub lead', 'Yanam', 512, 774, (498, 770)),
    ('sub lead end', 'Mahé', 252, 958, (268, 954)),
    # neighbours
    (C, 'Pakistan', 110, 250), ('country lead end', 'Afghanistan', 190, 14, (214, 21)), (C, 'China', 560, 200),
    (C, 'Nepal', 562, 335), (C, 'Bhutan', 782, 378), (C, 'Bangladesh', 775, 580), (C, 'Myanmar', 972, 492),
]


def label_data():
    out = []
    for lab in LABELS:
        cls, text, x, y, *leads = lab
        out.append({'cls': cls, 'text': text, 'x': x, 'y': y, 'leads': leads})
    return out


# ------------------------------------------------------------------------- rivers
# rivers/<system>.json files are produced by rivers/river_tool.py (one per river system).
def load_rivers(river_dir):
    rivers, river_owner = [], {}
    for fn in sorted(os.listdir(river_dir)) if os.path.isdir(river_dir) else []:
        if not fn.endswith('.json') or fn.endswith('.spec.json') or fn == 'projection_fit.json':
            continue
        sysdata = json.load(open(river_dir + fn, encoding='utf-8'))
        if not isinstance(sysdata, dict) or 'rivers' not in sysdata or sysdata.get('system') == 'test':
            continue
        for r in sysdata['rivers']:
            key = r['name'].lower()
            assert key not in river_owner, f"river {r['name']} drawn in both {river_owner[key]} and {fn}"
            river_owner[key] = fn
            d = ''.join('M' + 'L'.join(f'{x:g} {y:g}' for x, y in p) for p in r['paths'])
            rivers.append({'n': r['name'], 'r': r['rank'], 's': sysdata['title'], 'd': d})
    rivers.sort(key=lambda r: -r['r'])          # minor rivers first, main rivers drawn on top
    return rivers
