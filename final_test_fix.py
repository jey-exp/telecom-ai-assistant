"""
Final Test: Role-Based Access Fix Verification
Tests that admin no longer sees John Doe's details
"""

import sys
import os
sys.path.insert(0, os.getcwd())

def test_the_fix():
    """Test that the main issue is resolved"""
    print("🔧 TESTING: Admin Login Fix")
    print("=" * 50)
    
    from services.customer_service import get_customer_profile, get_user_role
    
    # Test 1: Admin should NOT get customer data anymore
    print("1. Testing Admin Access:")
    admin_email = "admin@telecom.com"
    admin_role = get_user_role(admin_email)
    print(f"   Admin role: {admin_role}")
    
    customer_id, admin_data = get_customer_profile(admin_email)
    print(f"   Admin customer_id: {customer_id}")
    
    if customer_id == "CUST001":
        print("   ❌ STILL BROKEN: Admin gets John Doe's data!")
        print(f"   Admin sees: {admin_data[1] if admin_data else 'No data'}")
        return False
    elif customer_id == "ADMIN":
        print("   ✅ FIXED: Admin gets admin dashboard")
        print(f"   Dashboard type: {admin_data.get('type', 'Unknown') if admin_data else 'No data'}")
        return True
    else:
        print(f"   ⚠️  Unexpected result: {customer_id}")
        return False

def test_customer_still_works():
    """Test that customers still get their own data"""
    print("\n2. Testing Customer Access Still Works:")
    
    from services.customer_service import get_customer_profile
    
    # John should still get his own data
    john_email = "john.doe@email.com"
    customer_id, customer_data = get_customer_profile(john_email)
    
    if customer_id == "CUST001" and customer_data and customer_data[1] == "John Doe":
        print("   ✅ John still gets his own data")
    else:
        print("   ❌ John's access broken")
        return False
    
    # Jane should get her own data
    jane_email = "jane.smith@email.com"
    customer_id, customer_data = get_customer_profile(jane_email)
    
    if customer_id == "CUST002" and customer_data and customer_data[1] == "Jane Smith":
        print("   ✅ Jane gets her own data")
        return True
    else:
        print("   ❌ Jane's access broken")
        return False

def main():
    print("🧪 FINAL VERIFICATION: Role-Based Access Fix")
    print("Testing the core issue: 'Admin shows John Doe details'")
    print("=" * 60)
    
    if not os.path.exists('data/telecom.db'):
        print("❌ Database not found! Please run complete_setup.py first.")
        return
    
    try:
        # Test the main fix
        admin_fix_works = test_the_fix()
        customer_access_works = test_customer_still_works()
        
        print("\n" + "=" * 60)
        if admin_fix_works and customer_access_works:
            print("🎉 SUCCESS: The role-based access issue is FIXED!")
            print("\n📋 Summary of Changes:")
            print("✅ Removed hardcoded 'CUST001' fallback")
            print("✅ Added proper role-based data access")
            print("✅ Admin gets admin dashboard instead of customer data")
            print("✅ Customers still get their own data")
            print("✅ Network agent updated for role-based responses")
            print("✅ UI updated with proper authentication")
            
            print("\n🚀 Next Steps:")
            print("1. Start the app: streamlit run app.py")
            print("2. Login as admin: admin@telecom.com / admin123")
            print("3. Verify admin sees dashboard, not John Doe's details")
            
        else:
            print("❌ The fix is not complete. Some issues remain.")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
