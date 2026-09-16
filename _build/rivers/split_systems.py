"""Split ref_rivers.json (built by ref_extract.py) into the RIVERS.md systems as SYSTEM.json,
in the format build.py already expects. Run after `python ref_extract.py build`."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))

# name -> (system, rank). Every name in ref_rivers.json must appear here exactly once.
PLAN = {
    # Indus system
    'Indus': ('indus', 1), 'Jhelum': ('indus', 2), 'Chenab': ('indus', 2),
    'Ravi': ('indus', 2), 'Beas': ('indus', 2), 'Sutlej': ('indus', 2),
    # Ganga north (main stem + northern tributaries)
    'Ganga': ('ganga_north', 1), 'Hooghly': ('ganga_north', 2), 'Gomti': ('ganga_north', 2),
    'Ghaghra': ('ganga_north', 2), 'Sharda (Mahakali)': ('ganga_north', 2),
    'Gandak': ('ganga_north', 2), 'Kosi': ('ganga_north', 2), 'Bagmati': ('ganga_north', 3),
    # Ganga south (Yamuna + southern tributaries, incl. West Bengal's Hooghly tributaries)
    'Yamuna': ('ganga_south', 1), 'Chambal': ('ganga_south', 2), 'Betwa': ('ganga_south', 2),
    'Son': ('ganga_south', 2), 'Damodar': ('ganga_south', 2), 'Banas (Rajasthan)': ('ganga_south', 3),
    'Kali Sindh': ('ganga_south', 3), 'Parbati (Chambal)': ('ganga_south', 3),
    'Shipra': ('ganga_south', 3), 'Rihand': ('ganga_south', 3), 'Kasai (Kansai)': ('ganga_south', 3),
    # Brahmaputra + north-east
    'Brahmaputra': ('brahmaputra', 1), 'Barak': ('brahmaputra', 2),
    # Godavari
    'Godavari': ('godavari', 1), 'Pranhita': ('godavari', 2), 'Wardha': ('godavari', 2),
    'Wainganga': ('godavari', 2), 'Penganga': ('godavari', 2), 'Manjira': ('godavari', 2),
    'Indravati': ('godavari', 2), 'Sabari': ('godavari', 2),
    # Krishna
    'Krishna': ('krishna', 1), 'Bhima': ('krishna', 2), 'Tungabhadra': ('krishna', 2),
    'Tunga (Tungabhadra)': ('krishna', 3), 'Bhadra (Tungabhadra)': ('krishna', 3),
    # Southern peninsula
    'Kaveri': ('south', 1), 'Kollidam': ('south', 2), 'Palar': ('south', 2),
    'Pennar': ('south', 2), 'Ponnaiyar': ('south', 2), 'Vaigai': ('south', 2),
    'Tamirabarani': ('south', 2), 'Periyar': ('south', 2), 'Chaliyar': ('south', 3),
    # Mahanadi / east coast
    'Mahanadi': ('east_central', 1), 'Baitarani': ('east_central', 2),
    'Brahmani': ('east_central', 2), 'Subarnarekha': ('east_central', 2),
    'Vamsadhara': ('east_central', 3),
    # West-flowing / desert
    'Narmada': ('west', 1), 'Tapi': ('west', 1), 'Sabarmati': ('west', 2),
    'Mahi': ('west', 2), 'Luni': ('west', 2), 'Bhadar': ('west', 3), 'Shetrunji': ('west', 3),
}

TITLES = {
    'indus': 'Indus system', 'ganga_north': 'Ganga (main stem and northern tributaries)',
    'ganga_south': 'Yamuna and Ganga southern tributaries', 'brahmaputra': 'Brahmaputra and the north-east',
    'godavari': 'Godavari system', 'krishna': 'Krishna system', 'south': 'Southern peninsula rivers',
    'east_central': 'Mahanadi and the east coast', 'west': 'West-flowing and desert rivers',
}

data = json.load(open(os.path.join(HERE, 'ref_rivers.json'), encoding='utf-8'))
missing = [r['name'] for r in data if r['name'] not in PLAN]
if missing:
    raise SystemExit(f'not assigned to a system: {missing}')
extra = set(PLAN) - {r['name'] for r in data}
if extra:
    raise SystemExit(f'planned but not in ref_rivers.json: {extra}')

by_system = {}
for r in data:
    system, rank = PLAN[r['name']]
    by_system.setdefault(system, []).append({'name': r['name'], 'rank': rank, 'paths': r['paths']})

for system, rivers in by_system.items():
    rivers.sort(key=lambda r: (r['rank'], -sum(len(p) for p in r['paths'])))
    out = {'system': system, 'title': TITLES[system], 'rivers': rivers}
    path = os.path.join(HERE, f'{system}.json')
    json.dump(out, open(path, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f'{system}.json: {len(rivers)} rivers')
