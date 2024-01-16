-- Creation of user table
CREATE TABLE IF NOT EXISTS login_user (
  id SERIAL PRIMARY KEY,
  username VARCHAR ( 50 ) UNIQUE NOT NULL,
  password VARCHAR ( 255 ) NOT NULL,
  email VARCHAR ( 255 ) UNIQUE NOT NULL
);

-- Inserting a test user
INSERT INTO login_user (username, password, email) VALUES ('test', 'testpass', 'test@test');