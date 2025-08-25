import mysql.connector
from mysql.connector import Error
import random
from datetime import datetime, timedelta


config = {
    'user': 'root',
    'password': '****',  
    'host': 'localhost',
    'database': 'Project'
}

def connect_db():
    try:
        conn = mysql.connector.connect(**config)
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None

# Funktion för att lägga till user
def add_user(name, email):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
            conn.commit()
            print("User added.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

# Lägg till kategori
def add_category(user_id, name):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO categories (user_id, name) VALUES (%s, %s)", (user_id, name))
            conn.commit()
            print("Category added.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

# Lägg till transaktion 
def add_transaction(user_id, category_id, date, amount, tx_type, description):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            # Gör amount positiv för income, negativ för expense
            if tx_type.lower() == 'expense':
                amount = -abs(amount)
            else:
                amount = abs(amount)  # Säkerställ positiv för income
            cursor.execute("""
                INSERT INTO transactions (user_id, category_id, date, amount, description)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, category_id, date, amount, description))
            conn.commit()
            print("Transaction added.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

# Query 1: View Transactions (basic)
def view_transactions_basic(user_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT t.date, c.name AS category, t.amount, t.description
                FROM transactions t
                JOIN categories c ON t.category_id = c.category_id
                WHERE t.user_id = %s
            """, (user_id,))
            results = cursor.fetchall()
            for row in results:
                print(row)
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

# Query 2: View Transactions with User Name
def view_transactions_with_user(user_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT t.date, u.name AS user_name, c.name AS category, t.amount, t.description
                FROM transactions t
                JOIN users u ON t.user_id = u.user_id
                JOIN categories c ON t.category_id = c.category_id
                WHERE u.user_id = %s
            """, (user_id,))
            results = cursor.fetchall()
            for row in results:
                print(row)
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

# Query 3: Monthly Category Totals (with specific month)
def monthly_category_totals_specific(user_id, month):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT c.name AS category, SUM(t.amount) AS total
                FROM transactions t
                JOIN categories c ON t.category_id = c.category_id
                WHERE t.user_id = %s
                  AND YEAR(t.date) = YEAR(CURRENT_DATE())
                  AND MONTH(t.date) = %s
                GROUP BY c.name
            """, (user_id, month))
            results = cursor.fetchall()
            for row in results:
                print(row)
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

# Query 4: Yearly Income/Expense Summary per Month
def yearly_income_expense_summary(user_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT MONTH(date) AS month,
                       SUM(CASE WHEN amount >= 0 THEN amount ELSE 0 END) AS total_income,
                       SUM(CASE WHEN amount <  0 THEN -amount ELSE 0 END) AS total_expense
                FROM transactions
                WHERE user_id = %s
                  AND YEAR(date) = YEAR(CURRENT_DATE())
                GROUP BY MONTH(date)
            """, (user_id,))
            results = cursor.fetchall()
            for row in results:
                print(row)
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

def create_negative_transactions_view():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE OR REPLACE VIEW negative_transactions AS
                SELECT * FROM transactions
                WHERE amount < 0
            """)
            conn.commit()
            print("View 'negative_transactions' created or replaced.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

# Setup Function: Create monthly_balance function 
def create_monthly_balance_function():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DROP FUNCTION IF EXISTS monthly_balance")
           
            cursor.execute("""
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
                END
            """)
            conn.commit()
            print("Function 'monthly_balance' created or replaced.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

# Använd function för månadsbalans
def get_monthly_balance(user_id, month, year):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT monthly_balance(%s, %s, %s)", (user_id, month, year))
            result = cursor.fetchone()[0]
            print(f"Balance for {month}/{year}: {result}")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

# View Warnings
def view_warnings():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT * FROM warnings ORDER BY created_at DESC LIMIT 50
            """)
            results = cursor.fetchall()
            for row in results:
                print(row)
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

# Generera testdata (uppdaterad: hantera amount-sign random för income/expense)
def generate_test_data(user_id):
    categories = ['Mat', 'Hyra', 'Nöjen', 'Lön', 'Övrigt']
    for cat in categories:
        add_category(user_id, cat)
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT category_id FROM categories WHERE user_id = %s", (user_id,))
    cat_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    
    start_date = datetime.now() - timedelta(days=365)
    for _ in range(50):
        date = start_date + timedelta(days=random.randint(0, 365))
        amount = random.uniform(100, 5000)
        tx_type = random.choice(['income', 'expense'])
        category_id = random.choice(cat_ids)
        add_transaction(user_id, category_id, date.date(), amount, tx_type, "Test transaction")

# Huvudmeny 
def main():
    create_negative_transactions_view()
    create_monthly_balance_function()
    
    while True:
        print("\nBudget Tracker Menu:")
        print("1. Add User")
        print("2. Add Category")
        print("3. Add Transaction")
        print("4. View Transactions (Basic - Query 1)")
        print("5. View Transactions with User Name (Query 2)")
        print("6. View Monthly Category Totals (Specific Month - Query 3)")
        print("7. View Yearly Income/Expense Summary per Month (Query 4)")
        print("8. Get Monthly Balance (Using Function)")
        print("9. View Warnings (Latest 50)")
        print("10. Generate Test Data (for user_id=1)")
        print("0. Exit")
        choice = input("Choose: ")
        if choice == '1':
            name = input("Name: ")
            email = input("Email: ")
            add_user(name, email)
        elif choice == '2':
            user_id = int(input("User ID: "))
            name = input("Category Name: ")
            add_category(user_id, name)
        elif choice == '3':
            user_id = int(input("User ID: "))
            category_id = int(input("Category ID: "))
            date = input("Date (YYYY-MM-DD): ")
            amount = float(input("Amount: "))
            tx_type = input("Type (income/expense): ")
            desc = input("Description: ")
            add_transaction(user_id, category_id, date, amount, tx_type, desc)
        elif choice == '4':
            user_id = int(input("User ID: "))
            view_transactions_basic(user_id)
        elif choice == '5':
            user_id = int(input("User ID: "))
            view_transactions_with_user(user_id)
        elif choice == '6':
            user_id = int(input("User ID: "))
            month = int(input("Month (1-12): "))
            monthly_category_totals_specific(user_id, month)
        elif choice == '7':
            user_id = int(input("User ID: "))
            yearly_income_expense_summary(user_id)
        elif choice == '8':
            user_id = int(input("User ID: "))
            month = int(input("Month (1-12): "))
            year = int(input("Year: "))
            get_monthly_balance(user_id, month, year)
        elif choice == '9':
            view_warnings()
        elif choice == '10':
            generate_test_data(1)
        elif choice == '0':
            break

if __name__ == "__main__":
    main()