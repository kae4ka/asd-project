CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TYPE connection_type AS ENUM ('gRPC', 'Http', 'database');

CREATE TABLE ext_datamodule_connections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    connection_string TEXT,
    contract TEXT,
    connection_type connection_type NOT NULL
);
