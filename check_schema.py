import sqlite3

# Connect to database
conn = sqlite3.connect('data/telecom.db')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables in database:")
for table in tables:
    print(f"- {table[0]}")

print("\n" + "="*50)

# Check customers table structure
cursor.execute("PRAGMA table_info(customers)")
customers_schema = cursor.fetchall()
print("\nCustomers table structure:")
for column in customers_schema:
    print(f"- {column[1]} ({column[2]})")

# Check if there are existing customers
cursor.execute("SELECT COUNT(*) FROM customers")
count = cursor.fetchone()[0]
print(f"\nExisting customers count: {count}")

if count > 0:
    cursor.execute("SELECT * FROM customers LIMIT 3")
    customers = cursor.fetchall()
    print("\nSample customers:")
    for customer in customers:
        print(customer)

conn.close()
