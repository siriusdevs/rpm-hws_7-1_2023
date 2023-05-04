CREATE TABLE IF NOT EXISTS users.data 
(
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    login text not null,
    pwd text not null
);

INSERT INTO users.data (login, pwd) VALUES (123, 123);