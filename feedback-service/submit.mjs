// Lambda behind a Function URL: validates one feedback submission and stores it.
import { config } from './config.mjs';
import { query } from './db.mjs';

export const deps = { query };

const MAX_BODY_BYTES = 8 * 1024;
const MAX_MESSAGE = 1000;
const MAX_EMAIL = 254;
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export async function handler(event) {
  try {
    if (event.requestContext?.http?.method !== 'POST') return reply(405, 'Use POST');

    const raw = Buffer.from(event.body ?? '', event.isBase64Encoded ? 'base64' : 'utf8');
    if (raw.length > MAX_BODY_BYTES) return reply(413, 'Request too large');

    let body;
    try { body = JSON.parse(raw.toString('utf8')); } catch { return reply(400, 'Body must be JSON'); }
    if (!body || typeof body !== 'object' || Array.isArray(body)) return reply(400, 'Body must be a JSON object');

    // Honeypot: hidden from people, so only bots fill it. They get a success and nothing is stored.
    if (body.website) return reply(200);

    const feedback = validate(body);
    if (typeof feedback === 'string') return reply(400, feedback);

    console.log(JSON.stringify({ event: 'FEEDBACK', ...feedback, ip: event.requestContext.http.sourceIp }));
    await deps.query(
      'INSERT INTO feedback (category, email_id, message) VALUES ($1, $2, $3)',
      [feedback.category, feedback.email, feedback.message],
    );
    return reply(200);
  } catch (err) {
    console.error(JSON.stringify({ event: 'FEEDBACK_FAILED', message: err.message }));
    return reply(500, 'Could not save feedback');
  }
}

function validate(body) {
  const { category, message } = body;
  if (!Number.isInteger(category) || !Object.hasOwn(config.categories, String(category))) return 'Unknown category';

  if (typeof message !== 'string') return 'Message is required';
  const text = message.trim();
  if (!text) return 'Message is required';
  if (text.length > MAX_MESSAGE) return `Message is over ${MAX_MESSAGE} characters`;
  // PostgreSQL text cannot hold NUL.
  if (text.includes(String.fromCharCode(0))) return 'Message contains an invalid character';

  let email = body.email ?? '';
  if (typeof email !== 'string') return 'Email must be text';
  email = email.trim();
  if (email && (email.length > MAX_EMAIL || !EMAIL.test(email))) return 'Email address is not valid';

  return { category, email: email || null, message: text };
}

function reply(statusCode, error) {
  return {
    statusCode,
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(statusCode === 200 ? { ok: true } : { error }),
  };
}
