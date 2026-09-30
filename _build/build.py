"""Build india-borders.html: the drawn map, border history, labels and rivers as data files."""
import re, json, html, shutil

import os
HERE = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/') + '/'   # this _build folder
ROOT = os.path.dirname(HERE.rstrip('/')) + '/'                                # the project folder

import sys
sys.path.insert(0, HERE)
from common import load_svg, label_data, load_rivers

svg = load_svg(ROOT)
matrix = open(ROOT + 'india-border-provenance-matrix-sourced.html', encoding='utf-8').read()

# ---------------------------------------------------------------- history text
history = {}
for a, b, body in re.findall(
        r'<td class="border-cell" data-a="([^"]*)" data-b="([^"]*)" tabindex="0">(.*?)</td>', matrix, flags=re.S):
    key = '|'.join(sorted([html.unescape(a), html.unescape(b)]))
    text = re.search(r'<div class="celltext">(.*?)</div>', body, flags=re.S).group(1).strip()
    history[key] = {'text': text}
assert len(history) == 93, len(history)

refs = re.search(r'<ol>.*?</ol>', matrix, flags=re.S).group(0)

# The matrix's reference [1] is the private research note it was compiled from, which
# readers cannot see, and each cell's grey "§ Section, line N" locator points into it.
# Both are dropped: the real sources behind each summary are cited from
# timelines/<region>.js ("summaries"). The remaining matrix references move up by one
# so the list still starts at [1]; app.js maps the data files' "mN" keys to N - 1.
def renumber(html_text):
    html_text = html_text.replace('<a href="#ref-1">[1]</a>', '')
    html_text = re.sub(r'<sup class="ref">\s*</sup>', '', html_text)
    html_text = re.sub(r'#ref-(\d+)"', lambda m: f'#ref-{int(m.group(1)) - 1}"', html_text)
    return re.sub(r'>\[(\d+)\]<', lambda m: f'>[{int(m.group(1)) - 1}]<', html_text).strip()

# The matrix cites its [13], the Bengal Boundary Commission's award, on these western
# frontiers too, but they were drawn by the Punjab commission or not by Radcliffe at all
# (Sind went to Pakistan whole); their region files cite the right sources instead.
NOT_BENGAL = ['Jammu and Kashmir (UT)|Punjab', 'Pakistan|Punjab', 'Gujarat|Pakistan', 'Pakistan|Rajasthan']
for key in NOT_BENGAL:
    assert '<a href="#ref-13">[13]</a>' in history[key]['text'], key
    history[key]['text'] = history[key]['text'].replace('<a href="#ref-13">[13]</a>', '')

for h in history.values():
    assert '#ref-0"' not in renumber(h['text'])
    h['text'] = renumber(h['text'])
refs = re.sub(r'<li id="ref-1">.*?</li>', '', refs, count=1, flags=re.S)
refs = re.sub(r'<li id="ref-(\d+)"', lambda m: f'<li id="ref-{int(m.group(1)) - 1}"', refs)
assert '<li id="ref-0"' not in refs and 'User-supplied' not in refs

# The references list is the matrix's own <ol>. The timelines, the references they
# cite and their numbering now live in timelines/<region>.js, read by the page
# itself (app.js), so changing a timeline needs no rebuild.

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

# ------------------------------------------------------------------- labels + rivers
# Both shared with build_rivers.py (india-rivers.html) via common.py.
data = {'borders': borders, 'labels': label_data(), 'rivers': load_rivers(HERE + 'rivers/')}
data_json = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

# ---------------------------------------------------- data files loaded by the page
# The HTML holds only the page's own frame; the drawn map, the border/timeline/label/
# river data, the references list, the styling and the page's own script each live in
# their own file, written straight into ROOT alongside india-borders.html (edit the
# _build/ source and rebuild to update them).
#
# The map goes out as markup in a .js file rather than being fetched from
# india-borders.svg, so the page still works opened straight from disk (file://
# blocks fetch); app.js drops it into the frame.
svg_json = json.dumps(svg, ensure_ascii=False).replace('</', '<\\/')
open(ROOT + 'map.js', 'w', encoding='utf-8', newline='\n').write(f'const MAP_SVG = {svg_json};\n')
open(ROOT + 'data.js', 'w', encoding='utf-8', newline='\n').write(f'const DATA = {data_json};\n')
refs_json = json.dumps(refs, ensure_ascii=False).replace('</', '<\\/')
open(ROOT + 'references.js', 'w', encoding='utf-8', newline='\n').write(f'const REFS_HTML = {refs_json};\n')
shutil.copyfile(HERE + 'styles.css', ROOT + 'styles.css')
shutil.copyfile(HERE + 'app.js', ROOT + 'app.js')

page = open(HERE + 'template.html', encoding='utf-8').read()
open(ROOT + 'india-borders.html', 'w', encoding='utf-8', newline='\n').write(page)
print('ok', len(page))
