# 💰 Budget Tracker - MySQL Project

A personal budget tracking system built with MySQL, featuring transaction management, balance monitoring, and automated warnings for negative balances.

---

## 📋 Project Overview
This project implements a complete budget tracking database system with:

- 👤 User management  
- 🗂️ Category-based transaction organization  
- ⚠️ Automated balance monitoring with warning system  
- 📈 Monthly reporting and analysis functions  
- 🐍 Python interface for data management  

---

## 🗄️ Database Schema

### Tables
- **users**: Stores user information (`user_id`, `name`, `email`)  
- **categories**: User-specific transaction categories (`category_id`, `user_id`, `name`)  
- **transactions**: Financial transactions (`tx_id`, `user_id`, `category_id`, `date`, `amount`, `description`)  
- **warnings**: Automated alerts for negative balances (`warning_id`, `tx_id`, `user_id`, `message`, `created_at`)  

### Key Features
- ✅ Auto-increment primary keys for all main tables  
- 🔗 Foreign key constraints with cascade delete  
- ⚡ Triggers for real-time balance monitoring  
- 📊 Stored functions for financial calculations  
- 👓 Views for simplified data access  

---

## ⚙️ Setup Instructions

### 1. Database Initialization
```bash
# Run the tables creation script first
mysql -u root -p < tables_creation.sql

# Then populate with sample data and procedures
mysql -u root -p < SQL_queries.sql
```
### 2. Python Interface Setup
```bash
# Install required dependencies
pip install mysql-connector-python
```
###Configure database connection in testdata.py:
```python

config = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',
    'database': 'Project'
}
```
---
Run the Python interface:

bash
Copy
Edit
python testdata.py
🚀 Usage
SQL Query Examples
View user transactions

sql
Copy
Edit
SELECT t.date, c.name AS category, t.amount, t.description
FROM transactions t
JOIN categories c ON t.category_id = c.category_id
WHERE t.user_id = 1;
Monthly category totals

sql
Copy
Edit
SELECT c.name AS category, SUM(t.amount) AS total
FROM transactions t
JOIN categories c ON t.category_id = c.category_id
WHERE t.user_id = 1 
  AND YEAR(t.date) = YEAR(CURRENT_DATE())
  AND MONTH(t.date) = 2
GROUP BY c.name;
Yearly income/expense summary

sql
Copy
Edit
SELECT MONTH(date) AS month,
       SUM(CASE WHEN amount >= 0 THEN amount ELSE 0 END) AS total_income,
       SUM(CASE WHEN amount < 0 THEN -amount ELSE 0 END) AS total_expense
FROM transactions
WHERE user_id = 1
  AND YEAR(date) = YEAR(CURRENT_DATE())
GROUP BY MONTH(date);
Python Interface Features
➕ Add users and categories

💵 Record transactions (income/expense)

👀 View transactions and reports

🧪 Generate test data

⚠️ Check balance warnings

🔧 Advanced Features
Automated Warnings System
Trigger check_negative_balance:

Checks balance after each transaction

Inserts warning records for negative balances

Includes transaction details and calculated balance

Monthly Balance Function
sql
Copy
Edit
SELECT monthly_balance(2, 2, 2025) AS bob_feb_balance;
Negative Transactions View
sql
Copy
Edit
CREATE VIEW negative_transactions AS
SELECT * FROM transactions WHERE amount < 0;
📊 Sample Data
The database includes sample data for two users:

Ali: Regular income with consistent spending

Bob: Smaller income with occasional negative balances (triggering warnings)

🛠️ Technical Details
Database: MySQL

Character Set: UTF-8

Decimal Precision: 10,2 for monetary values

Timestamps: Automatic creation timestamps for warnings

Constraints: Foreign keys with ON DELETE CASCADE

📝 License
This project is for educational purposes. Feel free to modify and use for personal budget tracking.

🤝 Contributing
Fork the repository

Create a feature branch

Commit your changes

Push to the branch

Create a Pull Request

📧 Support
For questions or issues, please check the SQL scripts for implementation details or review the Python interface code for usage examples.



