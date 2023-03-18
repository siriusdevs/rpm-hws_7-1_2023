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
INSERT INTO token VALUES ('admin', a1b2c3d4-a1b2-c3d4-e5f6-a1b2c3a1b2c3);
