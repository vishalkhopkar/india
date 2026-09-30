import { test, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { handler, deps, localDate } from '../digest.mjs';

let rows, queries, published;
beforeEach(t => {
  process.env.TOPIC_ARN = 'arn:aws:sns:us-east-1:123456789012:feedback';
  rows = [];
  queries = [];
  published = [];
  deps.query = async (text, params) => {
    queries.push({ text, params });
    return { rows: text.startsWith('SELECT') ? rows : [] };
  };
  deps.publish = async params => { published.push(params); };
  // 01:30 UTC on 30 Sep is 20:30 CDT on 29 Sep: the digest date must be the Central one.
  deps.now = () => new Date('2026-09-30T01:30:00Z');
  t.mock.method(console, 'log', () => {});
});

const row = (id, over = {}) => ({
  id, category: 0, email_id: null, message: `Message ${id}`,
  recv_date: new Date('2026-09-29T14:05:00Z'), ...over,
});
const updates = () => queries.filter(q => q.text.startsWith('UPDATE'));

test('no unsent rows: no email and nothing marked', async () => {
  assert.deepEqual(await handler(), { feedback: 0, emails: 0 });
  assert.equal(published.length, 0);
  assert.equal(updates().length, 0);
});

test('unsent rows go out in one email, then exactly those ids are marked', async () => {
  rows = [row(3), row(7, { category: 1, email_id: 'reader@example.com', message: 'Great work' })];
  assert.deepEqual(await handler(), { feedback: 2, emails: 1 });

  assert.equal(published.length, 1);
  const [mail] = published;
  assert.equal(mail.TopicArn, process.env.TOPIC_ARN);
  assert.equal(mail.Subject, '[India borders] 2 new feedback - 2026-09-29');
  assert.match(mail.Subject, /^[\x20-\x7e]{1,99}$/);   // SNS: ASCII, under 100 characters
  assert.match(mail.Message, /#1 {2}Report incorrect information\nReceived: Sep 29, 2026, 9:05 AM CDT\nFrom: not given\n\nMessage 3/);
  assert.match(mail.Message, /#2 {2}General feedback\n.*\nFrom: reader@example.com\n\nGreat work/);

  assert.equal(updates().length, 1);
  assert.deepEqual(updates()[0].params, ['2026-09-29', [3, 7]]);
});

test('the SELECT reads only unsent rows, oldest first', async () => {
  await handler();
  assert.match(queries[0].text, /WHERE NOT sent ORDER BY id$/);
});

test('an unknown category still reads sensibly', async () => {
  rows = [row(1, { category: 5 })];
  await handler();
  assert.match(published[0].Message, /#1 {2}Category 5\n/);
});

test('a failed publish marks nothing and fails the run', async () => {
  rows = [row(1), row(2)];
  deps.publish = async () => { throw new Error('SNS unreachable'); };
  await assert.rejects(handler(), /SNS unreachable/);
  assert.equal(updates().length, 0);
});

test('a digest over the SNS size limit is split, each part marked after it is sent', async () => {
  rows = Array.from({ length: 300 }, (_, i) => row(i + 1, { message: 'ह'.repeat(1000) }));   // 3 bytes a character
  const order = [];
  deps.publish = async p => { published.push(p); order.push('publish'); };
  const query = deps.query;
  deps.query = async (text, params) => { if (text.startsWith('UPDATE')) order.push('update'); return query(text, params); };

  const result = await handler();
  assert.ok(result.emails > 1);
  assert.equal(published.length, result.emails);
  for (const p of published) assert.ok(Buffer.byteLength(p.Message) < 256 * 1024);
  assert.match(published[0].Subject, /\(part 1 of \d+\)$/);
  assert.deepEqual(order, published.flatMap(() => ['publish', 'update']));
  assert.deepEqual(updates().flatMap(u => u.params[1]), rows.map(r => r.id));
});

test('a missing TOPIC_ARN fails before touching the database', async () => {
  delete process.env.TOPIC_ARN;
  await assert.rejects(handler(), /TOPIC_ARN/);
  assert.equal(queries.length, 0);
});

test('localDate uses Central time across the day boundary and DST', () => {
  assert.equal(localDate(new Date('2026-09-30T01:30:00Z')), '2026-09-29');   // CDT, UTC-5
  assert.equal(localDate(new Date('2026-09-30T05:30:00Z')), '2026-09-30');
  assert.equal(localDate(new Date('2026-12-15T05:30:00Z')), '2026-12-14');   // CST, UTC-6
});
