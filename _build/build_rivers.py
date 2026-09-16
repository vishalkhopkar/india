"""Build india-rivers.html: the SVG inlined verbatim, with external borders, LoC/LAC
and rivers shown by default, and state/UT borders behind a toggle. No hover or border
history here — see build.py / india-borders.html for that."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/') + '/'   # this _build folder
ROOT = os.path.dirname(HERE.rstrip('/')) + '/'                                # the project folder

sys.path.insert(0, HERE)
from common import load_svg, label_data, load_rivers

svg = load_svg(ROOT)
data = {'labels': label_data(), 'rivers': load_rivers(HERE + 'rivers/')}
data_json = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

page = open(HERE + 'template_rivers.html', encoding='utf-8').read()
page = page.replace('<!--SVG-->', svg).replace('/*DATA*/null', data_json)
open(ROOT + 'india-rivers.html', 'w', encoding='utf-8', newline='\n').write(page)
print('ok', len(page))
