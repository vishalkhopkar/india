# Border timelines — progress notes

Last updated: 2026-09-15. Status: **COMPLETE: all 95 border pairs have timelines**, with 283 new
references numbered after the matrix's own [1]–[35]. The HTML is rebuilt. The hover test passes at
1920×1080 and 1400×1100: all 105 border pieces are reachable, grow 2px, show the pointer cursor,
and open a hover box that fits on screen, with no script errors.

**Source caveats the agents flagged, worth a human look:**
- **Weaker sources:** the Dangs’ 1948 merger into Bombay is sourced to indiastatestory.in, a
  secondary site. Devikulam/Peermade material comes from a Tamil Nadu-side article and is phrased
  as a claim.
- **Unverified matrix claim:** Odisha’s reliance on 1938 Balasore revenue maps (matrix text) could
  not be verified, so the Odisha–WB timeline doesn’t repeat it.
- **Date conflicts, noted in the text or the reference:**
  - Treaty of Sinchula: 1865 per Wikipedia, 1864 per darjeeling.gov.in.
  - Khathing’s Tawang expedition: 1951 vs 1950.
  - Maharashtra’s Supreme Court suit on Belgaum: 2004 vs 2006.
  - Cooch Behar merger: 19 Jan 1950, per coochbehar.gov.in.
- **Dropped as unsourced:** the Balasore–Midnapore transfer dates of 1837–86; the 1925 Naga Hills
  notification number; the 1938/44 British missions to Tawang; the 1872–73 Bhutan boundary survey.

**Task started 2026-09-15, both parts now DONE** (user request):
1. Make state/UT borders dotted grey at rest and unchanged (solid, 2px thicker) on hover. **Done.**
2. Draw all the rivers: only their Indian stretch, plus a few km beyond the boundary, one subagent
   per river system, then list every river drawn. **Done — 61 rivers across all 9 systems.**
   Midway, the user pointed at `India_rivers_and_lakes_map.svg` (a reference rivers map already in
   the project folder) as a source of river points; that turned out to hold every river's actual
   line-work AND a name label, so the 9 Overpass-based subagents were stopped (cleanly, no file
   conflicts) in favour of one extraction pipeline (`rivers/ref_extract.py`) pulling the whole
   network out of that file directly — faster and more complete than continuing OSM fetches.
   River line thickness was also changed to equal a resting state/UT border's width exactly, per
   the user's instruction. Full write-up, the extraction method, and where to add more rivers
   later: `rivers/RIVERS.md`.

Everything below is the history of how the work was done.

## The task

The user asked for extensive research on **every internal and external border** on the map, and
for each hover box to show a **timeline with numbered references**, in the style of the first
one done (Haryana–Rajasthan).

- Start each timeline at the earliest traceable origin of the line: the treaty, princely-state
  edge or colonial district boundary it follows.
- If no earlier origin can be found, start from the reorganisation that created the border. The
  user's example was Maharashtra–Gujarat, which could begin at the Bombay Reorganisation Act,
  1960. But note that Act split Umbergaon taluka village by village and gave the Dangs to
  Gujarat, so try the older Dharampur / Bansda / Surgana / Dangs history first.
- End each timeline with the event that made it today's border (for example 1 Nov 1966 for
  Haryana–Rajasthan).
- Stay factual and neutral, especially on disputed borders.

## How the build works (all in this `_build` folder)

| File | Role |
|---|---|
| `build.py` | `python build.py` rebuilds `../india-borders.html`. It reads `../india-borders.svg`, `../india-border-provenance-matrix-sourced.html`, `template.html` and `timelines.py`. |
| `template.html` | Page CSS and JavaScript (labels, hit areas, hover box, timeline rendering, two-column layout on short windows). Since 2026-09-14 it also holds the header ("Every Indian border mapped"), the footer ("An ongoing project of Vishal Khopkar") and the Indian theme: palette in `:root`, Rozha One and Mukta fonts from Google Fonts, jaali background, toran divider, rangoli rosette symbol `#rangoli`. The map SVG is selected with `.map > svg:not(.corner)`, because the corner rosettes are also SVGs inside `.map`. |
| `timelines.py` | Defines `ref(key, title, desc, url)` and `timeline('A|B', (when, text, [keys]), ...)`. It runs the regional files `tl_nw.py`, `tl_north.py`, `tl_west.py`, `tl_south.py`, `tl_east.py` and `tl_ne.py` in that order, skipping any that don't exist. |
| `tl_nw.py`, `tl_north.py` | Timelines done so far. |
| `hovertest.mjs` | `node hovertest.mjs 1400 900` drives headless Chrome with real mouse events. It checks every border is reachable, grows 2px, shows the pointer cursor and opens its hover box; the tooltip dims print as `TIPDIMS`. |
| `_todo.txt` | Pairs still without a timeline (regenerate with the snippet at the end of this file). |

Conventions:
- **Pair keys** are the two matrix names sorted alphabetically and joined with `|`, e.g.
  `'Delhi (NCT)|Haryana'`, `'Jammu and Kashmir (UT)|Pakistan'`, `'Afghanistan|Ladakh'`,
  `'Chhattisgarh|Uttar Pradesh'`.
- **Reference keys** `m1`–`m35` point at the matrix's own reference list, for example:
  - `m2` States Reorganisation Act 1956; `m3` Bihar–WB Transfer of Territories Act 1956
  - `m4` Bombay Reorganisation Act 1960; `m5` State of Nagaland Act 1962
  - `m6` Punjab Reorganisation Act 1966; `m7` North-Eastern Areas (Reorganisation) Act 1971
  - `m8` UP Reorganisation Act 2000; `m9` Bihar Reorganisation Act 2000
  - `m10` AP Reorganisation Act 2014; `m11` AP Reorganisation (Amendment) Bill 2014
  - `m12` J&K Reorganisation Act 2019; `m13` Radcliffe Bengal award; `m15`/`m16` Assam border pages
  - `m20` Puducherry history; `m24` Orissa Order 1936; `m26` Simla Agreement; `m27` Karachi Agreement
  - `m28` 100th Amendment 2015; `m29` DoPT on the 2000 reorganisation; `m30` Assam–Arunachal 2023
  - `m32` Goa, Daman and Diu Reorganisation Act 1987; `m33` DNH&DD merger 2019
  - `m34` Manipur Merger Agreement 1949; `m35` Sikkim–Tibet Convention 1890
- **New references** are numbered from 36 in the order `ref()` is called, counting only those
  actually cited. Keys must be unique across all regional files; `build.py` fails on an unknown or
  duplicate key.
- **Apostrophes and HTML:** use `’` for apostrophes and `&amp;` for a literal ampersand in text.
- **Timeline size:** keep each timeline to about 4–11 entries so the hover box fits the window.

## Research rules the user expects

- Cite only sources actually read: a fetched page, or a search-result summary with its URL.
- Don't include claims that no source backs up. One example already excluded: "southern Bhattiana
  went to Bikaner in 1818" appeared in a search summary but in no page read.
- If sources disagree, say so in the entry, as with "Loharu 1803 (some sources say 1806)".

## Practical lessons

- **Shell limits:** very long Bash heredocs fail with `ENAMETOOLONG`, so write new region files
  with the Write tool, not heredocs.
- **Escaping:** Python edits made through a Bash heredoc have mangled `\n` and `\\` more than
  once. Use the Edit tool for small changes.
- **Unreachable sites:** `delhiassembly.delhi.gov.in`, `delhiplanning.delhi.gov.in` and
  `dmshahdara.delhi.gov.in` refused connections from WebFetch.
- **PDFs:** when WebFetch can't parse a PDF, it saves the binary to a tool-results file; the Read
  tool can then open it. This is expensive, since it renders page images, so use it only for key
  sources such as the US State Dept International Boundary Studies (`ibs86` was read this way).
- **Good sources:**
  - US State Dept International Boundary Studies (at `library.law.fsu.edu/Digital-Collections/LimitsinSeas/pdf/ibsNNN.pdf`)
  - Wikisource copies of the Radcliffe awards and the 1950 White Paper on Indian States
  - District "history" pages on `*.nic.in` and `*.gov.in`
  - India Code / Indian Kanoon for the Alteration of Boundaries Acts

## Done (29)

- **Region file `timelines.py`:** Haryana|Rajasthan.
- **Region file `tl_nw.py`:**
  - Punjab: Punjab|Rajasthan, Haryana|Punjab, Pakistan|Punjab
  - Chandigarh: Chandigarh|Haryana, Chandigarh|Punjab
  - Delhi and Haryana: Delhi (NCT)|Haryana, Delhi (NCT)|Uttar Pradesh, Haryana|Uttar Pradesh, Haryana|Himachal Pradesh
  - Himachal: Himachal Pradesh|Punjab, Himachal Pradesh|Jammu and Kashmir (UT), Himachal Pradesh|Ladakh, China|Himachal Pradesh
  - J&K and Ladakh: Jammu and Kashmir (UT)|Punjab, Jammu and Kashmir (UT)|Ladakh, Jammu and Kashmir (UT)|Pakistan, Ladakh|Pakistan, China|Ladakh, Afghanistan|Ladakh
  - West: Pakistan|Rajasthan, Gujarat|Pakistan
- **Region file `tl_north.py`:** Nepal|Uttarakhand, Nepal|Uttar Pradesh, Bihar|Nepal, Uttar Pradesh|Uttarakhand, Himachal Pradesh|Uttarakhand, China|Uttarakhand, Bihar|Uttar Pradesh.

## 2026-09-14: parallel research run (subagents)

The 66 remaining pairs were split across 9 research subagents. Each one writes only its own file,
uses its own reference-key prefix, and validates with `python check_region.py <file>`. The
loader in `timelines.py` already lists all these files and skips any that don't exist.

| File | Prefix | Pairs |
|---|---|---|
| `tl_north2.py` | `n2_` | Jharkhand/Chhattisgarh/Madhya Pradesh/Rajasthan with Uttar Pradesh |
| `tl_west.py` | `w_` | Gujarat–Maharashtra, DNH&DD with Gujarat and with Maharashtra, Goa with Maharashtra and with Karnataka, Gujarat with Rajasthan and with MP |
| `tl_centre.py` | `c_` | MP with Rajasthan and with Maharashtra; Chhattisgarh with MP, Maharashtra, Odisha, Telangana, Jharkhand and AP |
| `tl_south.py` | `s_` | AP with Telangana, Karnataka, TN, Odisha and Puducherry; Telangana with Maharashtra and with Karnataka |
| `tl_south2.py` | `s2_` | Karnataka with Kerala, Maharashtra and TN; Kerala with TN and with Puducherry; Puducherry–TN |
| `tl_east.py` | `e_` | Bihar with Jharkhand and with WB; Jharkhand with WB and with Odisha; Odisha–WB; Bangladesh–WB |
| `tl_sikkim.py` | `h_` | Sikkim–WB, Nepal with WB and with Sikkim, Bhutan with WB and with Sikkim, China–Sikkim |
| `tl_ne.py` | `ne_` | The Assam internal pairs (with Arunachal, Nagaland, Meghalaya, Mizoram, Manipur, Tripura, WB), Arunachal–Nagaland, Manipur with Nagaland and with Mizoram, Mizoram–Tripura |
| `tl_ne2.py` | `nx_` | The Myanmar ×4, Bangladesh ×4 (Assam, Meghalaya, Tripura, Mizoram), Bhutan ×2 (Arunachal, Assam) and Arunachal–China pairs |

If a run is interrupted:
1. Check which files exist and pass `check_region.py`.
2. Rerun research only for the missing pairs.
3. Run `python build.py` and `node hovertest.mjs 1920 1080`.

**Outcome of the first run:** all 9 agents hit the account's session usage limit and stopped
before writing anything, so no region file was created and nothing was lost from the HTML.
Lesson: agents must **save after every pair**, writing the file and running `check_region.py`
each time, so partial research survives an interruption. Rerun on 2026-09-14 with that rule.

**Outcome of the retry (Sonnet agents, save-per-pair):** the usage limit hit again, but 24 pairs
were saved and all validate. They are built into the HTML (2026-09-15).
- **Total: 53 of 95 pairs done.**
- Fixed one agent error in `tl_north2.py`: the SRA 1956 entry wrongly said the Act "formed Uttar
  Pradesh".
- Saved per file:
  - `tl_north2.py`: all 4 done.
  - `tl_centre.py`: MP–Rajasthan, MP–Maharashtra, Chhattisgarh with MP and with Maharashtra.
  - `tl_west.py`: Gujarat–Maharashtra.
  - `tl_south.py`: AP with Telangana and with Karnataka.
  - `tl_south2.py`: Karnataka with Kerala and with Maharashtra.
  - `tl_east.py`: Bihar–Jharkhand, Bihar–WB, Jharkhand–WB.
  - `tl_sikkim.py`: Nepal–Sikkim, Nepal–WB, Sikkim–WB.
  - `tl_ne.py`: Arunachal–Assam.
  - `tl_ne2.py`: the four Myanmar pairs.
- Some files define references for pairs not yet written. That's harmless, because only cited
  references are listed.
- **Remaining 42 pairs:** see `_todo.txt`. Each belongs to the file of the same region per the
  table above.
- **To resume:** give each region's agent its own file name and tell it to keep the existing
  pairs and add the missing ones.

**2026-09-15, after resuming the agents:** **85 of 95 pairs are done** and built into the HTML;
all files validate and the hover test passes.
- Complete: `tl_north2`, `tl_centre`, `tl_south`, `tl_south2`, `tl_sikkim`.
- **Remaining 10 pairs** (the usage limit hit again):
  - `tl_west.py`: Gujarat|Madhya Pradesh
  - `tl_east.py`: Bangladesh|West Bengal
  - `tl_ne.py`: Arunachal Pradesh|Nagaland, Assam|West Bengal, Manipur|Mizoram, Manipur|Nagaland, Mizoram|Tripura
  - `tl_ne2.py`: Arunachal Pradesh|Bhutan, Assam|Bhutan, Arunachal Pradesh|China

## To do (66), suggested order and research leads

### North, remainder (append to `tl_north.py`)
- **Jharkhand|Uttar Pradesh:** not researched yet.
  - Leads: Palamau district (Chota Nagpur) vs Mirzapur and, later, Sonbhadra (1989); Chota Nagpur Division; Bihar & Orissa 1912; Bihar 1936; Bihar Reorganisation Act 2000 (`m9`).
- **Chhattisgarh|Uttar Pradesh** (currently shows a short EXTRA text in `build.py`):
  - Leads: Surguja princely state vs Mirzapur; Eastern States Agency; Surguja merged into the Central Provinces in 1948; MP 1956; Chhattisgarh 2000.
- **Madhya Pradesh|Uttar Pradesh:**
  - Leads: Bundelkhand states; Central India Agency; Vindhya Pradesh (1948) and Madhya Bharat (1948); MP 1956; the jagged Lalitpur line; the Chambal and Yamuna.
- **Rajasthan|Uttar Pradesh:**
  - Leads: Bharatpur, Dholpur and Karauli vs Agra and Mathura (ceded 1803 in the Surji-Anjangaon / Lake campaign); Matsya Union 1948; Rajasthan 1949.

### West and centre (new file `tl_west.py`)
- **Gujarat|Maharashtra:**
  - Leads: Bombay Presidency districts of Surat, Thana and West Khandesh; Baroda state; the Dangs; the Dharampur, Bansda and Surgana states.
  - Also: Bombay State 1956, the Samyukta Maharashtra movement, and the Bombay Reorganisation Act 1960 (`m4`) village schedules.
- **Dadra and Nagar Haveli and Daman and Diu|Gujarat** and **…|Maharashtra:**
  - Leads: Portuguese Diu 1535 and Daman 1559; the Dadra and Nagar Haveli grants of 1779–85 (Treaty of Friendship with the Marathas); liberation 1954; annexation 1961.
  - Also: the Goa, Daman and Diu Reorganisation Act 1987 (`m32`) and the 2019/2020 merger (`m33`).
- **Goa|Maharashtra** and **Goa|Karnataka:**
  - Leads: the Portuguese Velhas Conquistas and Novas Conquistas (1763–88); Sawantwadi; North Kanara (Bombay Presidency) going to Mysore in 1956; Operation Vijay, 19 Dec 1961; the 1967 opinion poll; statehood 30 May 1987 (`m32`).
- **Gujarat|Rajasthan:**
  - Leads: Palanpur, Idar, Danta and Sirohi; the Western India States Agency vs the Rajputana Agency; Sirohi split in 1950; Abu Road to Rajasthan 1956 (`m2`).
- **Gujarat|Madhya Pradesh:**
  - Leads: Rewa Kantha vs Jhabua and Alirajpur (Central India Agency); Madhya Bharat 1948; Bombay 1956; Gujarat 1960.
- **Madhya Pradesh|Rajasthan:**
  - Leads: the Central India and Rajputana Agencies; Gwalior, Tonk (enclaves such as Sironj) and Jhalawar; 1956 exchanges of Sironj to MP and Sunel Tappa to Rajasthan (`m2`).
- **Madhya Pradesh|Maharashtra:**
  - Leads: the Central Provinces (1861) and Berar (1903 merger); Nagpur division and Berar to Bombay State in 1956; Maharashtra 1960.
- **Chhattisgarh borders:**
  - Chhattisgarh|Madhya Pradesh, Chhattisgarh|Maharashtra, Chhattisgarh|Odisha, Chhattisgarh|Telangana, Chhattisgarh|Jharkhand, Andhra Pradesh|Chhattisgarh
  - Leads: Chhattisgarh division of the CP (1862); the Chhattisgarh Feudatory States and Eastern States Agency, merged into the CP on 1 Jan 1948; Bastar; Madhya Pradesh Reorganisation Act 2000; the 2014 transfer of the Polavaram mandals (`m10`/`m11`).

### South (new file `tl_south.py`)
- **Andhra Pradesh pairs:** AP|Telangana, AP|Karnataka, AP|Tamil Nadu, AP|Odisha, AP|Puducherry.
  - Leads: Madras Presidency and Hyderabad; Andhra State 1 Oct 1953; the Bellary partition; AP 1 Nov 1956; Tiruttani to Madras under the 1959 alteration of boundaries Act; Telangana 2 Jun 2014 (`m10`).
  - Also: Kotia (AP–Odisha); the Orissa province of 1936 (`m24`).
- **Karnataka pairs:** Karnataka|Kerala, Karnataka|Maharashtra, Karnataka|Tamil Nadu, Karnataka|Telangana.
  - Leads: Mysore state; SRA 1956; Kasaragod; the Belgaum dispute and Mahajan Commission 1967; Kollegal.
- **Kerala|Tamil Nadu:** Travancore–Cochin 1949; Kanyakumari and Shencottah moved to Madras in 1956.
- **Puducherry pairs:** Kerala|Puducherry, Puducherry|Tamil Nadu.
  - Leads: French India; de facto transfer 1 Nov 1954; de jure 1962 (`m20`).
- **Maharashtra|Telangana:** Hyderabad State; Marathwada to Bombay State in 1956.

### East (new file `tl_east.py`)
- **Bengal and Bihar pairs:** Bihar|Jharkhand, Bihar|West Bengal, Jharkhand|West Bengal, Odisha|West Bengal, Jharkhand|Odisha.
  - Leads: Bengal Presidency; 1905 partition; 1912; 1936; Seraikela and Kharsawan to Bihar in 1948; Mayurbhanj; the Bihar–WB 1956 Act (`m3`); Jharkhand 15 Nov 2000 (`m9`).
- **Sikkim|West Bengal:** Treaty of Titalia 1817; Darjeeling grant 1835; annexation 1850; Sikkim state 1975.
- **Nepal|West Bengal** and **Nepal|Sikkim:** Sugauli 1816; Titalia 1817.
- **Bhutan|West Bengal** and **Bhutan|Sikkim:** Duar War; Treaty of Sinchula, 11 Nov 1865; Treaty of Punakha 1910; 1949 treaty.
- **China|Sikkim:** the 1890 Convention (`m35`); Doklam 2017.
- **Bangladesh|West Bengal:** Radcliffe award (`m13`); Nehru–Noon 1958; Berubari; 1974 Land Boundary Agreement; enclave exchange 31 Jul 2015 (`m28`).

### North-east (new file `tl_ne.py`)
- **Assam's internal borders:** Arunachal Pradesh|Assam, Assam|Nagaland, Assam|Meghalaya, Assam|Mizoram, Assam|Manipur, Assam|Tripura, Assam|West Bengal.
  - Leads: Treaty of Yandabo 1826; Assam province 1874; the 1873 Inner Line; NEFA; Nagaland 1963 (`m5`); NEARA 1971 (`m7`); Mizoram 1987; the dispute pages (`m15`, `m18`, `m25`, `m30`); the Manipur merger (`m34`); Tripura's merger in 1949; Goalpara vs Cooch Behar.
- **Hill-state borders:** Arunachal Pradesh|Nagaland, Manipur|Nagaland, Manipur|Mizoram, Mizoram|Tripura.
- **Myanmar borders:** Arunachal Pradesh|Myanmar, Myanmar|Nagaland, Manipur|Myanmar, Mizoram|Myanmar.
  - Leads: Yandabo 1826; the Pemberton line 1834 and Kabaw Valley; Burma's separation in 1937; the India–Burma boundary agreement of 10 Mar 1967. Try International Boundary Study No. 80 (Burma–India).
- **Bangladesh borders:** Assam|Bangladesh, Bangladesh|Meghalaya, Bangladesh|Tripura, Bangladesh|Mizoram.
  - Leads: Radcliffe award; the Sylhet referendum of July 1947; the 1974 Land Boundary Agreement and the 2015 amendment.
- **Bhutan borders:** Arunachal Pradesh|Bhutan, Assam|Bhutan (Duars, Sinchula 1865).
- **China|Arunachal:** Arunachal Pradesh|China, covering the Simla Convention of 1914, the McMahon Line and the 1962 war.

## Snippet: regenerate `_todo.txt`

```python
import re, sys; sys.path.insert(0, '.')
src = open('build.py', encoding='utf-8').read()
grab = lambda n: re.findall(r"'([^']+\|[^']+)'", re.search(n + r' = \[(.*?)\n\]', src, flags=re.S).group(1))
pairs = {'|'.join(sorted(p.split('|'))) for p in grab('INTERNAL') + grab('EXTERNAL')}
from timelines import TIMELINES
open('_todo.txt', 'w', encoding='utf-8').write('\n'.join(sorted(pairs - set(TIMELINES))))
```
