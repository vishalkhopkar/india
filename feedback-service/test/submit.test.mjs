import { test, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import { handler, deps } from '../submit.mjs';

let calls;
beforeEach(t => {
  calls = [];
  deps.query = async (text, params) => { calls.push({ text, params }); return { rows: [] }; };
  t.mock.method(console, 'log', () => {});
  t.mock.method(console, 'error', () => {});
});

const post = (body, extra = {}) => handler({
  requestContext: { http: { method: 'POST', sourceIp: '203.0.113.9' } },
  body: typeof body === 'string' ? body : JSON.stringify(body),
  isBase64Encoded: false,
  ...extra,
});

test('valid feedback is stored and answered with 200', async () => {
  const res = await post({ category: 0, message: '  Ladakh date is wrong  ', email: ' a@b.co ', website: '' });
  assert.equal(res.statusCode, 200);
  assert.deepEqual(JSON.parse(res.body), { ok: true });
  assert.equal(calls.length, 1);
  assert.match(calls[0].text, /^INSERT INTO feedback \(category, email_id, message\)/);
  assert.deepEqual(calls[0].params, [0, 'a@b.co', 'Ladakh date is wrong']);
});

test('email is optional and stored as null when blank or missing', async () => {
  await post({ category: 1, message: 'Nice map', email: '   ' });
  await post({ category: 1, message: 'Nice map' });
  assert.deepEqual(calls.map(c => c.params[1]), [null, null]);
});

test('a base64-encoded body is decoded', async () => {
  const body = Buffer.from(JSON.stringify({ category: 1, message: 'hi' })).toString('base64');
  assert.equal((await post(body, { isBase64Encoded: true })).statusCode, 200);
  assert.equal(calls.length, 1);
});

test('a message of exactly 1000 characters is accepted', async () => {
  assert.equal((await post({ category: 0, message: 'x'.repeat(1000) })).statusCode, 200);
});

for (const [name, body] of [
  ['unknown category', { category: 2, message: 'hi' }],
  ['negative category', { category: -1, message: 'hi' }],
  ['category as string', { category: '0', message: 'hi' }],
  ['fractional category', { category: 0.5, message: 'hi' }],
  ['inherited key as category', { category: 'toString', message: 'hi' }],
  ['missing message', { category: 0 }],
  ['blank message', { category: 0, message: ' \n ' }],
  ['message over 1000 characters', { category: 0, message: 'x'.repeat(1001) }],
  ['message with NUL', { category: 0, message: 'a' + String.fromCharCode(0) + 'b' }],
  ['bad email', { category: 0, message: 'hi', email: 'not-an-email' }],
  ['email over 254 characters', { category: 0, message: 'hi', email: 'a'.repeat(250) + '@b.co' }],
  ['email not a string', { category: 0, message: 'hi', email: 42 }],
  ['JSON array', [1, 2]],
  ['JSON null', 'null'],
  ['invalid JSON', '{nope'],
]) {
  test(`400 and nothing stored: ${name}`, async () => {
    const res = await post(body);
    assert.equal(res.statusCode, 400);
    assert.ok(JSON.parse(res.body).error);
    assert.equal(calls.length, 0);
  });
}

test('an oversized body is refused with 413', async () => {
  const res = await post({ category: 0, message: 'x', pad: 'y'.repeat(9000) });
  assert.equal(res.statusCode, 413);
  assert.equal(calls.length, 0);
});

test('anything but POST is refused with 405', async () => {
  const res = await handler({ requestContext: { http: { method: 'GET' } } });
  assert.equal(res.statusCode, 405);
  assert.equal(calls.length, 0);
});

test('a filled honeypot gets 200 but nothing is stored', async () => {
  const res = await post({ category: 0, message: 'buy now', website: 'http://spam.example' });
  assert.equal(res.statusCode, 200);
  assert.equal(calls.length, 0);
});

test('a database failure answers 500', async () => {
  deps.query = async () => { throw new Error('connection refused'); };
  const res = await post({ category: 0, message: 'hi' });
  assert.equal(res.statusCode, 500);
});
