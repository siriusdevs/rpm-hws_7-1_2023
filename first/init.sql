create table people(id int primary key generated always as identity, fname text, lname text, email text);
CREATE TABLE IF NOT EXISTS people(
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    fname TEXT,
    lname TEXT,
    email TEXT
);
CREATE EXTENSION "uuid-ossp";
CREATE TABLE token (
    username TEXT PRIMARY KEY,
    token uuid
);
INSERT INTO token VALUES ('admin', uuid_generate_v4());
