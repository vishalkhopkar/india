CREATE TABLE IF NOT EXISTS feedback (
  id         integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  -- 0 = report incorrect information, 1 = general feedback. The labels and the numbers
  -- accepted live in config.json, so a new category needs no migration.
  category   smallint      NOT NULL CHECK (category >= 0),
  email_id   varchar(254),
  message    varchar(1000) NOT NULL,
  sent       boolean       NOT NULL DEFAULT false,
  recv_date  timestamptz   NOT NULL DEFAULT now(),
  sent_date  date
);

-- The nightly digest reads only unsent rows.
CREATE INDEX IF NOT EXISTS feedback_unsent ON feedback (id) WHERE NOT sent;
