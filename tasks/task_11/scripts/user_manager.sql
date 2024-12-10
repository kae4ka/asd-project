CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TYPE access_request_state AS ENUM ('Wait', 'Approved', 'Declined');
CREATE TYPE user_role AS ENUM ('EditTask', 'ManageData', 'CreateExtDatamodule', 'ProcessEtlTask');
CREATE TYPE ext_datamodule_access_type AS ENUM ('Read', 'Write', 'Owner');

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL
);

CREATE TABLE user_roles (
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role user_role NOT NULL,
    PRIMARY KEY (user_id, role)
);

CREATE TABLE ext_datamodule_access (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    owner_id UUID NOT NULL REFERENCES users(id),
    ext_datamodule_id UUID NOT NULL,
    type ext_datamodule_access_type NOT NULL
);

CREATE TABLE access_request (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    ext_datamodule_id UUID NOT NULL,
    state access_request_state NOT NULL DEFAULT 'Wait'
);
