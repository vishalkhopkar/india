# Border timelines

The dated history shown in each border's modal on `india-borders.html`, the sources
behind each border's one-paragraph summary, and the references both cite. **These files are the source.** They are read by the page as
they are: edit one, reload the page, done — nothing is generated from them and
`_build/build.py` does not need to run.

One file per region, listed in `index.js` and loaded by the `<script>` tags in
`india-borders.html`:

| File | Covers |
|---|---|
| `nw.js` | Punjab, Haryana, Himachal, Delhi, Chandigarh, J&K, Ladakh; Pakistan, Afghanistan and western China |
| `north.js` | Uttar Pradesh, Uttarakhand, Bihar; Nepal and central China |
| `north2.js` | Jharkhand, Chhattisgarh, Madhya Pradesh and Rajasthan with Uttar Pradesh |
| `west.js` | Gujarat, Maharashtra, DNH&DD, Goa, Karnataka, Rajasthan, Madhya Pradesh |
| `centre.js` | Madhya Pradesh and Chhattisgarh with their neighbours |
| `south.js` | Andhra Pradesh, Telangana, Karnataka, Tamil Nadu, Odisha, Puducherry (Yanam), Maharashtra |
| `south2.js` | Karnataka, Kerala, Tamil Nadu and Puducherry among themselves |
| `east.js` | Bihar, Jharkhand, West Bengal, Odisha; the Bangladesh frontier |
| `sikkim.js` | Sikkim, Nepal, Bhutan and the China (Sikkim sector) borders |
| `ne.js` | Assam's internal borders, Arunachal–Nagaland, Manipur–Nagaland, Manipur–Mizoram, Mizoram–Tripura |
| `ne2.js` | Myanmar, Bangladesh, Bhutan and China frontiers of the north-eastern states |

## Format

```js
TIMELINES.<region> = {
  "refs": {
    "<key>": ["<title>", "<description>", "<url>"]
  },
  "timelines": {
    "<Region A>|<Region B>": [
      ["<when>", "<what happened>", ["<ref key>", "<ref key>"]]
    ]
  },
  "summaries": {
    "<Region A>|<Region B>": ["<ref key>", "<ref key>"],
    "<Region C>|<Region D>": {"text": "<replacement summary>", "refs": ["<ref key>"]}
  }
};
```

- **Pair keys** are the two names exactly as the provenance matrix writes them,
  sorted alphabetically and joined with `|` — `"Delhi (NCT)|Haryana"`,
  `"Jammu and Kashmir (UT)|Pakistan"`, `"Afghanistan|Ladakh"`. A pair the map has
  no line for is ignored (the page logs a warning).
- **Entries** are `[when, what, [ref keys]]`, oldest first. `when` is free text
  (`"1815–16"`, `"11 Apr 1861"`, `"Before 1803"`). `what` may use `<strong>` and
  `<em>`; write `&amp;` for a literal ampersand. Pass `[]` for no citation.
- **Summaries** list the sources for the summary paragraph at the top of the
  border's modal (the text comes from the provenance matrix via `_build/build.py`).
  The listed references are added to the citations already at the end of that
  paragraph. The object form also replaces the paragraph's text, for a summary whose
  matrix wording no source supports. Keep each pair in the same file as its timeline.
- **Reference keys** `m2`–`m35` point at the provenance matrix's own reference
  list and need no entry under `refs`. `m1` is not valid: it was the private
  research note the matrix was compiled from, which is not published. Every other
  cited key must be defined in some region file — any file, not necessarily this one.

## Reference numbering

The matrix's own references are shown as [1]–[34] (key `mN` appears as [N − 1],
because the matrix's [1] is dropped). `app.js` numbers every other cited
reference from 35 upwards, in the order the files define them, following the
region order in `index.js`. So inserting a new
reference shifts the numbers of the ones defined after it; the `[n]` links and
the list at the bottom of the page stay consistent because both are rendered from
these files at load time. References that nothing cites are not listed.

## Checking your edit

Reload `india-borders.html` and open the browser console. The page warns about a
region that failed to load, a reference or pair defined twice, a cited reference
that is not defined, and a timeline or summary that matches no border on the map. A syntax
error in one file (a missing comma or bracket) stops that file alone from
loading, so its borders lose their timelines — the console names the file.

Adding a whole new region file also means adding a `<script>` tag for it in
`_build/template.html` and rebuilding the page; changing timeline data does not.
