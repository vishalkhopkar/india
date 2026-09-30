# Feedback service

Two Lambdas behind the site's feedback form, packaged together:

- **`submit.handler`** is called by the page through a Function URL. It validates the submission, writes it to CloudWatch, inserts it into the `feedback` table and answers with one of these:
  - `200 {"ok":true}`
  - `400` or `413` for bad input
  - `405` for a method other than POST
  - `500` when the database fails, which makes the page show its error toast
- **`digest.handler`** runs daily at 8 pm Central. It emails every unsent row as a single SNS message from `no-reply@sns.amazonaws.com`. After each message is published, it sets `sent = true` and `sent_date` (the Central-time date) on exactly the rows in that message. With nothing unsent, no email is sent.

## Build and test

```sh
npm install
npm test          # unit tests; the database tests are skipped
npm run package   # writes dist/feedback-service.zip, used by both Lambdas
```

Database tests: point the `PG*` variables at a **disposable** UTF8 database and run `FEEDBACK_TEST_DB=1 PGSSLMODE=disable npm test`. They drop and recreate the table.

## AWS settings the code expects

**RDS PostgreSQL**
- Private, with UTF8 encoding (the RDS default).
- Run `schema.sql` once.

**Submit Lambda**
- Runtime Node.js 22 or later, handler `submit.handler`, code from `dist/feedback-service.zip`, timeout 10 s.
- Placed in the RDS VPC's private subnets.
- Environment variables: `PGHOST`, `PGPORT` (5432), `PGDATABASE`, `PGUSER`, `PGPASSWORD`.
- Reserved concurrency 2, which acts as the MVP rate limit. Extra requests get a 429 and the page shows its error toast.
- Function URL:
  - auth type `NONE`
  - CORS allowed origin `https://vishalkhopkar.github.io`
  - allowed method `POST`
  - allowed header `content-type`
  - The handler sets no CORS headers of its own.

**Digest Lambda**
- Same zip, VPC and `PG*` variables as the submit Lambda.
- Handler `digest.handler`, timeout 60 s.
- Environment variable `TOPIC_ARN`.
- IAM permission `sns:Publish` on that topic.
- Needs an SNS interface VPC endpoint (`com.amazonaws.<region>.sns`, private DNS on). A Lambda inside a VPC cannot reach SNS otherwise. The submit Lambda needs no AWS APIs.

**SNS**
- A standard topic with your address subscribed over the email protocol. Confirm the subscription from your inbox.

**Schedule**
- EventBridge Scheduler: `cron(0 20 * * ? *)`, time zone `America/Chicago`, target the digest Lambda.
- Scheduler handles daylight saving.
- `config.json` → `digest` records the same time and zone, and the code uses the zone for `sent_date`. If you change one, change the other.

**Security groups**
- The Lambdas' security group may reach the RDS security group on port 5432.
- The SNS endpoint's security group allows 443 from the Lambdas.

**Logs**
- Set retention on both log groups, for example 90 days. The submit log holds messages, email addresses and IPs.

Finally, put the Function URL in the site's `config.js` → `feedbackEndpoint`.

## Categories

The page sends `category` as a number. `config.json` → `categories` lists the numbers the service accepts and their labels in the digest. To add a category:
1. Add an entry to `config.json` and redeploy the zip.
2. Add the matching `<option>` in `_build/template.html`.
