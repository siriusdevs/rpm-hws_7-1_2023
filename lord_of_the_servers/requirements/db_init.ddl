CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS token (
    username text NOT NULL primary key,
    token uuid default uuid_generate_v4()
);

INSERT INTO token (username) VALUES ('admin');

CREATE TABLE IF NOT EXISTS book (
    id int primary key generated always as identity,
    title text NOT NULL,
    volume int NOT NULL,
    published int NOT NULL
);

INSERT INTO book (title, volume, published) VALUES
    ('The Hobbit', 320, 1937),
    ('The Fellowship of the Ring', 432, 1954),
    ('The Two Towers', 924, 1954),
    ('The Return of the King', 432, 1955),
    ('The Silmarillion', 384, 1977),
    ('Unfinished Tales of Numenor and Middle-earth', 480, 1980),
    ('The Children of Hurin', 320, 2007),
    ('Beren and Luthien', 288, 2017),
    ('The Fall of Gondolin', 304, 2018);

CREATE TABLE IF NOT EXISTS movie (
    id int primary key generated always as identity,
    title text NOT NULL,
    duration int NOT NULL,
    released int NOT NULL
);

INSERT INTO movie (title, duration, released) VALUES
    ('The Lord of the Rings: The Fellowship of the Ring', 178, 2001),
    ('The Lord of the Rings: The Two Towers', 179, 2002),
    ('The Lord of the Rings: The Return of the King', 201, 2003),
    ('The Hobbit: An Unexpected Journey', 182, 2012),
    ('The Hobbit: The Desolation of Smaug', 186, 2013),
    ('The Hobbit: The Battle of the Five Armies', 164, 2014);
