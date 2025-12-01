import sqlite3

conn = sqlite3.connect('data/telecom.db')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]
print('Tables:', tables)

# Check customers table schema
cursor.execute("PRAGMA table_info(customers);")
print('\nCustomers table schema:')
for row in cursor.fetchall():
    print(row)

# Check existing customers
cursor.execute("SELECT * FROM customers LIMIT 5;")
print('\nSample customers:')
for row in cursor.fetchall():
    print(row)

conn.close()
