// Builds dist/feedback-service.zip, the one bundle both Lambdas deploy from: the handlers,
// config, RDS CA bundle and the production node_modules. Written here rather than with a
// zip tool so every entry carries Unix read permissions, which Lambda needs; zips made by
// Windows tools often lack them.
import { execSync } from 'node:child_process';
import { mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { crc32, deflateRawSync } from 'node:zlib';

const ROOT = fileURLToPath(new URL('..', import.meta.url));
const OUT = join(ROOT, 'dist', 'feedback-service.zip');
const FILES = ['submit.mjs', 'digest.mjs', 'migrate.mjs', 'schema.sql', 'db.mjs', 'config.mjs', 'config.json', 'global-bundle.pem', 'package.json'];

// Production dependencies only (pg and what it pulls in), as npm resolved them.
const deps = execSync('npm ls --omit=dev --all --parseable', { cwd: ROOT, encoding: 'utf8' })
  .split(/\r?\n/).filter(p => p && relative(ROOT, p).startsWith('node_modules'));
if (!deps.length) throw new Error('No node_modules found: run npm install first');

const paths = [...FILES.map(f => join(ROOT, f)), ...deps.flatMap(walk)];
const entries = [...new Set(paths)].sort().map(p => ({ name: relative(ROOT, p).split(sep).join('/'), data: readFileSync(p) }));

mkdirSync(join(ROOT, 'dist'), { recursive: true });
writeFileSync(OUT, zip(entries));
console.log(`${relative(ROOT, OUT)}: ${entries.length} files, ${(statSync(OUT).size / 1024).toFixed(0)} KB`);

function walk(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap(d => {
    const p = join(dir, d.name);
    return d.isDirectory() ? walk(p) : d.isFile() ? [p] : [];
  });
}

function zip(files) {
  const DOS_TIME = 0, DOS_DATE = (2020 - 1980) << 9 | 1 << 5 | 1;   // fixed, so rebuilds are identical
  const UNIX_FILE = (0o100644 << 16) >>> 0;                        // regular file, rw-r--r--
  const locals = [], centrals = [];
  let offset = 0;
  for (const { name, data } of files) {
    const nameBuf = Buffer.from(name, 'utf8');
    const packed = deflateRawSync(data, { level: 9 });
    const stored = packed.length >= data.length;
    const body = stored ? data : packed;
    const crc = crc32(data);

    const local = Buffer.alloc(30);
    local.writeUInt32LE(0x04034b50, 0);
    local.writeUInt16LE(20, 4);                  // version needed
    local.writeUInt16LE(0x0800, 6);              // UTF-8 names
    local.writeUInt16LE(stored ? 0 : 8, 8);
    local.writeUInt16LE(DOS_TIME, 10);
    local.writeUInt16LE(DOS_DATE, 12);
    local.writeUInt32LE(crc, 14);
    local.writeUInt32LE(body.length, 18);
    local.writeUInt32LE(data.length, 22);
    local.writeUInt16LE(nameBuf.length, 26);
    locals.push(local, nameBuf, body);

    const central = Buffer.alloc(46);
    central.writeUInt32LE(0x02014b50, 0);
    central.writeUInt16LE(3 << 8 | 20, 4);       // made by Unix, so the permissions below apply
    central.writeUInt16LE(20, 6);
    central.writeUInt16LE(0x0800, 8);
    central.writeUInt16LE(stored ? 0 : 8, 10);
    central.writeUInt16LE(DOS_TIME, 12);
    central.writeUInt16LE(DOS_DATE, 14);
    central.writeUInt32LE(crc, 16);
    central.writeUInt32LE(body.length, 20);
    central.writeUInt32LE(data.length, 24);
    central.writeUInt16LE(nameBuf.length, 28);
    central.writeUInt32LE(UNIX_FILE, 38);
    central.writeUInt32LE(offset, 42);
    centrals.push(central, nameBuf);

    offset += local.length + nameBuf.length + body.length;
  }
  const dir = Buffer.concat(centrals);
  const end = Buffer.alloc(22);
  end.writeUInt32LE(0x06054b50, 0);
  end.writeUInt16LE(files.length, 8);
  end.writeUInt16LE(files.length, 10);
  end.writeUInt32LE(dir.length, 12);
  end.writeUInt32LE(offset, 16);
  return Buffer.concat([...locals, dir, end]);
}
