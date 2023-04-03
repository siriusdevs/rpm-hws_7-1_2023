create extension if not exists "uuid-ossp";
create table if not exists chat_user(
    id uuid primary key not null default uuid_generate_v4(),
    username text,
    email text,
    password text,
    frame_color text
);
insert into chat_user (username, email, password, frame_color) values ('admin',  'admin@admin.com', 'admin', '#B6DCEE');
create table if not exists message(
    user_id uuid references chat_user (id),
    filling text
);
insert into message (user_id, filling) values ((select id from chat_user limit 1), 'user');
