create extension "uuid-ossp";
create schema college;

create table if not exists college.token
(
    username text primary key,
    token uuid default uuid_generate_v4()
);
create table if not exists college.ips
(
    id integer generated always as identity not null primary key,
    name text not null,
    local_ip text not null,
    public_ip text not null,
    created timestamp with time zone default current_timestamp
);
INSERT INTO college.token VALUES ('admin', 'a1b2c3d4-a1b2-c3d4-e5f6-a1b2c3a1b2c3');
