import { spawn } from 'node:child_process';
import { writeFileSync, mkdirSync } from 'node:fs';

const SCRATCH = (process.env.TEMP || '.').split('\\').join('/');  // screenshots + chrome profile go here
const URL_ = 'file:///D:/OneDrive/Documents/INDIA_BORDERS/india-borders.html';
const [W, H] = process.argv.slice(2).map(Number);
const PORT = 9333 + (W % 100);
mkdirSync(`${SCRATCH}/chrome-profile-${W}`, { recursive: true });

const chrome = spawn('C:/Program Files/Google/Chrome/Application/chrome.exe', [
  '--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${SCRATCH}/chrome-profile-${W}`,
  `--window-size=${W},${H}`, '--no-first-run', '--disable-gpu', URL_,
], { stdio: 'ignore' });

const sleep = ms => new Promise(r => setTimeout(r, ms));
let target;
for (let i = 0; i < 50 && !target; i++) {
  await sleep(200);
  try { target = (await (await fetch(`http://127.0.0.1:${PORT}/json`)).json()).find(t => t.type === 'page'); } catch {}
}
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise(r => ws.addEventListener('open', r));
let id = 0; const pending = new Map(); const errors = [];
ws.addEventListener('message', e => {
  const m = JSON.parse(e.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
  if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails);
  if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') errors.push(m.params.args);
});
const send = (method, params = {}) => new Promise(r => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const evaluate = async expr => (await send('Runtime.evaluate', { expression: expr, returnByValue: true })).result.result.value;
await send('Runtime.enable');
await sleep(800);

const info = await evaluate(`(() => {
  const svg = document.querySelector('.map > svg:not(.corner)');
  const ctm = svg.getScreenCTM();
  const borders = [...svg.querySelectorAll('.border-line')].map((line, i) => {
    line.dataset.idx = i; const g = line;
    const len = line.getTotalLength();
    const pts = [0.5, 0.3, 0.7, 0.15, 0.85, 0.05, 0.95].map(f => {
      const p = line.getPointAtLength(len * f).matrixTransform(line.getScreenCTM());
      return [p.x, p.y];
    });
    const mid = line.getPointAtLength(len * 0.5);
    return { idx: i, svg: [mid.x, mid.y], kind: g.dataset.kind || (line.closest('g').getAttribute('stroke-dasharray') ? 'loc-lac' : line.closest('g').getAttribute('stroke')), base: parseFloat(line.style.getPropertyValue('--w')), pts };
  });
  const coast = [...svg.querySelectorAll('.coastline path')].map(p => {
    const q = p.getPointAtLength(p.getTotalLength() * 0.5).matrixTransform(p.getScreenCTM());
    return [q.x, q.y];
  });
  return { scale: ctm.a, svgW: svg.getBoundingClientRect().width, borders, coast,
    counts: [...svg.querySelectorAll('.border-line')].reduce((a, g) => (a[g.dataset.kind] = (a[g.dataset.kind] || 0) + 1, a), {}) };
})()`);

const probe = `(() => {
  const g = document.querySelector('.border-line.is-hovered');
  if (!g) return null;
  const line = g;
  const el = document.elementFromPoint(window.__x, window.__y);
  const tip = document.querySelector('.tip'); const r = tip.getBoundingClientRect();
  return { idx: +g.dataset.idx, sw: parseFloat(getComputedStyle(line).strokeWidth), cursor: getComputedStyle(el).cursor,
    title: tip.hidden ? null : tip.querySelector('.tip-title').textContent,
    kind: tip.hidden ? null : tip.querySelector('.tip-kind').textContent,
    inView: r.left >= 0 && r.top >= 0 && r.right <= innerWidth && r.bottom <= innerHeight };
})()`;
const move = async (x, y) => {
  await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y });
  await evaluate(`window.__x=${x};window.__y=${y}`);
};

const failures = []; const widthErrors = []; let samples = 0, wrong = 0; const titles = [];
for (const b of info.borders) {
  let ok = false;
  for (const [x, y] of b.pts) {
    await move(x, y);
    const r = await evaluate(probe);
    samples++; if (!r || r.idx !== b.idx) wrong++;
    if (r && r.idx === b.idx) {
      ok = true;
      const screenGrow = (r.sw - b.base) * info.scale;
      if (Math.abs(screenGrow - 2) > 0.01 || r.cursor !== 'pointer' || !r.title || !r.inView) widthErrors.push({ idx: b.idx, screenGrow, cursor: r.cursor, title: r.title, inView: r.inView });
      titles.push(`${b.idx} ${b.kind} @(${Math.round(b.svg[0])},${Math.round(b.svg[1])}) -> [${r.kind}] ${r.title}`);
      break;
    }
  }
  if (!ok) failures.push(b.idx + ':' + b.kind);
}

// Away from everything and on coastlines: no border should be hovered.
let coastHovered = 0;
for (const [x, y] of info.coast) {
  await move(x, y);
  const r = await evaluate(probe);
  const cursor = await evaluate(`getComputedStyle(document.elementFromPoint(${x},${y})).cursor`);
  if (r || cursor === 'pointer') { coastHovered++; console.log('coast point hovers border', x.toFixed(1), y.toFixed(1), r && info.borders[r.idx].kind); }
}

console.log(titles.join(String.fromCharCode(10)));
// Screenshot with one external and see it thickened.
const ext = info.borders[29];
await move(...ext.pts[0]);
const shot = await send('Page.captureScreenshot', { format: 'png', clip: { x: ext.pts[0][0] - 60, y: ext.pts[0][1] - 60, width: 120, height: 120, scale: 3 } });
writeFileSync(`${SCRATCH}/hover-${W}.png`, Buffer.from(shot.result.data, 'base64'));
await move(5, 5);
const shot2 = await send('Page.captureScreenshot', { format: 'png', clip: { x: ext.pts[0][0] - 60, y: ext.pts[0][1] - 60, width: 120, height: 120, scale: 3 } });
writeFileSync(`${SCRATCH}/nohover-${W}.png`, Buffer.from(shot2.result.data, 'base64'));
for (const [n, bi] of [['rjhr', 36]]) {
  for (const p of info.borders[bi].pts) {
    await move(...p);
    const r = await evaluate(probe);
    if (r && r.idx === bi) break;
  }
  const dims = await evaluate(`(() => { const r = document.querySelector('.tip').getBoundingClientRect(); return [Math.round(r.width), Math.round(r.height), Math.round(r.top), innerHeight]; })()`);
  console.log('TIPDIMS', n, JSON.stringify(dims));
  const sh = await send('Page.captureScreenshot', { format: 'png' });
  writeFileSync(`${SCRATCH}/tip-${n}-${W}.png`, Buffer.from(sh.result.data, 'base64'));
}
await move(5, 5);
const full = await send('Page.captureScreenshot', { format: 'png' });
writeFileSync(`${SCRATCH}/full-${W}.png`, Buffer.from(full.result.data, 'base64'));

console.log(JSON.stringify({ viewport: [W, H], scale: info.scale, svgW: info.svgW, counts: info.counts,
  unreachable: failures, onLineSamplesPickingOtherBorder: `${wrong}/${samples}`, widthOrCursorErrors: widthErrors, coastlinePointsTriggeringHover: `${coastHovered}/${info.coast.length}`, jsErrors: errors }, null, 1));
ws.close(); chrome.kill();
process.exit(0);
