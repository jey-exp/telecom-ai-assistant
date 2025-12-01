# User Management Guide - Telecom AI Assistant

## Problem Fixed

The original error `"no such column: c.phone_number"` occurred because the database schema didn't match what the application code expected. This has been resolved by:

1. **Updated Database Schema**: Created tables with correct column names matching the application code
2. **Added User Management**: Implemented proper user authentication and role-based access
3. **Created Sample Data**: Added admin and customer accounts with proper relationships

## Database Schema Fixed

### Key Changes Made:
- ✅ `customers.phone` → `customers.phone_number`
- ✅ `customers.plan_id` → `customers.service_plan_id`
- ✅ Added `customers.account_status`
- ✅ Added `customers.last_billing_date`
- ✅ `service_plans.id` → `service_plans.plan_id`
- ✅ Added proper service plan columns (data_limit_gb, voice_minutes, etc.)
- ✅ Updated customer_usage table with billing periods and proper usage tracking

## Users Created

### Admin Account
- **Username**: `admin`
- **Email**: `admin@telecom.com`
- **Password**: `admin123`
- **Role**: `admin`

### Customer Accounts
1. **John Doe**
   - **Username**: `john_doe`
   - **Email**: `john.doe@email.com`
   - **Password**: `customer123`
   - **Customer ID**: `CUST001`
   - **Phone**: `+1-555-0101`
   - **Plan**: Standard Plan ($45.99/month)

2. **Jane Smith**
   - **Username**: `jane_smith`
   - **Email**: `jane.smith@email.com`
   - **Password**: `customer456`
   - **Customer ID**: `CUST002`
   - **Phone**: `+1-555-0102`
   - **Plan**: Premium Plan ($75.99/month)

## How to Add More Users

### Method 1: Using the User Management Module

```python
from utils.user_management import user_manager

# Add an admin user
admin_id = user_manager.add_admin_user(
    username="new_admin",
    email="newadmin@telecom.com",
    password="secure_password",
    name="New Administrator"
)

# Add a customer user
customer_id = user_manager.add_customer_user(
    username="new_customer",
    email="customer@email.com",
    password="customer_password",
    name="Customer Name",
    customer_id="CUST003",
    phone_number="+1-555-0103",
    address="123 New Street, City, State 12345",
    service_plan_id=2  # 1=Basic, 2=Standard, 3=Premium, 4=Family
)
```

### Method 2: Direct Database Insertion

```python
import sqlite3
from utils.user_management import user_manager

# Manual database insertion
conn = sqlite3.connect('data/telecom.db')
cursor = conn.cursor()

# Hash the password
password_hash = user_manager.hash_password("password123")

# Insert user
cursor.execute("""
    INSERT INTO users (username, email, password_hash, role) 
    VALUES (?, ?, ?, ?)
""", ("username", "email@domain.com", password_hash, "customer"))

user_id = cursor.lastrowid

# Insert customer profile (for customer role)
cursor.execute("""
    INSERT INTO customers (user_id, customer_id, name, email, phone_number, address, service_plan_id) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", (user_id, "CUST004", "Customer Name", "email@domain.com", "+1-555-0104", "Address", 1))

conn.commit()
conn.close()
```

## Service Plans Available

1. **Basic Plan** (ID: 1) - $25.99/month - 5GB Data
2. **Standard Plan** (ID: 2) - $45.99/month - 20GB Data  
3. **Premium Plan** (ID: 3) - $75.99/month - Unlimited Data
4. **Family Plan** (ID: 4) - $120.99/month - 100GB Shared

## Files Created/Modified

### New Files:
- `utils/user_management.py` - User management functions
- `complete_setup.py` - Complete database setup script
- `verify_fix.py` - Verification script

### Modified Files:
- `utils/database.py` - Updated with correct schema and table creation

## Testing the Fix

Run the verification script to confirm everything works:

```bash
python verify_fix.py
```

This will test the exact query that was failing before and confirm all user accounts are properly created.

## Next Steps

1. **Authentication Integration**: The user management system is ready to be integrated with your UI/authentication system
2. **Password Security**: Consider upgrading from SHA-256 to bcrypt for better password security
3. **User Roles**: Extend the role system if you need more granular permissions
4. **Customer Data**: Add more customer profiles and usage data as needed

## Troubleshooting

If you encounter schema issues in the future:
1. Run `python complete_setup.py` to reset the database
2. Check column names in SQL queries match the schema
3. Use `verify_fix.py` to test critical queries

The database now properly supports all the features expected by your Telecom AI Assistant application!
