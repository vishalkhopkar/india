import { readFileSync } from 'node:fs';
import pg from 'pg';

// Connection settings come from the standard PGHOST, PGPORT, PGUSER, PGPASSWORD and
// PGDATABASE environment variables. One connection per Lambda instance, reused while warm.
let pool;

export function query(text, params) {
  pool ??= createPool();
  return pool.query(text, params);
}

export async function end() {
  await pool?.end();
  pool = undefined;
}

function createPool() {
  const p = new pg.Pool({
    max: 1,
    connectionTimeoutMillis: 5000,
    // RDS is reached over verified TLS; PGSSLMODE=disable is only for a local test database.
    ssl: process.env.PGSSLMODE === 'disable' ? false : {
      rejectUnauthorized: true,
      ca: readFileSync(new URL('./global-bundle.pem', import.meta.url), 'utf8'),
    },
  });
  // A connection dropped while the Lambda was frozen must not crash the next invocation.
  p.on('error', err => console.error(JSON.stringify({ event: 'PG_POOL_ERROR', message: err.message })));
  return p;
}
