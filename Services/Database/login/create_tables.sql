-- Creation of user table
CREATE TABLE IF NOT EXISTS user_login (
  id SERIAL PRIMARY KEY,
  username VARCHAR ( 50 ) UNIQUE NOT NULL,
  password VARCHAR ( 255 ) NOT NULL,
  email VARCHAR ( 255 ) UNIQUE NOT NULL
);

-- Inserting a test user
INSERT INTO user_login (username, password, email) VALUES ('test', 'testpass', 'test@test');