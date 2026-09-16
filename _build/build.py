"""Build india-borders.html: the SVG inlined verbatim + border history + labels."""
import re, json, html

import os
HERE = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/') + '/'   # this _build folder
ROOT = os.path.dirname(HERE.rstrip('/')) + '/'                                # the project folder

svg = open(ROOT + 'india-borders.svg', encoding='utf-8').read().strip()
matrix = open(ROOT + 'india-border-provenance-matrix-sourced.html', encoding='utf-8').read()

# ---------------------------------------------------------------- history text
history = {}
for a, b, body in re.findall(
        r'<td class="border-cell" data-a="([^"]*)" data-b="([^"]*)" tabindex="0">(.*?)</td>', matrix, flags=re.S):
    key = '|'.join(sorted([html.unescape(a), html.unescape(b)]))
    text = re.search(r'<div class="celltext">(.*?)</div>', body, flags=re.S).group(1).strip()
    src = re.search(r'<div class="source">(.*?)</div>', body, flags=re.S)
    history[key] = {'text': text, 'source': src.group(1).strip() if src else ''}
assert len(history) == 93, len(history)

refs = re.search(r'<ol>.*?</ol>', matrix, flags=re.S).group(0)

# ------------------------------------------ extra references and timelines
# Timelines and their references live in timelines.py. New references are
# numbered after the matrix's own [1]-[35], in the order they are defined there.
import sys
sys.path.insert(0, HERE)
from timelines import REFS, TIMELINES

cited = {k for items in TIMELINES.values() for _w, _t, keys in items for k in keys}
unknown = {k for k in cited if not re.fullmatch(r'm\d+', k) and k not in REFS}
assert not unknown, unknown
REF_NO = {k: 36 + i for i, k in enumerate(k for k in REFS if k in cited)}
for k in cited:
    if re.fullmatch(r'm\d+', k):
        REF_NO[k] = int(k[1:])
refs = refs.replace('</ol>', ''.join(
    f'<li id="ref-{REF_NO[key]}"><strong>{title}</strong> — {desc} '
    f'<a href="{url}" rel="noopener noreferrer" target="_blank">Source</a></li>'
    for key, (title, desc, url) in REFS.items() if key in REF_NO) + '</ol>')

def cite(keys):
    nums = sorted({REF_NO[k] for k in keys})
    return '<sup class="ref">' + ''.join(f'<a href="#ref-{n}">[{n}]</a>' for n in nums) + '</sup>'

RENDERED_TIMELINES = {
    key: [(when, f'{text} {cite(keys)}' if keys else text) for when, text, keys in items]
    for key, items in TIMELINES.items()
}

# ------------------------------------------------ which pair each SVG line is
# Paths inside each SVG layer are in alphabetical order of the pair (verified
# against the geometry: every line was matched to the regions on its two sides).
INTERNAL = [
    'Andhra Pradesh|Chhattisgarh', 'Andhra Pradesh|Karnataka', 'Andhra Pradesh|Odisha',
    'Andhra Pradesh|Puducherry', 'Andhra Pradesh|Tamil Nadu', 'Andhra Pradesh|Telangana',
    'Arunachal Pradesh|Assam', 'Arunachal Pradesh|Nagaland', 'Assam|Manipur', 'Assam|Meghalaya',
    'Assam|Mizoram', 'Assam|Nagaland', 'Assam|Tripura', 'Assam|West Bengal', 'Bihar|Jharkhand',
    'Bihar|Uttar Pradesh', 'Bihar|West Bengal', 'Chandigarh|Haryana', 'Chandigarh|Punjab',
    'Chhattisgarh|Jharkhand', 'Chhattisgarh|Madhya Pradesh', 'Chhattisgarh|Maharashtra',
    'Chhattisgarh|Odisha', 'Chhattisgarh|Telangana', 'Chhattisgarh|Uttar Pradesh',
    'Dadra and Nagar Haveli and Daman and Diu|Gujarat', 'Dadra and Nagar Haveli and Daman and Diu|Maharashtra',
    'Delhi (NCT)|Haryana', 'Delhi (NCT)|Uttar Pradesh', 'Goa|Karnataka', 'Goa|Maharashtra',
    'Gujarat|Madhya Pradesh', 'Gujarat|Maharashtra', 'Gujarat|Rajasthan', 'Haryana|Himachal Pradesh',
    'Haryana|Punjab', 'Haryana|Rajasthan', 'Haryana|Uttar Pradesh', 'Himachal Pradesh|Jammu and Kashmir (UT)',
    'Himachal Pradesh|Ladakh', 'Himachal Pradesh|Punjab', 'Himachal Pradesh|Uttarakhand',
    'Jammu and Kashmir (UT)|Ladakh', 'Jammu and Kashmir (UT)|Punjab', 'Jharkhand|Odisha',
    'Jharkhand|Uttar Pradesh', 'Jharkhand|West Bengal', 'Karnataka|Kerala', 'Karnataka|Maharashtra',
    'Karnataka|Tamil Nadu', 'Karnataka|Telangana', 'Kerala|Puducherry', 'Kerala|Tamil Nadu',
    'Madhya Pradesh|Maharashtra', 'Madhya Pradesh|Rajasthan', 'Madhya Pradesh|Uttar Pradesh',
    'Maharashtra|Telangana', 'Manipur|Mizoram', 'Manipur|Nagaland', 'Mizoram|Tripura',
    'Odisha|West Bengal', 'Puducherry|Tamil Nadu', 'Punjab|Rajasthan', 'Rajasthan|Uttar Pradesh',
    'Sikkim|West Bengal', 'Uttar Pradesh|Uttarakhand',
]
EXTERNAL = [
    'Arunachal Pradesh|Bhutan', 'Arunachal Pradesh|China', 'Arunachal Pradesh|Myanmar',
    'Assam|Bangladesh', 'Assam|Bhutan', 'Bihar|Nepal', 'Gujarat|Pakistan', 'Himachal Pradesh|China',
    'Jammu and Kashmir (UT)|Pakistan', 'Ladakh|Afghanistan', 'Ladakh|China', 'Ladakh|Pakistan',
    'Manipur|Myanmar', 'Meghalaya|Bangladesh', 'Mizoram|Bangladesh', 'Mizoram|Myanmar',
    'Nagaland|Myanmar', 'Punjab|Pakistan', 'Rajasthan|Pakistan', 'Sikkim|Bhutan', 'Sikkim|China',
    'Sikkim|Nepal', 'Tripura|Bangladesh', 'Uttar Pradesh|Nepal', 'Uttarakhand|China',
    'Uttarakhand|Nepal', 'West Bengal|Bangladesh', 'West Bengal|Bhutan', 'West Bengal|Nepal',
]
assert len(INTERNAL) == 66 and len(EXTERNAL) == 29

# Text for lines the matrix has no entry for.
EXTRA = {
    'Chhattisgarh|Uttar Pradesh': (
        'Until 2000 this stretch was part of the Uttar Pradesh–Madhya Pradesh boundary; the '
        '<strong>Madhya Pradesh Reorganisation Act, 2000</strong> carved out Chhattisgarh and turned '
        'it into the UP–Chhattisgarh border. Before independence it separated the United Provinces’ '
        'Mirzapur district from the princely state of <strong>Surguja</strong>.'),
    'Afghanistan|Ladakh': (
        'The frontier with Afghanistan’s <strong>Wakhan Corridor</strong>, a strip left between British '
        'India and the Russian Empire: its southern edge follows the Hindu Kush watershed accepted in the '
        '<strong>Durand Agreement, 1893</strong>, and its northern edge was fixed by the '
        '<strong>Anglo-Russian Pamir agreement, 1895</strong>. India counts this ~106 km border through '
        'the Gilgit region of the former princely state of Jammu and Kashmir, which is administered '
        'by Pakistan as Gilgit-Baltistan.'),
}
CLAIM_NOTE = {
    'Jammu and Kashmir (UT)|Pakistan': 'This line is the boundary as claimed by India. The de facto line is the dotted Line of Control, which the text below describes.',
    'Ladakh|Pakistan': 'This line is the boundary as claimed by India. Gilgit-Baltistan, on India’s side of it, is administered by Pakistan.',
    'Ladakh|China': 'This line is the boundary as claimed by India. Parts of the territory on India’s side of it are administered by China (Aksai Chin, the Shaksgam Valley) and Pakistan (Gilgit-Baltistan).',
    'Afghanistan|Ladakh': 'This line is the boundary as claimed by India; the area on India’s side of it is administered by Pakistan as Gilgit-Baltistan.',
}

def entry(pair, kind, part=None, tag=None, title=None, note=None, text_from=None):
    a, b = pair.split('|')
    key = '|'.join(sorted([a, b]))
    e = {'a': a, 'b': b, 'kind': kind}
    src = '|'.join(sorted(text_from.split('|'))) if text_from else key
    if src in history:
        e.update(history[src])
        if text_from:
            e['from'] = text_from.replace('|', ' – ')
    else:
        e['text'] = EXTRA[src]
    if kind == 'external' and key in CLAIM_NOTE:
        e['note'] = CLAIM_NOTE[key]
    if key in RENDERED_TIMELINES:
        e['timeline'] = RENDERED_TIMELINES[key]
    for k, v in (('part', part), ('tag', tag), ('title', title), ('note', note)):
        if v is not None:
            e[k] = v
    return e

# Some SVG paths hold more than one border. They are cut into parts, each given as
# [sub-path index, first vertex, last vertex (None = to the end)]. Vertices were
# located by converting the SVG to latitude/longitude (the map is equirectangular:
# lon = 67.54 + x / 33.6, lat = 37.46 - y / 37.1, checked against Puducherry,
# Karaikal, Mahé, Yanam, Delhi, Chandigarh, NJ9842, Indira Col and Karakoram Pass).
SHAKSGAM_NOTE = ('Both sides of this line are claimed by India as part of Ladakh. Pakistan administers '
                 'Gilgit-Baltistan; China administers the Shaksgam Valley, ceded to it by Pakistan in 1963.')
external = [entry(p, 'external') for p in EXTERNAL]
external[11] = [   # Ladakh's north-western claim line
    entry('Ladakh|Pakistan', 'external', part=[0, 0, None]),      # Gilgit-Baltistan – Khyber Pakhtunkhwa
    entry('Ladakh|Afghanistan', 'external', part=[1, 0, 3]),      # rest of the Wakhan, to the Wakhjir Pass tripoint
    entry('Ladakh|China', 'external', part=[1, 3, None]),         # Kilik – Mintaka – Khunjerab
]
dotted = [[   # the dotted layer is a single <path>
    entry('Ladakh|Pakistan', 'defacto', part=[0, 0, 13], title='Gilgit-Baltistan – Shaksgam Valley',
          tag='De facto Pakistan–China line', note=SHAKSGAM_NOTE, text_from='Ladakh|Pakistan'),
    entry('Ladakh|Pakistan', 'defacto', part=[0, 13, 15], tag='De facto line · Siachen',
          note='The stretch between NJ9842 and Indira Col, beyond the end of the Line of Control.'),
    entry('Ladakh|Pakistan', 'loc', part=[0, 15, 27]),                         # NJ9842 → J&K–Ladakh boundary
    entry('Jammu and Kashmir (UT)|Pakistan', 'loc', part=[0, 27, None]),       # → Jammu
    entry('Ladakh|Pakistan', 'defacto', part=[1, 0, None], title='Gilgit-Baltistan – Shaksgam Valley',
          tag='De facto Pakistan–China line', note=SHAKSGAM_NOTE, text_from='Ladakh|Pakistan'),
    entry('Ladakh|China', 'defacto', part=[2, 0, None], tag='De facto line · Siachen–Shaksgam',
          note='India holds the Siachen side; the Shaksgam Valley beyond is claimed by India and administered by China.',
          text_from='Ladakh|Pakistan'),
    entry('Ladakh|China', 'lac', part=[3, 0, None]),
    entry('Ladakh|China', 'lac', part=[4, 0, None]),
]]

borders = {
    'internal': [entry(p, 'internal') for p in INTERNAL],
    'external': external,
    'loc-lac': dotted,
}
flat = [e for v in borders.values() for x in v for e in (x if isinstance(x, list) else [x])]
used = {'|'.join(sorted([e['a'], e['b']])) for e in flat}
missing = set(history) - used
assert not missing, missing

# ------------------------------------------------------------------- labels
# x, y in SVG user units. lead = point the leader line points at.
S, U, C, SUB = 'state', 'ut', 'country', 'sub'
labels = [
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
label_data = []
for lab in labels:
    cls, text, x, y, *leads = lab
    label_data.append({'cls': cls, 'text': text, 'x': x, 'y': y, 'leads': leads})

# ------------------------------------------------------------------- rivers
# rivers/<system>.json files are produced by rivers/river_tool.py (one per river system).
rivers, river_owner = [], {}
RIVER_DIR = HERE + 'rivers/'
for fn in sorted(os.listdir(RIVER_DIR)) if os.path.isdir(RIVER_DIR) else []:
    if not fn.endswith('.json') or fn.endswith('.spec.json') or fn == 'projection_fit.json':
        continue
    sysdata = json.load(open(RIVER_DIR + fn, encoding='utf-8'))
    if not isinstance(sysdata, dict) or 'rivers' not in sysdata or sysdata.get('system') == 'test':
        continue
    for r in sysdata['rivers']:
        key = r['name'].lower()
        assert key not in river_owner, f"river {r['name']} drawn in both {river_owner[key]} and {fn}"
        river_owner[key] = fn
        d = ''.join('M' + 'L'.join(f'{x:g} {y:g}' for x, y in p) for p in r['paths'])
        rivers.append({'n': r['name'], 'r': r['rank'], 's': sysdata['title'], 'd': d})
rivers.sort(key=lambda r: -r['r'])          # minor rivers first, main rivers drawn on top

data = {'borders': borders, 'labels': label_data, 'rivers': rivers}
data_json = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

page = open(HERE + 'template.html', encoding='utf-8').read()
page = page.replace('<!--SVG-->', svg).replace('/*DATA*/null', data_json).replace('<!--REFS-->', refs)
open(ROOT + 'india-borders.html', 'w', encoding='utf-8', newline='\n').write(page)
print('ok', len(page))
