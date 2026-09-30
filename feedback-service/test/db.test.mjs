// Runs both handlers against a real PostgreSQL. Skipped unless FEEDBACK_TEST_DB=1 and the
// PG* variables point at a disposable database: it drops and recreates the feedback table.
import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { query, end } from '../db.mjs';
import * as submit from '../submit.mjs';
import * as digest from '../digest.mjs';
import * as migrate from '../migrate.mjs';

const skip = process.env.FEEDBACK_TEST_DB !== '1' && 'set FEEDBACK_TEST_DB=1 and PG* to run';
const published = [];

before(async () => {
  if (skip) return;
  // Feedback arrives in any script (Devanagari included); RDS databases are UTF8 by default.
  assert.equal((await query('SHOW server_encoding')).rows[0].server_encoding, 'UTF8', 'test database must be UTF8');
  await query('DROP TABLE IF EXISTS feedback');
  // The deploy's own path to the schema, run twice: it must be safe to repeat.
  await migrate.handler();
  await migrate.handler();
  process.env.TOPIC_ARN = 'arn:aws:sns:us-east-1:123456789012:feedback';
  digest.deps.publish = async p => { published.push(p); };
});
after(() => !skip && end());

const post = body => submit.handler({
  requestContext: { http: { method: 'POST', sourceIp: '203.0.113.9' } },
  body: JSON.stringify(body),
});

test('submit, digest, and a second digest with nothing new', { skip }, async t => {
  t.mock.method(console, 'log', () => {});
  assert.equal((await post({ category: 0, message: 'Ladakh date is wrong', email: 'a@b.co' })).statusCode, 200);
  assert.equal((await post({ category: 1, message: 'ह'.repeat(1000) })).statusCode, 200);   // 1000 characters fits varchar(1000)

  const { rows: stored } = await query('SELECT * FROM feedback ORDER BY id');
  assert.equal(stored.length, 2);
  assert.deepEqual(stored.map(r => [r.id, r.category, r.email_id, r.sent, r.sent_date]),
    [[1, 0, 'a@b.co', false, null], [2, 1, null, false, null]]);
  assert.ok(Math.abs(stored[0].recv_date - Date.now()) < 60_000);

  digest.deps.now = () => new Date('2026-09-30T01:00:00Z');   // 20:00 CDT on 29 Sep
  assert.deepEqual(await digest.handler(), { feedback: 2, emails: 1 });
  assert.equal(published.length, 1);
  assert.match(published[0].Message, /Ladakh date is wrong/);

  const { rows: marked } = await query(`SELECT id, sent, to_char(sent_date, 'YYYY-MM-DD') AS day FROM feedback ORDER BY id`);
  assert.deepEqual(marked, [{ id: 1, sent: true, day: '2026-09-29' }, { id: 2, sent: true, day: '2026-09-29' }]);

  assert.deepEqual(await digest.handler(), { feedback: 0, emails: 0 });
  assert.equal(published.length, 1);

  // Arrives after a digest: waits, unsent, for the next one.
  await post({ category: 1, message: 'Later' });
  const { rows: later } = await query('SELECT id, sent FROM feedback WHERE NOT sent');
  assert.deepEqual(later, [{ id: 3, sent: false }]);
});

test('the table itself refuses what validation would', { skip }, async () => {
  await assert.rejects(query('INSERT INTO feedback (category, message) VALUES (-1, $1)', ['x']), /check constraint/);
  await assert.rejects(query('INSERT INTO feedback (category, message) VALUES (0, $1)', ['x'.repeat(1001)]), /too long/);
  await assert.rejects(query('INSERT INTO feedback (category) VALUES (0)'), /null value/);
});
