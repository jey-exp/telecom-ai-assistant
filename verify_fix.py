"""
Quick Database Verification Script
Tests if the schema fixes resolved the phone_number column issue
"""

import sqlite3

def test_customer_query():
    """Test the exact query that was failing before"""
    try:
        conn = sqlite3.connect('data/telecom.db')
        cursor = conn.cursor()
        
        # This is the query from customer_service.py that was failing
        customer_query = """
        SELECT c.customer_id, c.name, c.email, c.phone_number, c.address, 
               c.account_status, c.registration_date, c.last_billing_date,
               p.name, p.monthly_cost, p.data_limit_gb, 
               p.voice_minutes, p.sms_count, p.unlimited_data, p.unlimited_voice, p.unlimited_sms
        FROM customers c
        LEFT JOIN service_plans p ON c.service_plan_id = p.plan_id
        WHERE c.customer_id = ?
        """
        
        # Test with customer CUST001
        cursor.execute(customer_query, ["CUST001"])
        customer_data = cursor.fetchone()
        
        if customer_data:
            print("✅ SUCCESS: Customer query executed without errors!")
            print(f"   Customer: {customer_data[1]} ({customer_data[0]})")
            print(f"   Email: {customer_data[2]}")
            print(f"   Phone: {customer_data[3]}")
            print(f"   Address: {customer_data[4]}")
            print(f"   Status: {customer_data[5]}")
            print(f"   Plan: {customer_data[8]} (${customer_data[9]})")
            return True
        else:
            print("❌ No customer data found")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False
    finally:
        if conn:
            conn.close()

def show_user_accounts():
    """Show all created user accounts"""
    try:
        conn = sqlite3.connect('data/telecom.db')
        cursor = conn.cursor()
        
        print("\n📋 User Accounts Created:")
        print("-" * 40)
        
        # Get all users with their customer info if available
        cursor.execute("""
            SELECT u.username, u.email, u.role, c.customer_id, c.name
            FROM users u
            LEFT JOIN customers c ON u.id = c.user_id
            ORDER BY u.role DESC, u.username
        """)
        
        users = cursor.fetchall()
        for user in users:
            if user[2] == 'admin':
                print(f"👤 ADMIN: {user[0]} ({user[1]})")
            else:
                print(f"👥 CUSTOMER: {user[0]} ({user[1]}) - {user[4]} [{user[3]}]")
                
        return True
        
    except Exception as e:
        print(f"❌ ERROR getting user accounts: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🔍 Database Verification Test")
    print("=" * 40)
    
    # Test if the database exists
    import os
    if not os.path.exists('data/telecom.db'):
        print("❌ Database file not found! Run complete_setup.py first.")
        exit(1)
    
    # Test the problematic query
    if test_customer_query():
        print("\n🎉 The phone_number column issue has been FIXED!")
    else:
        print("\n❌ There are still issues with the database schema.")
    
    # Show created accounts
    show_user_accounts()
    
    print("\n✨ Verification completed!")
