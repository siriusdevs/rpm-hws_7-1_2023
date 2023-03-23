CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS token (
    username text primary key,
    token uuid
);

INSERT INTO token (username, token) VALUES ('admin', 'a1b2c3d4-a1b2-c3d4-e5f6-a1b2c3a1b2c3');

CREATE TABLE IF NOT EXISTS book (
    id int primary key generated always as identity,
    title text NOT NULL,
    volume int NOT NULL,
    published int NOT NULL
);

CREATE TABLE IF NOT EXISTS movie (
    id int primary key generated always as identity,
    title text NOT NULL,
    duration int NOT NULL,
    released int NOT NULL
);
