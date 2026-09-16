# Rivers — assignment and progress

Task (user, 2026-09-15): draw all significant rivers on the map. For rivers that also flow outside
India, draw only the Indian stretch plus a few km beyond the boundary to show where they enter or
leave. At the end, list every river drawn. The user asked for one subagent per independent river
system.

## Pipeline (`river_tool.py`; run `python river_tool.py` for full usage)

- **Data sources:**
  - Natural Earth 10m river centre-lines (`data/ne_10m_rivers_lake_centerlines.geojson`): main rivers only.
  - OpenStreetMap via Overpass (`osm KEY --wikidata Q…` or `--name REGEX --bbox S,W,N,E`), cached as `data/osm_KEY.json`.
- **Projection:** SVG x/y are an affine function of lon/lat (`projection_fit.json`), fitted to Natural
  Earth's India-view outline. Median error is about 0.55 SVG units (~2 km). Checked against the
  Godavari's river-borders, which it follows exactly.
- **Clipping:** rivers are clipped to India's claimed boundary (`data/ind.geojson`, admin-0 India
  view) buffered by 0.10° (~11 km), which gives the "few km outside" stretch automatically.
- **Output:** each system has `SYSTEM.spec.json` (what to draw) and `SYSTEM.json` (built geometry).
  `python river_tool.py preview SYSTEM [--bbox …]` renders a PNG for a visual check.
- **Page build:** `../build.py` reads every `SYSTEM.json` into the page. It fails if the same river
  name appears in two systems.
- **Styling** (in `template.html`): rank 1 is a thick blue, rank 2 medium, rank 3 thin pale blue.
  Rivers sit beneath all borders and never take the mouse.

## Systems and owners

| System file | Scope |
|---|---|
| `indus` | Indus basin in India, including claimed areas: Indus, Shyok, Nubra, Zanskar, Suru, Dras, Jhelum, Kishanganga, Chenab (Chandra, Bhaga), Tawi, Ravi, Beas, Sutlej, Spiti |
| `ganga_north` | Ganga main stem (Bhagirathi, Alaknanda, Hooghly) and its northern / Himalayan tributaries: Ramganga, Gomti, Sharda (Mahakali), Ghaghara, Rapti, Gandak, Burhi Gandak, Bagmati, Kosi, Mahananda |
| `ganga_south` | Yamuna (including Tons, Hindon) and the southern tributaries of the Ganga/Hooghly: Chambal, Banas, Kali Sindh, Parbati, Sindh, Betwa, Ken, Tons (Tamsa), Son, Rihand, North Koel, Damodar, Barakar, Ajay, Mayurakshi, Rupnarayan |
| `brahmaputra` | Brahmaputra (Siang), Lohit, Dibang, Subansiri, Kameng, Manas, Sankosh, Raidak, Torsa, Jaldhaka, Teesta, Dhansiri, Kopili; Barak–Meghna rivers (Barak, Surma, Kushiyara, Gumti, Khowai, Dhaleswari/Tlawng); NE rivers flowing to Myanmar (Imphal/Manipur, Tizu, Kaladan) |
| `godavari` | Godavari, Purna (Godavari), Manjira, Pranhita, Wardha, Wainganga, Penganga, Indravati, Sabari, Sileru |
| `krishna` | Krishna, Koyna, Bhima, Nira, Sina, Ghataprabha, Malaprabha, Tungabhadra, Tunga, Bhadra, Vedavathi, Musi, Munneru |
| `south` | Kaveri basin (Kaveri, Hemavati, Kabini, Shimsha, Arkavathi, Bhavani, Amaravati, Kollidam); Pennar, Chitravati, Palar, Ponnaiyar, Vaigai, Tamirabarani; west-flowing Periyar, Bharathapuzha, Chaliyar, Pamba, Netravati, Sharavathi, Kali (Karnataka), Mandovi, Zuari |
| `east_central` | Mahanadi (Seonath, Hasdeo, Mand, Ib, Tel, Jonk), Brahmani (Sankh, South Koel), Baitarani, Subarnarekha, Budhabalanga, Rushikulya, Vamsadhara, Nagavali |
| `west` | Narmada (Tawa), Tapi (Purna (Tapi), Girna), Sabarmati, Mahi, Banas (Gujarat), Luni, Ghaggar, Shetrunji, Bhadar, Vaitarna |

## Naming rule

Names must be unique across all systems. Qualify shared names in brackets, e.g. "Purna (Godavari)"
vs "Purna (Tapi)", "Banas (Rajasthan)" vs "Banas (Gujarat)", "Tons (Uttarakhand)" vs "Tons (Tamsa)",
"Kali (Karnataka)" vs "Sharda (Mahakali)".

## Status: DONE (2026-09-15)

**Both parts of the task are complete and built into `../../india-borders.html`.**

### Part 1 — dotted state/UT borders
State/UT borders are grey dots at rest and the original solid line (+2px) on hover. The CSS is
`.border-line.internal` in `template.html`; `joinSegments()` in the page script merges the
two-point segments so the dots run evenly. The legend swatch is updated. `hovertest.mjs` reads
the base width from the `--w` custom property. The hover test passes (105/105 border pieces).

### Part 2 — rivers: superseded the OSM/Overpass plan with a reference-file extraction

**The 9 per-system subagents' Overpass-based approach (specs, OSM caches) is superseded.** Partway
through, the user pointed at `../../India_rivers_and_lakes_map.svg` — an existing India rivers-and-
lakes map (Adobe Illustrator export) — as a source of river points. That map already contains every
river's actual line-work AND a name label for each, so instead of continuing 9 slow, flaky Overpass
fetches, the coordinator built a one-shot extraction pipeline (`ref_extract.py`) that pulls the
whole river network out of that file directly, and it's both faster and more complete than the
OSM route was going to be. All 9 subagents were told to stop; each confirmed no file conflicts.

**How `ref_extract.py` works** (run `python ref_extract.py` for the usage docstring):
1. **`fit`** — the reference file draws its own lat/lon graticule (parallels 8–36°N, meridians
   68–96°E) with printed degree labels. Every parallel × meridian *intersection* is an exact,
   known (lon, lat) at a precise point in the reference file's own coordinates — 71 of a possible
   72 were found. A quadratic (lon,lat)→(x,y) fit through those 71 points gets a median residual
   of ~2 units (down from ~20 with a plain affine — this map has mild conic curvature). Composed
   with `projection_fit.json` (this project's existing lon/lat→our-SVG fit), that gives
   reference-file → our-SVG directly, without ever comparing the two files' boundary shapes
   (which was tried first, via ICP, and failed: residual 30+ units, because the reference file's
   "India_Map" layer turned out to include far more/different detail than just India's own
   outline, corrupting shape-based matching).
   - **Gotcha fixed along the way:** a naive `d="..."` regex was matching inside `id="sikkim"`
     (which contains the substring `d="sikkim"`) instead of the real geometry attribute — anchor
     that regex on a preceding space/`>`.
   - **Gotcha fixed along the way:** the reference file's paths use real SVG arcs (`A`/`a`) with
     packed flag digits (e.g. `011` = three flags `0,1,1`, not the number 11) — needed a proper
     character-scanning path parser (`_Scanner`/`parse_path`), not a single number-regex tokenizer.
2. **`list`** — the reference file's `<g id="riv">` group holds 63 name labels (one `<path>` guide
   curve + one `<text>` per label): 61 rivers plus 2 non-river entries filtered out
   (`NOT_RIVERS`: seas, reservoirs/lakes, the title, the legend).
3. **`build`** — the actual line-work lives in `<g id="rivers">` (99 disjoint hand-drawn curve
   pieces, stroke `#0074E8`). Each piece is assigned to whichever label's guide curve runs
   closest to it; **near-ties are assigned to every nearby label, not just the closest one** —
   at a confluence the junction piece sits almost equidistant between a river and its tributary
   (sometimes distance 0), and strict single-ownership left several rivers (Ganga among them)
   with zero geometry, every contact point having been won by a tributary by a fraction of a
   unit. A shared confluence piece drawn under two names is visually identical to drawing it
   once, so the duplication is harmless. Assignments then grow along touching endpoints.
   Segments are clipped to India's outline (reusing `river_tool.py`'s Natural-Earth-based
   `india_clip()`, reprojected into our SVG — *not* polygonized from our own border line-work,
   which is stored as disjoint fragments and doesn't close into one clean ring). Kept as
   separate pieces per river (no `linemerge` — the source file itself draws a river as several
   disconnected curve fragments, and our own state-border convention already renders multi-piece
   paths fine, so there's nothing to gain by forcing one continuous line and it isn't always
   possible: pieces don't reliably share exact endpoints).
   - Output: `ref_rivers.json` (61 rivers, flat, no system/rank yet).
4. **`split_systems.py`** — a fixed name→(system, rank) table assigns each of the 61 rivers to one
   of the 9 `RIVERS.md` systems and a rank (1 = main stem, 2 = major tributary, 3 = minor), then
   writes `SYSTEM.json` in the exact format `build.py` already expects.
5. **`preview`** (both `river_tool.py` and `ref_extract.py` have one) renders a PNG for visual
   sanity-checking. The full-map preview matched real geography closely, including several
   stretches where a state border visibly follows the river it's named after (e.g. Krishna
   through Maharashtra/Karnataka/Telangana/AP).

**River line thickness (original, 2026-09-15):** changed to equal a resting state/UT border's width
exactly (`calc(var(--px) * 1.9)`), per the user's then-current instruction. **Superseded the same
day** — see "Round 2" below.

**Final count after the reference-file extraction: 61 rivers, all 9 systems built.**

## Round 2 (2026-09-15, same day): visibility fixes + smaller tributaries

The user asked for five more changes after seeing the 61-river build:
1. Rivers were visually overshadowing the state/UT borders — make them lighter and thinner.
2. Put rivers on their own toggleable layer.
3. Off by default; a bottom-right slider shows/hides them.
4. Add the smaller rivers too, using whatever river data was already on hand.
5. Some rivers were incorrectly extended a few km into the sea at their mouth (noticed in Gujarat
   and Karnataka), when the "extend a little past the border" behaviour should only apply where a
   river actually crosses a land border into a neighbouring country.

**Fix for #5 first, since it affects every river already drawn:** `river_tool.py`'s `india_clip()`
used to buffer *all* of India's boundary by `MARGIN_DEG` (~11 km), coastline included — so every
river mouth got pushed out to sea by that margin, not just rivers that actually cross a land
border. Fixed by buffering only the Natural Earth land-border lines that touch India
(`data/ne_10m_admin_0_boundary_lines_land.geojson`, filtered to `ADM0_A3_L`/`ADM0_A3_R` == `IND`)
and unioning that with India's own unbuffered coastline, instead of buffering the whole country
outline. Re-ran `ref_extract.py build` + `split_systems.py` afterwards to rebuild all 61 original
rivers with the corrected clip (confirmed by projecting every river endpoint into SVG space and
checking it against both the coastline and the land-border lines: zero sea overshoots remained,
land-border extensions like Indus into Pakistan/China or Ganga tributaries into Nepal were
unaffected).

**Fix for #1–#3:** `.map .rivers` is `display:none` by default; a `.map.show-rivers .rivers` rule
and a bottom-right slider (`#river-toggle`, styled like a switch) toggle it. River colour/width
were changed from the equal-to-border style back to something lighter and thinner than a border:
`.river` is `stroke:#7fa8d6` at `~1.05px` with `opacity:.65`, `.river.r2` `~.8px`/`.58` opacity,
`.river.r3` `~.62px`/`.5` opacity — rank now varies both width and opacity, not just colour shade.

**Fix for #4 — 60 more rivers from cached OSM data:** an earlier (superseded) research phase had
already run `python river_tool.py osm KEY --wikidata/--name ...` for ~90 candidate tributaries
before the whole approach was replaced by the reference-file extraction; those fetches are still
cached in `data/osm_*.json` and cost nothing to reuse. A new tool, `add_osm_rivers.py SYSTEM
ADD.json`, appends OSM-sourced rivers to an existing SYSTEM.json (built by the reference-file
pipeline) without touching what's already there — same projection/clip/simplify as
`river_tool.py`'s own `make`, just merging instead of overwriting. One subagent per system
(matching the user's original "one subagent per independent river system" instruction) checked
each candidate cache's real lon/lat bbox against the expected geography before adding it (several
of the ~90 caches turned out to be contaminated — e.g. `osm_gomti.json` and `osm_sharda.json` cover
absurdly large, wrong-looking extents and were never used; `osm_tons_uk.json`, meant to be the
Uttarakhand Tons, actually turned out to be the unrelated Son-tributary Tons near Rewa/MP and was
added under the corrected name "Tons (Son)" instead of being mislabelled). `osm_bhadra.json` was
skipped as a duplicate of the already-drawn "Bhadra (Tungabhadra)".

Bug found and fixed during this round: `add_osm_rivers.py`'s `linemerge(unary_union(lines))` crashed
whenever a cached river had exactly one OSM way (`unary_union` of one line returns a bare
`LineString`, which `linemerge` rejects) — same root cause as the `linemerge` issue noted in the
original pipeline above. Fixed by skipping `linemerge` when the union is already a single
`LineString`.

**Final count: 121 rivers across the 9 systems.** Full breakdown: `python river_tool.py summary`.
The Brahmaputra system went from 2 rivers to 10 (Dibang, Kameng, Subansiri, Kopili, Raidak,
Sankosh, Jaldhaka, Torsa added) — closing the biggest gap noted below. The Delhi-area gap is
also closed (Hindon added to `ganga_south.json`).

**If more rivers are wanted later:** every cached `data/osm_*.json` with usable geometry has now
been used or deliberately excluded (see per-system git history / agent reports for exact
reasoning). Caches that were empty and skipped: `ajay`, `arkavathi`, `budhabalanga`, `kadam`,
`munneru`, `north_koel`, `rapti`, `rupnarayan`, `rushikulya`, `vaitarna`. Anything further needs a
fresh `python river_tool.py osm KEY --wikidata Q... ` (or `--name`) call.
