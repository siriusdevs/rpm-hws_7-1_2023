## This server needs:
### postgres database with tables:
 - token (username text primary key, token uuid)
 - ips (
    id integer generated always as identity not null primary key,
    name text not null,
    local_ip text not null,
    public_ip text not null,
    created timestamp with time zone default current_timestamp)
### .env file with credentials:
postgres info: PG_DBNAME, PG_HOST, PG_PORT, PG_USER, PG_PASSWORD, SMTP_MAIL_PASSWORD