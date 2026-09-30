# Feedback service

Lambdas behind the site's feedback form, packaged together:

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
npm run package   # writes dist/feedback-service.zip, used by all three Lambdas
```

Database tests: point the `PG*` variables at a **disposable** UTF8 database and run `FEEDBACK_TEST_DB=1 PGSSLMODE=disable npm test`. They drop and recreate the table.

## Deployment

Everything on AWS is created by Terraform in [`../infra`](../infra/README.md), run by the
*Feedback service* GitHub Actions workflow on every push to `main` that touches this folder.
`migrate.handler` (a third Lambda) applies `schema.sql` during each deploy, so keep that file
idempotent (`IF NOT EXISTS`). The digest's schedule is read from `config.json`.

## Categories

The page sends `category` as a number. `config.json` → `categories` lists the numbers the service accepts and their labels in the digest. To add a category:
1. Add an entry to `config.json` and push (the workflow redeploys).
2. Add the matching `<option>` in `_build/template.html`.
