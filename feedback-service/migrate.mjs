// Applies schema.sql. The database is private, so the deploy runs this Lambda (inside the VPC)
// instead of connecting itself; schema.sql is idempotent, so running it again is harmless.
import { readFileSync } from 'node:fs';
import { query } from './db.mjs';

export async function handler() {
  await query(readFileSync(new URL('./schema.sql', import.meta.url), 'utf8'));
  console.log(JSON.stringify({ event: 'MIGRATE', ok: true }));
  return { ok: true };
}
