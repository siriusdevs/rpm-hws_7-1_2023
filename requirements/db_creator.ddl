CREATE TABLE  IF NOT EXISTS titles (number int primary key, phrase text);

INSERT INTO titles (number, phrase) values (1, 'Do not rely on chance, but trust your intuition'), 
                    (2, 'Stick to your own path');


CREATE EXTENSION "uuid-ossp";

CREATE TABLE IF NOT EXISTS token  (username text primary key, password uuid);

INSERT INTO token (username, password) values ('admin', '077bc286-8564-4627-84c2-beb7b6af5521');