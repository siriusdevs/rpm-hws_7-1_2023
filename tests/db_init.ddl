CREATE TABLE IF NOT EXISTS token (username text primary key, token uuid);

CREATE TABLE students (id integer generated always as identity not null primary key, 
    fname text not null, 
    lname text not null, 
    sname text, 
    group_ text not null, 
    age int);

INSERT INTO token VALUES ('admin', 'a1b2c3d4-a1b2-c3d4-e5f6-a1b2c3a1b2c3');
