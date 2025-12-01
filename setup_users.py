"""
Setup Script - Initialize database and add sample users.
This script creates the database schema and adds an admin and 2 customer users.
"""

from utils.database import db
from utils.user_management import user_manager


def setup_service_plans():
    """Add sample service plans"""
    plans = [
        ("Basic Plan", "prepaid", 25.99, 5.0, 500, 100, 0, 0, 0, "Voice, SMS, 5GB Data"),
        ("Standard Plan", "postpaid", 45.99, 20.0, 1000, 500, 0, 0, 0, "Voice, SMS, 20GB Data, Hotspot"),
        ("Premium Plan", "postpaid", 75.99, None, None, None, 1, 1, 1, "Voice, SMS, Unlimited Data, Hotspot, International"),
        ("Family Plan", "postpaid", 120.99, 100.0, 2000, 1000, 0, 0, 0, "4 Lines, Voice, SMS, 100GB Shared Data")
    ]
    
    for plan in plans:
        db.execute(
            """INSERT OR IGNORE INTO service_plans 
               (name, plan_type, monthly_cost, data_limit_gb, voice_minutes, sms_count, 
                unlimited_data, unlimited_voice, unlimited_sms, features) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            plan
        )
    
    print("Service plans added successfully!")


def add_sample_network_issues():
    """Add sample network troubleshooting data"""
    issues = [
        ("No Signal", "No bars, no connectivity", "Check if phone is in airplane mode, restart device, check for network outages", "connectivity"),
        ("Slow Data", "Slow internet browsing, apps loading slowly", "Check data usage, restart device, toggle mobile data off/on", "performance"),
        ("Call Drops", "Calls dropping frequently", "Check signal strength, avoid interference sources, update device software", "voice")
    ]
    
    for issue in issues:
        db.execute(
            "INSERT OR IGNORE INTO common_network_issues (issue_type, symptoms, solution, category) VALUES (?, ?, ?, ?)",
            issue
        )
    
    print("Network troubleshooting data added successfully!")


def main():
    print("Setting up Telecom AI Assistant Database...")
    print("=" * 50)
    
    # Create database tables
    print("1. Creating database tables...")
    db.create_tables()
    
    # Setup service plans
    print("\n2. Adding service plans...")
    setup_service_plans()
    
    # Add network issues
    print("\n3. Adding network troubleshooting data...")
    add_sample_network_issues()
    
    # Add Admin User
    print("\n4. Adding Admin User...")
    admin_id = user_manager.add_admin_user(
        username="admin",
        email="admin@telecom.com", 
        password="admin123",
        name="System Administrator"
    )
    
    # Add Customer Users
    print("\n5. Adding Customer Users...")
    
    # Customer 1
    customer1_id = user_manager.add_customer_user(
        username="john_doe",
        email="john.doe@email.com",
        password="customer123",
        name="John Doe",
        customer_id="CUST001",
        phone_number="+1-555-0101",
        address="123 Main St, Anytown, ST 12345",
        service_plan_id=2  # Standard Plan
    )
    
    # Customer 2  
    customer2_id = user_manager.add_customer_user(
        username="jane_smith",
        email="jane.smith@email.com", 
        password="customer456",
        name="Jane Smith",
        customer_id="CUST002",
        phone_number="+1-555-0102",
        address="456 Oak Ave, Another City, ST 67890",
        service_plan_id=3  # Premium Plan
    )
    
    # Add sample usage data for customers
    print("\n6. Adding sample usage data...")
    if customer1_id:
        db.execute(
            """INSERT INTO customer_usage (customer_id, billing_period_start, billing_period_end, 
               data_used_gb, voice_minutes_used, sms_count_used, additional_charges, total_bill_amount, month, year) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            ("CUST001", "2025-11-01", "2025-11-30", 15.5, 120, 250, 0.0, 45.99, 11, 2025)
        )
    
    if customer2_id:
        db.execute(
            """INSERT INTO customer_usage (customer_id, billing_period_start, billing_period_end, 
               data_used_gb, voice_minutes_used, sms_count_used, additional_charges, total_bill_amount, month, year) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            ("CUST002", "2025-11-01", "2025-11-30", 35.2, 89, 180, 5.0, 80.99, 11, 2025)
        )
    
    print("\n" + "=" * 50)
    print("Database setup completed successfully!")
    print("\n📋 Users Created:")
    print("Admin:")
    print("  - Username: admin")
    print("  - Email: admin@telecom.com")
    print("  - Password: admin123")
    print("  - Role: admin")
    print("\nCustomers:")
    print("  - Username: john_doe")
    print("  - Email: john.doe@email.com") 
    print("  - Password: customer123")
    print("  - Customer ID: CUST001")
    print()
    print("  - Username: jane_smith")
    print("  - Email: jane.smith@email.com")
    print("  - Password: customer456")
    print("  - Customer ID: CUST002")
    
    # List all users to verify
    print("\n📊 All Users in System:")
    users = user_manager.list_users()
    for user in users:
        print(f"  - ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Role: {user[3]}")


if __name__ == "__main__":
    main()
