"""
Customer Service Module
Handles database interactions for fetching customer profile and usage data.
"""

from utils.database import db

def get_user_role(email):
    """Get user role from users table"""
    user_query = "SELECT role FROM users WHERE email = ?"
    result = db.query_one(user_query, [email])
    return result[0] if result else None

def get_customer_profile(email):
    """
    Fetch customer profile and plan details by email with role-based access.
    - Admin users get admin dashboard data
    - Customer users get their own profile only
    """
    # 1. Check user role first
    user_role = get_user_role(email)
    
    if user_role == 'admin':
        return get_admin_dashboard()
    elif user_role == 'customer':
        return get_customer_data_by_email(email)
    else:
        return None, None  # Invalid user

def get_customer_data_by_email(email):
    """Get customer data for a customer user"""
    # Get customer ID from customers table (not fallback to CUST001)
    email_query = "SELECT customer_id FROM customers WHERE email = ?"
    result = db.query_one(email_query, [email])
    
    if not result:
        return None, None  # Customer not found
    
    customer_id = result[0]
    customer_id = result[0]
    
    # 2. Fetch Profile + Plan
    customer_query = """
    SELECT c.customer_id, c.name, c.email, c.phone_number, c.address, 
           c.account_status, c.registration_date, c.last_billing_date,
           p.name, p.monthly_cost, p.data_limit_gb, 
           p.voice_minutes, p.sms_count, p.unlimited_data, p.unlimited_voice, p.unlimited_sms
    FROM customers c
    LEFT JOIN service_plans p ON c.service_plan_id = p.plan_id
    WHERE c.customer_id = ?
    """
    customer_data = db.query_one(customer_query, [customer_id])
    
    return customer_id, customer_data

def get_admin_dashboard():
    """
    Return admin dashboard data with customer overview
    """
    # Get total customers count
    total_customers_result = db.query_one("SELECT COUNT(*) FROM customers")
    total_customers = total_customers_result[0] if total_customers_result else 0
    
    # Get recent customers
    recent_customers_query = """
    SELECT customer_id, name, email, account_status, registration_date
    FROM customers 
    ORDER BY registration_date DESC 
    LIMIT 10
    """
    recent_customers = db.query(recent_customers_query)
    
    # Get plan distribution
    plan_stats_query = """
    SELECT p.name, COUNT(c.customer_id) as customer_count
    FROM service_plans p
    LEFT JOIN customers c ON p.plan_id = c.service_plan_id
    GROUP BY p.plan_id, p.name
    """
    plan_stats = db.query(plan_stats_query)
    
    admin_data = {
        'type': 'admin_dashboard',
        'total_customers': total_customers,
        'recent_customers': recent_customers,
        'plan_statistics': plan_stats
    }
    
    return 'ADMIN', admin_data

def get_all_customers():
    """
    Admin function to get all customers
    """
    query = """
    SELECT c.customer_id, c.name, c.email, c.phone_number, 
           c.account_status, p.name as plan_name
    FROM customers c
    LEFT JOIN service_plans p ON c.service_plan_id = p.plan_id
    ORDER BY c.name
    """
    return db.query(query)

def get_customer_by_id(customer_id):
    """
    Admin function to get any customer by ID
    """
    customer_query = """
    SELECT c.customer_id, c.name, c.email, c.phone_number, c.address, 
           c.account_status, c.registration_date, c.last_billing_date,
           p.name as plan_name, p.monthly_cost, p.data_limit_gb, 
           p.voice_minutes, p.sms_count, p.unlimited_data, p.unlimited_voice, p.unlimited_sms
    FROM customers c
    LEFT JOIN service_plans p ON c.service_plan_id = p.plan_id
    WHERE c.customer_id = ?
    """
    customer_data = db.query_one(customer_query, [customer_id])
    
    if not customer_data:
        return None, None
    
    return customer_id, customer_data

def get_usage_history(customer_id):
    """
    Fetch last 6 months of usage history for a customer.
    """
    usage_query = """
    SELECT billing_period_start, billing_period_end, 
           data_used_gb, voice_minutes_used, sms_count_used,
           additional_charges, total_bill_amount
    FROM customer_usage
    WHERE customer_id = ?
    ORDER BY billing_period_end DESC LIMIT 6
    """
    return db.query(usage_query, [customer_id])
