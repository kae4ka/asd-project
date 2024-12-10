CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TYPE data_state AS ENUM ('Created', 'Modified', 'Sent');

CREATE TABLE data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    run_id UUID NOT NULL,
    content TEXT NOT NULL,
    saved_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    modified_at TIMESTAMPTZ,
    state data_state NOT NULL DEFAULT 'Created'
);