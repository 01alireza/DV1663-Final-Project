CREATE database Project;
USE Project;

CREATE TABLE users (
  user_id    INT AUTO_INCREMENT PRIMARY KEY,
  name       VARCHAR(100) NOT NULL,
  email      VARCHAR(100) UNIQUE
);

CREATE TABLE categories (
  category_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id     INT NOT NULL,
  name        VARCHAR(50) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE CASCADE
);

CREATE TABLE transactions (
  tx_id        INT AUTO_INCREMENT PRIMARY KEY,
  user_id      INT NOT NULL,
  category_id  INT NOT NULL,
  date         DATE    NOT NULL,
  amount       DECIMAL(10,2) NOT NULL,
  description  VARCHAR(255),
  FOREIGN KEY (user_id)     REFERENCES users(user_id)
    ON DELETE CASCADE,
  FOREIGN KEY (category_id) REFERENCES categories(category_id)
    ON DELETE CASCADE
);


