create  extension if not exists  "uuid-ossp";
create table if not exists token (username text primary key, token uuid);
create table if not exists user_image(
    id integer primary key generated always as identity,
    title text not null,
    explanation text not null,
    date date NOT NULL DEFAULT CURRENT_DATE,
    url text,
    user_name text references token on delete cascade
);
