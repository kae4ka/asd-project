CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TYPE task_state AS ENUM ('Draft', 'Released', 'Completed');
CREATE TYPE task_run_state AS ENUM ('Running', 'Paused', 'Stopped');

CREATE TABLE etl_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    is_released BOOLEAN NOT NULL DEFAULT FALSE,
    state task_state NOT NULL DEFAULT 'Draft',
    extraction_script_id UUID,
    upload_script_id UUID,
    CONSTRAINT etl_tasks_state_check CHECK (state IN ('Draft', 'Released', 'Completed'))
);

CREATE TABLE etl_task_field_rules (
    etl_task_id UUID NOT NULL REFERENCES etl_tasks(id) ON DELETE CASCADE,
    field_rule_id UUID NOT NULL,
    PRIMARY KEY (etl_task_id, field_rule_id)
);

CREATE TABLE etl_task_anonym_rules (
    etl_task_id UUID NOT NULL REFERENCES etl_tasks(id) ON DELETE CASCADE,
    anonym_rule_id UUID NOT NULL,
    PRIMARY KEY (etl_task_id, anonym_rule_id)
);

CREATE TABLE etl_task_transformation_scripts (
    etl_task_id UUID NOT NULL REFERENCES etl_tasks(id) ON DELETE CASCADE,
    transformation_script_id UUID NOT NULL,
    PRIMARY KEY (etl_task_id, transformation_script_id)
);

CREATE TABLE task_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    etl_task_id UUID NOT NULL REFERENCES etl_tasks(id) ON DELETE CASCADE,
    extracted_data_count BIGINT NOT NULL DEFAULT 0,
    run_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    state task_run_state NOT NULL DEFAULT 'Running'
);

