-- shopping list tables
CREATE TABLE IF NOT EXISTS users(
  user_id SERIAL PRIMARY KEY,
  email VARCHAR(100),
  username VARCHAR(50),
  pword VARCHAR(64),
  date_registered TIMESTAMP DEFAULT current_timestamp
);


CREATE TABLE IF NOT EXISTS lists(
  list_id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(user_id),
  list_name VARCHAR(50),
  time_updated TIMESTAMP DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS items(
  item_id SERIAL PRIMARY KEY ,
  list_id INT REFERENCES lists(list_id),
  item_name VARCHAR(50),
  quantity FLOAT,
  units VARCHAR(5),
  item_cost FLOAT,
  time_updated TIMESTAMP DEFAULT current_timestamp

);

CREATE TABLE IF NOT EXISTS authentication(
  auth_id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(user_id),
  auth_token VARCHAR(100),
  login_time TIMESTAMP DEFAULT current_timestamp
);