create schema college;

create extension "uuid-ossp";

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

insert into college.ips (name, local_ip, public_ip) values ('Work', '127.0.0.2', '86.101.44.128');

insert into college.token (username, token)
values ('admin', '77f498fc-ab20-4017-aa62-c8b246615bae');
