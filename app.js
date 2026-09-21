document.getElementById('refs-list').innerHTML = REFS_HTML;

(function () {
  const NS = 'http://www.w3.org/2000/svg';
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

  function renderModal(b) {
    const [kindLabel, swatch] = KIND[b.kind];
    modalBody.innerHTML =
      `<div class="modal-kind"><svg width="18" height="8" aria-hidden="true">${swatch}</svg>${b.tag || kindLabel}</div>` +
      `<div class="modal-title" id="modal-title">${b.title || name(b.a) + ' – ' + name(b.b)}</div>` +
      (b.note ? `<div class="modal-note">${b.note}</div>` : '') +
      (b.from ? `<div class="modal-from">From the matrix entry for ${b.from.replace(/ \(UT\)| \(NCT\)/g, '')}:</div>` : '') +
      `<div class="modal-text">${b.text}</div>` +
      (b.source ? `<div class="modal-source">${b.source}</div>` : '') +
      (b.timeline
        ? `<div class="modal-timeline-head">Timeline</div><ol class="modal-timeline">` +
          b.timeline.map(([when, what]) => `<li><b>${when}</b><span>${what}</span></li>`).join('') + '</ol>'
        : '') +
      (b.text.includes('class="revision"') ? `<div class="modal-foot">Blue text: correction or update added in the matrix</div>` : '');
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
})();
