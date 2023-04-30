CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  username VARCHAR(20) UNIQUE NOT NULL,
  password VARCHAR(60) NOT NULL
);


CREATE TABLE posts (
  id INTEGER PRIMARY KEY,
  title VARCHAR(100) NOT NULL,
  content TEXT NOT NULL,
  published_date DATE NOT NULL,
  author_id INTEGER NOT NULL,
  FOREIGN KEY (author_id) REFERENCES users(id)
);

INSERT INTO users (username, password) VALUES ('alice', 'password1');
INSERT INTO users (username, password) VALUES ('bob', 'password2');