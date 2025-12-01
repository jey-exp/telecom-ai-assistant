"""
Complete Database Setup Script for Telecom AI Assistant
This script fixes the schema mismatch and adds the requested users.
"""

import sqlite3
import hashlib
import os
from datetime import datetime

# Database path
DB_PATH = "data/telecom.db"

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_database():
    """Initialize database with correct schema"""
    
    # Remove existing database if it exists
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Removed existing database: {DB_PATH}")
    
    # Create new database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Create users table
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'customer',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        """)
        
        # Create customers table with correct column names
        cursor.execute("""
            CREATE TABLE customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                customer_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone_number TEXT,
                address TEXT,
                service_plan_id INTEGER,
                account_status TEXT DEFAULT 'active',
                registration_date DATE DEFAULT CURRENT_DATE,
                last_billing_date DATE,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (service_plan_id) REFERENCES service_plans (plan_id)
            )
        """)
        
        # Create service_plans table with correct schema
        cursor.execute("""
            CREATE TABLE service_plans (
                plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                plan_type TEXT NOT NULL,
                monthly_cost REAL NOT NULL,
                data_limit_gb REAL,
                voice_minutes INTEGER,
                sms_count INTEGER,
                unlimited_data BOOLEAN DEFAULT 0,
                unlimited_voice BOOLEAN DEFAULT 0,
                unlimited_sms BOOLEAN DEFAULT 0,
                features TEXT
            )
        """)
        
        # Create customer_usage table with correct schema
        cursor.execute("""
            CREATE TABLE customer_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT NOT NULL,
                billing_period_start DATE NOT NULL,
                billing_period_end DATE NOT NULL,
                data_used_gb REAL DEFAULT 0,
                voice_minutes_used INTEGER DEFAULT 0,
                sms_count_used INTEGER DEFAULT 0,
                additional_charges REAL DEFAULT 0,
                total_bill_amount REAL DEFAULT 0,
                month INTEGER,
                year INTEGER,
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
            )
        """)
        
        # Create network_incidents table
        cursor.execute("""
            CREATE TABLE network_incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                incident_id TEXT UNIQUE NOT NULL,
                area TEXT NOT NULL,
                issue_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                status TEXT DEFAULT 'open',
                reported_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resolved_date TIMESTAMP
            )
        """)
        
        # Create common_network_issues table
        cursor.execute("""
            CREATE TABLE common_network_issues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                issue_type TEXT NOT NULL,
                symptoms TEXT NOT NULL,
                solution TEXT NOT NULL,
                category TEXT NOT NULL
            )
        """)
        
        conn.commit()
        print("✅ Database schema created successfully!")
        
        return conn
        
    except Exception as e:
        print(f"❌ Error creating schema: {e}")
        conn.rollback()
        return None

def add_service_plans(conn):
    """Add service plans"""
    cursor = conn.cursor()
    
    plans = [
        ("Basic Plan", "prepaid", 25.99, 5.0, 500, 100, 0, 0, 0, "Voice, SMS, 5GB Data"),
        ("Standard Plan", "postpaid", 45.99, 20.0, 1000, 500, 0, 0, 0, "Voice, SMS, 20GB Data, Hotspot"),
        ("Premium Plan", "postpaid", 75.99, None, None, None, 1, 1, 1, "Unlimited Voice, SMS, Data, Hotspot, International"),
        ("Family Plan", "postpaid", 120.99, 100.0, 2000, 1000, 0, 0, 0, "4 Lines, Voice, SMS, 100GB Shared Data")
    ]
    
    for plan in plans:
        cursor.execute("""
            INSERT INTO service_plans 
            (name, plan_type, monthly_cost, data_limit_gb, voice_minutes, sms_count, 
             unlimited_data, unlimited_voice, unlimited_sms, features) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, plan)
    
    conn.commit()
    print("✅ Service plans added successfully!")

def add_network_issues(conn):
    """Add sample network troubleshooting data"""
    cursor = conn.cursor()
    
    issues = [
        ("No Signal", "No bars, no connectivity", "Check if phone is in airplane mode, restart device, check for network outages", "connectivity"),
        ("Slow Data", "Slow internet browsing, apps loading slowly", "Check data usage, restart device, toggle mobile data off/on", "performance"),
        ("Call Drops", "Calls dropping frequently", "Check signal strength, avoid interference sources, update device software", "voice")
    ]
    
    for issue in issues:
        cursor.execute("""
            INSERT INTO common_network_issues (issue_type, symptoms, solution, category) 
            VALUES (?, ?, ?, ?)
        """, issue)
    
    conn.commit()
    print("✅ Network troubleshooting data added successfully!")

def add_users(conn):
    """Add admin and customer users"""
    cursor = conn.cursor()
    
    # Add admin user
    admin_password_hash = hash_password("admin123")
    cursor.execute("""
        INSERT INTO users (username, email, password_hash, role) 
        VALUES (?, ?, ?, ?)
    """, ("admin", "admin@telecom.com", admin_password_hash, "admin"))
    
    admin_id = cursor.lastrowid
    print(f"✅ Admin user created (ID: {admin_id})")
    
    # Add customer 1
    customer1_password_hash = hash_password("customer123")
    cursor.execute("""
        INSERT INTO users (username, email, password_hash, role) 
        VALUES (?, ?, ?, ?)
    """, ("john_doe", "john.doe@email.com", customer1_password_hash, "customer"))
    
    customer1_user_id = cursor.lastrowid
    
    # Add customer 1 profile
    cursor.execute("""
        INSERT INTO customers (user_id, customer_id, name, email, phone_number, address, service_plan_id, last_billing_date) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (customer1_user_id, "CUST001", "John Doe", "john.doe@email.com", "+1-555-0101", 
          "123 Main St, Anytown, ST 12345", 2, "2025-11-01"))
    
    print(f"✅ Customer user 'john_doe' created (ID: {customer1_user_id})")
    
    # Add customer 2
    customer2_password_hash = hash_password("customer456")
    cursor.execute("""
        INSERT INTO users (username, email, password_hash, role) 
        VALUES (?, ?, ?, ?)
    """, ("jane_smith", "jane.smith@email.com", customer2_password_hash, "customer"))
    
    customer2_user_id = cursor.lastrowid
    
    # Add customer 2 profile
    cursor.execute("""
        INSERT INTO customers (user_id, customer_id, name, email, phone_number, address, service_plan_id, last_billing_date) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (customer2_user_id, "CUST002", "Jane Smith", "jane.smith@email.com", "+1-555-0102", 
          "456 Oak Ave, Another City, ST 67890", 3, "2025-11-01"))
    
    print(f"✅ Customer user 'jane_smith' created (ID: {customer2_user_id})")
    
    conn.commit()

def add_usage_data(conn):
    """Add sample usage data"""
    cursor = conn.cursor()
    
    # Usage data for customer 1
    cursor.execute("""
        INSERT INTO customer_usage 
        (customer_id, billing_period_start, billing_period_end, data_used_gb, 
         voice_minutes_used, sms_count_used, additional_charges, total_bill_amount, month, year) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ("CUST001", "2025-11-01", "2025-11-30", 15.5, 120, 250, 0.0, 45.99, 11, 2025))
    
    # Usage data for customer 2
    cursor.execute("""
        INSERT INTO customer_usage 
        (customer_id, billing_period_start, billing_period_end, data_used_gb, 
         voice_minutes_used, sms_count_used, additional_charges, total_bill_amount, month, year) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ("CUST002", "2025-11-01", "2025-11-30", 35.2, 89, 180, 5.0, 80.99, 11, 2025))
    
    conn.commit()
    print("✅ Usage data added successfully!")

def verify_setup(conn):
    """Verify the setup by querying the data"""
    cursor = conn.cursor()
    
    print("\n📊 Verification Results:")
    print("=" * 50)
    
    # Check users
    cursor.execute("SELECT id, username, email, role FROM users")
    users = cursor.fetchall()
    print(f"Users created: {len(users)}")
    for user in users:
        print(f"  - {user[1]} ({user[3]}) - {user[2]}")
    
    # Check customers
    cursor.execute("SELECT customer_id, name, email, phone_number FROM customers")
    customers = cursor.fetchall()
    print(f"\nCustomer profiles: {len(customers)}")
    for customer in customers:
        print(f"  - {customer[0]}: {customer[1]} - {customer[2]} - {customer[3]}")
    
    # Check service plans
    cursor.execute("SELECT plan_id, name, monthly_cost FROM service_plans")
    plans = cursor.fetchall()
    print(f"\nService plans: {len(plans)}")
    for plan in plans:
        print(f"  - {plan[0]}: {plan[1]} (${plan[2]})")
    
    # Test the problematic query
    print("\n🧪 Testing customer profile query:")
    cursor.execute("""
        SELECT c.customer_id, c.name, c.email, c.phone_number, c.address, 
               c.account_status, c.registration_date, c.last_billing_date,
               p.name, p.monthly_cost
        FROM customers c
        LEFT JOIN service_plans p ON c.service_plan_id = p.plan_id
        WHERE c.customer_id = 'CUST001'
    """)
    
    result = cursor.fetchone()
    if result:
        print("✅ Query executed successfully!")
        print(f"   Customer: {result[1]} ({result[0]})")
        print(f"   Phone: {result[3]}")
        print(f"   Plan: {result[8]} - ${result[9]}")
    else:
        print("❌ Query failed or no results")

def main():
    print("🚀 Setting up Telecom AI Assistant Database")
    print("=" * 50)
    
    # Initialize database
    conn = init_database()
    if not conn:
        print("❌ Failed to initialize database")
        return
    
    try:
        # Add data
        add_service_plans(conn)
        add_network_issues(conn)
        add_users(conn)
        add_usage_data(conn)
        
        # Verify setup
        verify_setup(conn)
        
        print("\n" + "=" * 50)
        print("🎉 Database setup completed successfully!")
        print("\n📝 Login Credentials:")
        print("Admin:")
        print("  Username: admin")
        print("  Password: admin123")
        print("  Email: admin@telecom.com")
        print("\nCustomers:")
        print("  Username: john_doe | Password: customer123")
        print("  Username: jane_smith | Password: customer456")
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == "__main__":
    main()
