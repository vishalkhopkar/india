"""Border timelines and their references.

REFS: key -> (title, description, url). Keys 'm1'..'m35' refer to the matrix's own
reference list and need no entry here. New references are numbered from 36 in the
order they are defined below (only those actually cited are listed).

TIMELINES: 'A|B' (names sorted, as in the matrix) -> [(when, text, [ref keys])].
"""

REFS = {}
TIMELINES = {}


def ref(key, title, desc, url):
    assert key not in REFS, key
    REFS[key] = (title, desc, url)


def timeline(pair, *items):
    key = '|'.join(sorted(pair.split('|')))
    assert key not in TIMELINES, key
    TIMELINES[key] = list(items)


# =============================================================================
# North-west: Rajasthan, Haryana
# =============================================================================
ref('surji', 'Treaty of Surji-Anjangaon, 30 December 1803', 'Wikipedia.', 'https://en.wikipedia.org/wiki/Treaty_of_Surji-Anjangaon')
ref('delhi', 'Delhi Territory', 'Wikipedia: cession in 1803, administration under the North-Western Provinces, transfer to Punjab in 1858.', 'https://en.wikipedia.org/wiki/Delhi_Territory')
ref('alwar', 'History of Alwar', 'District &amp; Sessions Court, Alwar: treaty with the East India Company, 14 November 1803.', 'https://alwar.dcourts.gov.in/about-department/history/')
ref('loharu', 'Loharu State', 'Wikipedia.', 'https://en.wikipedia.org/wiki/Loharu_State')
ref('bhattiana', 'Bhattiana', 'Wikipedia: Bhatti chiefs, the 1818 expedition and the 1837 district.', 'https://en.wikipedia.org/wiki/Bhattiana')
ref('sirsa', 'R. Kumar &amp; S. Meena, “The Town under the Crown: The District Sirsa”', 'IJCRT 6(1), 2018, pp. 454–461; pargana history drawn from the Sirsa settlement report and Hisar gazetteer.', 'https://ijcrt.org/papers/IJCRT1705308.pdf')
ref('amritsar1809', 'Treaty of Amritsar, 25 April 1809', 'Wikipedia: the Sutlej as the limit of Ranjit Singh’s kingdom.', 'https://en.wikipedia.org/wiki/Treaty_of_Amritsar_(1809)')
ref('thomas', 'George Thomas (soldier)', 'Wikipedia: his state at Hansi, 1798–1801.', 'https://en.wikipedia.org/wiki/George_Thomas_(soldier)')
ref('rohtak', 'History of Rohtak district', 'Government of Haryana: transfer to Punjab, 13 April 1858.', 'https://rohtak.gov.in/history/')
ref('mahendragarh', 'History of Mahendragarh district', 'Government of Haryana: partition of Jhajjar and formation of the district in 1948.', 'https://mahendragarh.gov.in/history/')
ref('bikaner', 'Sardar Singh of Bikaner', 'Wikipedia: grant of the Tibi pargana, 11 April 1861.', 'https://en.wikipedia.org/wiki/Sardar_Singh_of_Bikaner')
ref('eastpunjab', 'East Punjab states: Loharu, Dujana and Pataudi', 'India State Story: Loharu’s merger agreement of 17 February 1948.', 'https://www.indiastatestory.in/post/16-east-punjab-states-loharu-dajuna-and-pataudi')
ref('matsya', 'Matsya States Union', 'Wikipedia: formed 18 March 1948, merged into Rajasthan 15 May 1949.', 'https://en.wikipedia.org/wiki/Matsya_States_Union')
ref('pepsu', 'Patiala and East Punjab States Union', 'Wikipedia: formed 1948, merged into Punjab 1 November 1956.', 'https://en.wikipedia.org/wiki/Patiala_and_East_Punjab_States_Union')
ref('whitepaper_raj', 'White Paper on Indian States (1950): The United State of Rajasthan', 'Wikisource.', 'https://en.wikisource.org/wiki/White_Paper_on_Indian_States_(1950)/Part_5/Formation_of_Unions/The_United_State_of_Rajasthan')

timeline('Haryana|Rajasthan',
    ('Before 1803', 'Contested by the Marathas, George Thomas (ruling Hisar and Rohtak from Hansi, 1798–1801), the Bhatti chiefs of Sirsa and the Sikh states of Patiala and Jind. Never part of Ranjit Singh’s empire, which the 1809 Treaty of Amritsar kept north of the Sutlej.', ['thomas', 'bhattiana', 'amritsar1809']),
    ('14 Nov 1803', 'Alwar signs a treaty with the East India Company and stays a separate state.', ['alwar']),
    ('30 Dec 1803', 'Treaty of Surji-Anjangaon: Scindia cedes Hisar, Rohtak, Rewari, Gurgaon and the Delhi region. The edge of this British “Delhi Territory” against Bikaner, Jaipur (Shekhawati) and Alwar is the origin of the line.', ['surji', 'delhi']),
    ('1803', 'Lord Lake grants Loharu to Ahmad Bakhsh Khan, creating a princely state on the British side (some sources say 1806).', ['loharu']),
    ('1818', 'The British take the Sirsa and Rania parganas from the Bhatti chiefs after an expedition against Zabita Khan.', ['bhattiana', 'sirsa']),
    ('1828', 'Darba pargana, partly colonised by the Raja of Bikaner, is resumed from him.', ['sirsa']),
    ('1837', 'Bhattiana district is formed on the Bikaner frontier.', ['bhattiana']),
    ('1858', 'After the 1857 revolt the Delhi and Hisar divisions move from the North-Western Provinces to Punjab: the line becomes the Punjab–Rajputana border. Bhattiana is renamed Sirsa district.', ['delhi', 'rohtak', 'sirsa']),
    ('1858–61', 'Jhajjar state is confiscated: Narnaul and Kanaud (Mahendragarh) go to Patiala, Bawal and Kanina to Nabha, Dadri to Jind.', ['mahendragarh']),
    ('11 Apr 1861', 'Bikaner receives the Tibi pargana, 41 villages of Sirsa district, for its help in 1857.', ['bikaner', 'sirsa']),
    ('1884', 'Sirsa district is abolished and merged into Hisar district.', ['sirsa']),
    ('17 Feb 1948', 'Loharu merges with East Punjab.', ['eastpunjab']),
    ('18 Mar 1948', 'Alwar joins the Matsya Union.', ['matsya']),
    ('1948', 'PEPSU is formed; Patiala’s Mahendragarh, Jind’s Dadri and Nabha’s Bawal become its Mahendragarh district.', ['pepsu', 'mahendragarh']),
    ('1949', 'Bikaner and Jaipur join Greater Rajasthan on 30 March; the Matsya Union (Alwar) follows on 15 May. The whole western side is now one state.', ['whitepaper_raj', 'matsya']),
    ('1 Nov 1956', 'PEPSU merges into Punjab under the States Reorganisation Act, 1956, putting the whole eastern side in Punjab.', ['m2', 'pepsu']),
    ('1 Nov 1966', 'The Punjab Reorganisation Act, 1966 creates Haryana from Punjab’s Hindi-speaking districts, including Hisar, Rohtak, Gurgaon and Mahendragarh: the line becomes the Haryana–Rajasthan border.', ['m6']),
)


# Regional timelines live in separate files, executed in this module's namespace.
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
for _part in ('tl_nw.py', 'tl_north.py', 'tl_north2.py', 'tl_west.py', 'tl_centre.py',
              'tl_south.py', 'tl_south2.py', 'tl_east.py', 'tl_sikkim.py', 'tl_ne.py', 'tl_ne2.py'):
    _path = _os.path.join(_HERE, _part)
    if _os.path.exists(_path):
        exec(compile(open(_path, encoding='utf-8').read(), _path, 'exec'))
