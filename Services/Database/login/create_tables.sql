-- Creation of user table
CREATE TABLE IF NOT EXISTS login_user (
  id SERIAL PRIMARY KEY,
  username VARCHAR ( 50 ) UNIQUE NOT NULL,
  password VARCHAR ( 255 ) NOT NULL,
  email VARCHAR ( 255 ) UNIQUE NOT NULL
);


--SELECT pg_checkpoint();
