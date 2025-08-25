USE Project;

CREATE TABLE IF NOT EXISTS warnings (
  warning_id INT AUTO_INCREMENT PRIMARY KEY,
  tx_id      INT,
  user_id    INT,
  message    VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER $$
CREATE TRIGGER check_negative_balance
AFTER INSERT ON transactions
FOR EACH ROW
BEGIN
  DECLARE current_balance DECIMAL(16,2);
  SELECT IFNULL(SUM(amount),0) INTO current_balance
    FROM transactions
    WHERE user_id = NEW.user_id;
  IF current_balance < 0 THEN
    INSERT INTO warnings(tx_id, user_id, message)
      VALUES (NEW.tx_id, NEW.user_id, CONCAT('Saldo negativt: ', current_balance));
  END IF;
END $$
DELIMITER ;

INSERT INTO users (user_id, name, email) VALUES
  (1, 'Ali', 'ali@example.com'),
  (2, 'Bob',       'bob@example.com');

INSERT INTO categories (category_id, user_id, name) VALUES
  -- Ali (user_id = 1)
  (1, 1, 'Hyra'),
  (2, 1, 'Mat'),
  (3, 1, 'Nöjen'),
  (4, 1, 'Lön'),
  (5, 1, 'Transport'),
  -- Bob (user_id = 2)
  (6, 2, 'Hyra'),
  (7, 2, 'Mat'),
  (8, 2, 'El & Uppvärmning'),
  (9, 2, 'Lön');

INSERT INTO transactions (tx_id, user_id, category_id, date, amount, description) VALUES
  -- inkomster och utgifter över flera månader
  (1, 1, 4, '2025-01-01', 30000.00, 'Lön januari'),
  (2, 1, 1, '2025-01-05', -12000.00, 'Hyra januari'),
  (3, 1, 2, '2025-01-07', -850.50, 'Mat - ICA'),
  (4, 1, 3, '2025-01-20', -250.00, 'Biokväll'),
  (5, 1, 5, '2025-01-22', -120.00, 'Tunnelbana'),
  (6, 1, 4, '2025-02-01', 30000.00, 'Lön februari'),
  (7, 1, 2, '2025-02-10', -970.00, 'Mat - Coop'),
  (8, 1, 3, '2025-02-14', -450.00, 'Konsert'),
  (9, 1, 1, '2025-02-28', -12000.00, 'Hyra februari'),
  (10, 1, 2, '2025-03-05', -760.25, 'Mat - Hemköp'),
  (11, 1, 4, '2025-03-01', 30000.00, 'Lön mars'),
  (12, 1, 3, '2025-03-15', -300.00, 'Netflix + fika'),
  (13, 1, 5, '2025-06-17', -400.00, 'Busskort'),
  (14, 1, 2, '2025-07-03', -950.00, 'Mat - storhandling'),
  (15, 1, 4, '2025-07-01', 30000.00, 'Lön juli'),

  -- mindre inkomster, en månad med negativt saldo
  (16, 2, 9, '2025-01-25', 15000.00, 'Lön januari'),
  (17, 2, 6, '2025-01-03', -7000.00, 'Hyra januari'),
  (18, 2, 7, '2025-01-10', -1400.00, 'Mat - Netto'),
  (19, 2, 8, '2025-01-20', -2000.00, 'El - Januari'),
  (20, 2, 9, '2025-02-25', 15000.00, 'Lön februari'),
  (21, 2, 7, '2025-02-04', -1600.00, 'Mat - ICA'),
  (22, 2, 6, '2025-02-10', -7000.00, 'Hyra februari'),
  -- En extra stor utgift som gör Bob negativ denna månad
  (23, 2, 7, '2025-02-15', -9000.00, 'Nödinköp / reparation (oroar saldo)'),
  (24, 2, 8, '2025-03-01', -1800.00, 'El - februari'),
  (25, 2, 9, '2025-03-27', 15000.00, 'Lön mars'),
  (26, 2, 7, '2025-03-05', -1200.00, 'Mat - Hemköp'),
  (27, 2, 6, '2025-03-01', -7000.00, 'Hyra mars');



SELECT t.date, c.name AS category, t.amount, t.description
FROM transactions t
JOIN categories c ON t.category_id = c.category_id
WHERE t.user_id = 1;

SELECT t.date, u.name AS user_name, c.name AS category, t.amount, t.description
FROM transactions t
JOIN users u       ON t.user_id = u.user_id
JOIN categories c  ON t.category_id = c.category_id
WHERE u.user_id = 1;


SELECT c.name AS category, SUM(t.amount) AS total
FROM transactions t
JOIN categories c ON t.category_id = c.category_id
WHERE t.user_id = 1 
  AND YEAR(t.date) = YEAR(CURRENT_DATE())
  AND MONTH(t.date) = 2
GROUP BY c.name;

SELECT MONTH(date) AS month,
       SUM(CASE WHEN amount >= 0 THEN amount ELSE 0 END) AS total_income,
       SUM(CASE WHEN amount <  0 THEN -amount ELSE 0 END) AS total_expense
FROM transactions
WHERE user_id = 1
  AND YEAR(date) = YEAR(CURRENT_DATE())
GROUP BY MONTH(date);

CREATE VIEW negative_transactions AS
SELECT * FROM transactions
WHERE amount < 0;

DELIMITER $$
CREATE FUNCTION monthly_balance(u_id INT, m INT, y INT) 
  RETURNS DECIMAL(10,2)
  DETERMINISTIC
BEGIN
  DECLARE bal DECIMAL(10,2);
  SELECT SUM(amount) INTO bal
    FROM transactions
    WHERE user_id = u_id
      AND MONTH(date) = m
      AND YEAR(date) = y;
  RETURN IFNULL(bal, 0);
END $$
DELIMITER ;


-- Testa monthly_balance-funktionen
SELECT monthly_balance(2, 2, 2025) AS bob_feb_balance;


INSERT INTO transactions (user_id, category_id, date, amount, description)
VALUES (2, 6, '2025-08-25', -25000.00, 'Force-negative test: -7000.00');

SELECT IFNULL(SUM(amount),0) INTO @bal
FROM transactions
WHERE user_id = 2;
SELECT @bal AS current_balance_for_carl;


SELECT * FROM warnings ORDER BY created_at DESC LIMIT 50;

