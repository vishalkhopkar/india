// ------------------------------------------------------------------ timelines
// The timelines and the references they cite are hand-edited data files in
// timelines/, read by the page as they are. Merging them, numbering the
// references and rendering the citation links used to happen in the build; doing
// it here is what lets a timeline be changed by editing a file and reloading.
(function () {
  const refs = new Map();       // ref key -> [title, description, url], in definition order
  const timelines = new Map();  // "Region A|Region B" (names sorted) -> [[when, what, [ref keys]]]

  for (const region of TIMELINE_REGIONS) {
    const data = TIMELINES[region];
    if (!data) { console.warn(`timelines: region "${region}" did not load`); continue; }
    for (const [key, ref] of Object.entries(data.refs || {})) {
      if (refs.has(key)) console.warn(`timelines: reference "${key}" is defined twice`);
      else refs.set(key, ref);
    }
    for (const [pair, items] of Object.entries(data.timelines || {})) {
      const key = pair.split('|').map(s => s.trim()).sort().join('|');
      if (timelines.has(key)) console.warn(`timelines: "${key}" has two timelines`);
      else timelines.set(key, items);
    }
  }

  // Reference numbers: "m1".."m35" are the matrix's own list; every other cited
  // reference is numbered after it, from 36, in the order the files define them.
  const cited = new Set();
  for (const items of timelines.values())
    for (const [, , keys] of items) for (const key of keys) cited.add(key);
  const number = new Map();
  for (const key of cited) if (/^m[0-9]+$/.test(key)) number.set(key, +key.slice(1));
  let next = 36;
  for (const key of refs.keys()) if (cited.has(key)) number.set(key, next++);
  for (const key of cited) if (!number.has(key)) console.warn(`timelines: cited reference "${key}" is not defined`);

  const cite = keys => '<sup class="ref">' +
    [...new Set(keys.map(key => number.get(key)))].filter(n => n !== undefined).sort((a, b) => a - b)
      .map(n => `<a href="#ref-${n}">[${n}]</a>`).join('') + '</sup>';

  // Hand each border its timeline. A border can be drawn as several paths (a long
  // line cut into parts); each part carries the same pair of names, so each gets it.
  const used = new Set();
  for (const border of Object.values(DATA.borders).flat(2)) {
    const key = [border.a, border.b].sort().join('|');
    const items = timelines.get(key);
    if (!items) continue;
    used.add(key);
    border.timeline = items.map(([when, what, keys]) => [when, keys.length ? `${what} ${cite(keys)}` : what]);
  }
  for (const key of timelines.keys()) if (!used.has(key)) console.warn(`timelines: "${key}" matches no border on the map`);

  // The references list: the matrix's own <ol>, plus every reference cited above.
  const extra = [...refs].filter(([key]) => number.has(key)).map(([key, [title, desc, url]]) =>
    `<li id="ref-${number.get(key)}"><strong>${title}</strong> — ${desc} ` +
    `<a href="${url}" rel="noopener noreferrer" target="_blank">Source</a></li>`).join('');
  document.getElementById('refs-list').innerHTML = REFS_HTML.replace('</ol>', () => extra + '</ol>');
})();

(function () {
  const NS = 'http://www.w3.org/2000/svg';

  // The drawn map is india-borders.svg, kept out of the page and handed over as
  // markup in map.js. Put it in the frame's placeholder, keeping its position
  // between the corner rosettes and the legend, and everything below works on
  // the SVG exactly as if the page had carried it all along.
  document.getElementById('map-svg').outerHTML = MAP_SVG;

  const svg = document.querySelector('.map > svg:not(.corner)');
  const tip = document.querySelector('.tip');

  function el(name, attrs) {
    const node = document.createElementNS(NS, name);
    for (const k in attrs) node.setAttribute(k, attrs[k]);
    return node;
  }

  // Layers in india-borders.svg, identified by their stroke styling:
  //   #9a9a9a                  state / UT borders
  //   #1f6fd0                  coastlines (not hoverable)
  //   #000000                  international borders
  //   #000000 + dasharray      Line of Control / Line of Actual Control
  function kindOf(layer) {
    const stroke = layer.getAttribute('stroke');
    if (stroke === '#9a9a9a') return 'internal';
    if (stroke === '#000000') return layer.hasAttribute('stroke-dasharray') ? 'loc-lac' : 'external';
    return 'coastline';
  }

  // 1. Tag every border line with its drawn width and history entry.
  //    Paths within a layer are matched to DATA.borders in document order.
  const lines = [];
  const info = new Map();

  function addBorder(path, entry, baseWidth) {
    path.classList.add('border-line');
    path.style.setProperty('--w', baseWidth + 'px');
    info.set(path, entry);
    lines.push(path);
  }

  // A few paths hold more than one border. Their entry is a list of parts, each
  // [sub-path, first vertex, last vertex or null]; cut the path into those parts.
  function partOf(d, [sub, from, to]) {
    const pts = d.split(/(?=M)/)[sub].match(/-?[\d.]+ -?[\d.]+/g);
    return 'M' + pts.slice(from, to === null ? undefined : to + 1).join('L');
  }

  // State / UT border paths are stored as many two-point segments ("M a L b M b L c …").
  // Join segments that continue from the previous one, so a dotted pattern runs evenly
  // instead of restarting at every vertex.
  function joinSegments(d) {
    const runs = [];
    for (const sub of d.split(/(?=M)/)) {
      const pts = sub.match(/-?[\d.]+ -?[\d.]+/g);
      if (!pts) continue;
      const run = runs[runs.length - 1];
      if (run && run[run.length - 1] === pts[0]) run.push(...pts.slice(1));
      else runs.push(pts);
    }
    return runs.map(run => 'M' + run.join('L')).join('');
  }

  for (const layer of svg.querySelectorAll(':scope > g')) {
    const kind = kindOf(layer);
    if (kind === 'coastline') {
      layer.classList.add('coastline');
      continue;
    }
    const baseWidth = parseFloat(layer.getAttribute('stroke-width'));

    [...layer.querySelectorAll('path')].forEach((path, i) => {
      const entry = DATA.borders[kind][i];
      if (kind === 'internal') {
        path.setAttribute('d', joinSegments(path.getAttribute('d')));
        path.classList.add('internal');
      }
      if (!Array.isArray(entry)) return addBorder(path, entry, baseWidth);
      for (const part of entry) {
        const piece = el('path', { d: partOf(path.getAttribute('d'), part.part) });
        layer.insertBefore(piece, path);
        addBorder(piece, part, baseWidth);
      }
      path.remove();
    });
  }

  // Rivers go just above the white background, beneath every border line.
  const riverLayer = el('g', { class: 'rivers' });
  for (const r of DATA.rivers) {
    const path = el('path', { class: `river r${r.r}`, d: r.d });
    path.dataset.name = r.n;
    riverLayer.append(path);
  }
  svg.querySelector(':scope > rect').after(riverLayer);

  const riverToggle = document.getElementById('river-toggle');
  riverToggle.addEventListener('change', () => {
    document.querySelector('.map').classList.toggle('show-rivers', riverToggle.checked);
  });

  // 2. Names of states, union territories and neighbouring countries.
  const labelLayer = el('g', { class: 'labels' });
  const leaders = [];
  for (const lab of DATA.labels) {
    // Labels with a leader line sit beside the place they name, anchored at the
    // side nearest to it: "end" = text left of the place, "mid" = centred,
    // otherwise text to the right.
    const classes = lab.cls.split(' ');
    if (classes.includes('lead') && !classes.includes('end') && !classes.includes('mid')) classes.push('start');
    const text = el('text', { class: classes.filter(c => c !== 'lead' && c !== 'mid').join(' '), x: lab.x, y: lab.y });
    const rows = lab.text.split('\n');
    rows.forEach((row, i) => {
      const tspan = el('tspan', { x: lab.x, dy: i === 0 ? (-(rows.length - 1) * 0.55) + 'em' : '1.1em' });
      tspan.textContent = row;
      text.append(tspan);
    });
    for (const [lx, ly] of lab.leads) {
      const line = el('line', { class: 'leader', x1: lx, y1: ly, x2: lx, y2: ly });
      labelLayer.append(line, el('circle', { class: 'leader-dot', cx: lx, cy: ly, r: 1.3 }));
      leaders.push({ line, text, lx, ly });
    }
    labelLayer.append(text);
  }
  svg.append(labelLayer);

  // 3. Invisible hit areas, drawn on top of everything in two layers:
  //    - "near": a few px of slack around each line, so thin lines are easy to hit;
  //    - "on":   the line itself, above every "near" area, so the line actually
  //              under the cursor always beats a neighbour's slack.
  //    Within a layer, shorter borders sit on top so tiny ones stay reachable.
  const near = el('g', { fill: 'none', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' });
  const on = near.cloneNode();
  lines
    .map((line, i) => ({ line, i, length: line.getTotalLength() }))
    .sort((a, b) => b.length - a.length)
    .forEach(({ line, i }) => {
      for (const [layer, cls] of [[near, 'hit hit-near'], [on, 'hit hit-on']]) {
        const hit = el('path', { d: line.getAttribute('d'), class: cls });
        hit.dataset.border = i;
        hit.style.setProperty('--w', line.style.getPropertyValue('--w'));
        layer.append(hit);
      }
    });
  svg.append(near, on);

  // 4. Hover box.
  const NAMES = { 'Delhi (NCT)': 'Delhi', 'Jammu and Kashmir (UT)': 'Jammu and Kashmir' };
  const SOLID = (color, width) => `<line x1="1" y1="4" x2="17" y2="4" stroke="${color}" stroke-width="${width}" stroke-linecap="round"/>`;
  const DOTTED = '<line x1="2" y1="4" x2="17" y2="4" stroke="#000" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="0.1 4.5"/>';
  const KIND = {
    internal: ['State / UT border', SOLID('#9a9a9a', 1.6)],
    external: ['International border', SOLID('#000', 2.4)],
    loc: ['Line of Control', DOTTED],
    lac: ['Line of Actual Control', DOTTED],
    defacto: ['De facto line', DOTTED],
  };
  const name = n => NAMES[n] || n;

  // Hover box: deliberately minimal — just what kind of border this is, the two
  // territories it separates, and a nudge to click for the full history.
  function renderTip(b) {
    const [kindLabel, swatch] = KIND[b.kind];
    const simple = b.kind === 'internal' ? 'Internal border' : 'External border';
    tip.innerHTML =
      `<div class="tip-kind"><svg width="18" height="8" aria-hidden="true">${swatch}</svg>${simple}</div>` +
      `<div class="tip-title">${b.title || name(b.a) + ' – ' + name(b.b)}</div>` +
      `<div class="tip-hint">Click to know more</div>`;
  }

  // Full-history modal: everything the old hover box used to show, laid out as a
  // reading page instead of a cursor-following box, with the timeline as a proper
  // two-column (date, description) list.
  const modalBackdrop = document.getElementById('modal-backdrop');
  const modalBody = document.querySelector('.modal-body');
  let lastFocused = null;

  // The history block, shared by the modal and the data view. titleId is the modal's
  // aria-labelledby target; the data view passes none, so the id stays unique.
  function historyHTML(b, titleId) {
    const [kindLabel, swatch] = KIND[b.kind];
    return (
      `<div class="modal-kind"><svg width="18" height="8" aria-hidden="true">${swatch}</svg>${b.tag || kindLabel}</div>` +
      `<div class="modal-title"${titleId ? ` id="${titleId}"` : ''}>${b.title || name(b.a) + ' – ' + name(b.b)}</div>` +
      (b.note ? `<div class="modal-note">${b.note}</div>` : '') +
      (b.from ? `<div class="modal-from">From the matrix entry for ${b.from.replace(/ \(UT\)| \(NCT\)/g, '')}:</div>` : '') +
      `<div class="modal-text">${b.text}</div>` +
      (b.source ? `<div class="modal-source">${b.source}</div>` : '') +
      (b.timeline
        ? `<div class="modal-timeline-head">Timeline</div><ol class="modal-timeline">` +
          b.timeline.map(([when, what]) => `<li><b>${when}</b><span>${what}</span></li>`).join('') + '</ol>'
        : '') +
      (b.text.includes('class="revision"') ? `<div class="modal-foot">Blue text: correction or update added in the matrix</div>` : ''));
  }

  function renderModal(b) {
    modalBody.innerHTML = historyHTML(b, 'modal-title');
  }

  function openModal(b) {
    renderModal(b);
    lastFocused = document.activeElement;
    modalBackdrop.hidden = false;
    document.body.style.overflow = 'hidden';
    document.querySelector('.modal').scrollTop = 0;
    document.getElementById('modal-close').focus();
  }
  function closeModal() {
    if (modalBackdrop.hidden) return;
    modalBackdrop.hidden = true;
    document.body.style.overflow = '';
    if (lastFocused && lastFocused.focus) lastFocused.focus();
  }
  document.getElementById('modal-close').addEventListener('click', closeModal);
  modalBackdrop.addEventListener('click', (e) => { if (e.target === modalBackdrop) closeModal(); });
  addEventListener('keydown', (e) => { if (e.key === 'Escape') closeModal(); });

  function placeTip(x, y) {
    const gap = 16, margin = 8;
    const w = tip.offsetWidth, h = tip.offsetHeight;
    let left = x + gap;
    if (left + w > innerWidth - margin) left = Math.max(margin, x - gap - w);
    let top = y + gap;
    if (top + h > innerHeight - margin) top = Math.max(margin, y - gap - h);
    tip.style.transform = `translate(${left}px, ${top}px)`;
  }

  // 5. Thicken whichever border the pointer is over and show its (minimal) hover box.
  let current = null;
  function setHovered(line) {
    if (line === current) return;
    if (current) current.classList.remove('is-hovered');
    current = line;
    if (current) {
      current.classList.add('is-hovered');
      renderTip(info.get(current));
    }
    tip.hidden = !current;
  }
  function onPointer(e) {
    const border = e.target.dataset && e.target.dataset.border;
    setHovered(border !== undefined ? lines[border] : null);
    if (current) placeTip(e.clientX, e.clientY);
  }
  svg.addEventListener('pointerover', onPointer);
  svg.addEventListener('pointermove', onPointer);
  svg.addEventListener('pointerleave', () => setHovered(null));

  // Clicking (or tapping) a border opens its full history in the modal.
  svg.addEventListener('click', (e) => {
    const border = e.target.dataset && e.target.dataset.border;
    if (border === undefined) return;
    tip.hidden = true;
    openModal(info.get(lines[border]));
  });

  // 6. Stroke widths and label sizes are in SVG user units, and the map is scaled
  //    to fit the window, so keep "1 screen px" in user units up to date.
  function updateScale() {
    const ctm = svg.getScreenCTM();
    if (!ctm || !ctm.a) return;
    svg.style.setProperty('--px', (1 / ctm.a) + 'px');
    // Label size just changed: end each leader line at the nearest edge of its label.
    for (const { line, text, lx, ly } of leaders) {
      const box = text.getBBox();
      line.setAttribute('x2', Math.max(box.x, Math.min(lx, box.x + box.width)));
      line.setAttribute('y2', Math.max(box.y, Math.min(ly, box.y + box.height)));
    }
  }
  updateScale();
  addEventListener('resize', updateScale);
  if ('ResizeObserver' in window) new ResizeObserver(updateScale).observe(svg);

  // 7. The two views. The map is one way to reach a border's history; the data view
  //    is the other, reading the same DATA.borders entries through two dropdowns.
  const tabs = [...document.querySelectorAll('.tab')];
  const view = tab => document.getElementById(tab.getAttribute('aria-controls'));
  function showTab(tab) {
    for (const t of tabs) {
      const on = t === tab;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
      view(t).hidden = !on;
    }
    // The map cannot be measured while hidden, so its scale is stale on the way back.
    if (view(tab).contains(svg)) updateScale();
  }
  for (const tab of tabs) {
    tab.addEventListener('click', () => showTab(tab));
    tab.addEventListener('keydown', (e) => {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      const step = e.key === 'ArrowRight' ? 1 : tabs.length - 1;
      const next = tabs[(tabs.indexOf(tab) + step) % tabs.length];
      showTab(next);
      next.focus();
    });
  }

  // Every border indexed by the pair it separates, and who borders whom. A pair can
  // hold several lines (a claim line, the Line of Control beside it); lines that
  // would read identically are folded into one.
  const ORDER = ['internal', 'external', 'loc', 'lac', 'defacto'];
  const pairKey = (a, b) => [a, b].sort().join('|');
  const pairs = new Map();
  const partners = new Map();
  const indian = new Set();
  for (const border of Object.values(DATA.borders).flat(2)) {
    const key = pairKey(border.a, border.b);
    if (!pairs.has(key)) pairs.set(key, []);
    const lines = pairs.get(key);
    const sig = JSON.stringify([border.kind, border.tag, border.title, border.note, border.text]);
    if (!lines.some(l => l.sig === sig)) lines.push({ sig, border });
    for (const [x, y] of [[border.a, border.b], [border.b, border.a]]) {
      if (!partners.has(x)) partners.set(x, new Set());
      partners.get(x).add(y);
    }
    if (border.kind === 'internal') { indian.add(border.a); indian.add(border.b); }
  }
  for (const lines of pairs.values()) lines.sort((p, q) => ORDER.indexOf(p.border.kind) - ORDER.indexOf(q.border.kind));

  // A name that never appears on an internal border belongs to a neighbouring country.
  const places = [...partners.keys()].sort((x, y) => name(x).localeCompare(name(y)));
  const GROUPS = [
    ['States and union territories', places.filter(n => indian.has(n))],
    ['Neighbouring countries', places.filter(n => !indian.has(n))],
  ];

  const pickA = document.getElementById('pick-a');
  const pickB = document.getElementById('pick-b');
  const showBtn = document.getElementById('show-timeline');
  const result = document.getElementById('data-result');

  // Refill a dropdown with the places still possible, keeping its choice if it survives.
  function fill(select, allowed) {
    const chosen = select.value;
    select.textContent = '';
    select.append(new Option(allowed ? 'Choose a neighbour…' : 'Choose…', ''));
    for (const [label, names] of GROUPS) {
      const list = allowed ? names.filter(n => allowed.has(n)) : names;
      if (!list.length) continue;
      const group = document.createElement('optgroup');
      group.label = label;
      for (const n of list) group.append(new Option(name(n), n));
      select.append(group);
    }
    select.value = [...select.options].some(o => o.value === chosen) ? chosen : '';
  }

  // The first dropdown always offers every place; the second one narrows to the
  // places the first actually borders. (Narrowing both ways would mean a chosen
  // neighbour could shrink the first list out from under the next question.)
  fill(pickA, null);
  fill(pickB, null);
  pickA.addEventListener('change', () => {
    fill(pickB, pickA.value ? partners.get(pickA.value) : null);
    ready();
  });
  pickB.addEventListener('change', ready);

  function ready() {
    showBtn.disabled = !(pickA.value && pickB.value);
    result.textContent = '';   // what is on screen is no longer the question being asked
  }

  showBtn.addEventListener('click', () => {
    const lines = pairs.get(pairKey(pickA.value, pickB.value));
    if (!lines) return;
    const [first, ...rest] = lines;
    const more = rest.map(({ border }) => {
      const [kindLabel, swatch] = KIND[border.kind];
      return '<div class="history-more-item">' +
        `<div class="modal-kind"><svg width="18" height="8" aria-hidden="true">${swatch}</svg>${border.tag || kindLabel}</div>` +
        (border.title ? `<div class="history-more-title">${border.title}</div>` : '') +
        (border.note ? `<div class="modal-note">${border.note}</div>` : '') +
        '</div>';
    }).join('');
    result.innerHTML = '<div class="history">' + historyHTML(first.border) +
      (rest.length ? '<div class="history-more"><div class="history-more-head">Also drawn along this border</div>' + more + '</div>' : '') +
      '</div>';
  });
})();
