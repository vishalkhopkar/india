// Scheduled Lambda: emails every unsent feedback row as one SNS message, then marks them sent.
import { config } from './config.mjs';
import { query } from './db.mjs';

let sns;
export const deps = {
  query,
  publish: async params => {
    // Provided by the Lambda Node.js runtime, so it is not bundled.
    const { SNSClient, PublishCommand } = await import('@aws-sdk/client-sns');
    sns ??= new SNSClient({});
    return sns.send(new PublishCommand(params));
  },
  now: () => new Date(),
};

// SNS caps a message at 256 KB; stay well under it so the footer SNS adds still fits.
const MAX_EMAIL_BYTES = 200 * 1024;
const RULE = '-'.repeat(48);

export async function handler() {
  const topic = process.env.TOPIC_ARN;
  if (!topic) throw new Error('TOPIC_ARN is not set');

  const { rows } = await deps.query(
    'SELECT id, category, email_id, message, recv_date FROM feedback WHERE NOT sent ORDER BY id',
  );
  if (rows.length === 0) {
    console.log(JSON.stringify({ event: 'DIGEST', feedback: 0, emails: 0 }));
    return { feedback: 0, emails: 0 };
  }

  const day = localDate(deps.now());
  const parts = split(rows.map((row, i) => ({ id: row.id, text: entry(row, i + 1) })));

  // Each part is marked only after it is published: a failed publish leaves its rows for
  // the next run, and rows that arrive mid-run are never marked without being emailed.
  for (const [i, part] of parts.entries()) {
    const of = parts.length > 1 ? ` (part ${i + 1} of ${parts.length})` : '';
    await deps.publish({
      TopicArn: topic,
      // SNS subjects must be ASCII, hence the plain hyphen.
      Subject: `[India borders] ${rows.length} new feedback - ${day}${of}`,
      Message: `${rows.length} new feedback since the last digest${of}.\n\n${RULE}\n\n` +
        part.map(e => e.text).join(''),
    });
    await deps.query(
      'UPDATE feedback SET sent = true, sent_date = $1 WHERE id = ANY($2::int[])',
      [day, part.map(e => e.id)],
    );
  }

  console.log(JSON.stringify({ event: 'DIGEST', feedback: rows.length, emails: parts.length, day }));
  return { feedback: rows.length, emails: parts.length };
}

function entry(row, n) {
  const label = config.categories[String(row.category)] ?? `Category ${row.category}`;
  return `#${n}  ${label}\n` +
    `Received: ${receivedAt(row.recv_date)}\n` +
    `From: ${row.email_id ?? 'not given'}\n\n` +
    `${row.message}\n\n${RULE}\n\n`;
}

function split(entries) {
  const parts = [];
  let current = [], size = 0;
  for (const e of entries) {
    const bytes = Buffer.byteLength(e.text);
    if (current.length && size + bytes > MAX_EMAIL_BYTES) { parts.push(current); current = []; size = 0; }
    current.push(e);
    size += bytes;
  }
  parts.push(current);
  return parts;
}

// The date in the schedule's time zone, as YYYY-MM-DD (the en-CA format).
export function localDate(date) {
  return new Intl.DateTimeFormat('en-CA', {
    timeZone: config.digest.timezone, year: 'numeric', month: '2-digit', day: '2-digit',
  }).format(date);
}

function receivedAt(date) {
  return new Intl.DateTimeFormat('en-US', {
    timeZone: config.digest.timezone, year: 'numeric', month: 'short', day: 'numeric',
    hour: 'numeric', minute: '2-digit', timeZoneName: 'short',
  }).format(date);
}
