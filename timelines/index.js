// Timeline data for india-borders.html, one file per region, all loaded by
// <script> tags in the page (see india-borders.html) in the order listed here.
//
// Each timelines/<region>.js adds itself to this object:
//
//   TIMELINES.<region> = {
//     "refs":      { "<key>": ["<title>", "<description>", "<url>"] },
//     "timelines": { "<Region A>|<Region B>": [["<when>", "<what>", ["<ref key>"]]] }
//   };
//
// app.js merges them, numbers the references and renders the citations, so a
// timeline is changed by editing a file here and reloading the page. Nothing is
// generated: these files are the source. See timelines/README.md.
//
// Region order matters: references are numbered from 36 (after the matrix's own
// [1]-[35]) in the order they are first defined across these files.
const TIMELINES = {};
const TIMELINE_REGIONS = ["nw", "north", "north2", "west", "centre", "south", "south2", "east", "sikkim", "ne", "ne2"];
