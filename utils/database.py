"""
Database Utility - SQLite connection manager with query methods.
Provides access to customers, service_plans, and customer_usage tables.
"""


import sqlite3
from config.config import config

class Database:
    def __init__(self, db_path=config.DB_PATH):
        self.db_path = db_path

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def query(self, sql, params=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, params or [])
            return cursor.fetchall()
        finally:
            conn.close()

    def query_one(self, sql, params=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, params or [])
            return cursor.fetchone()
        finally:
            conn.close()

    def execute(self, sql, params=None):
        """Execute INSERT, UPDATE, DELETE statements"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, params or [])
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def create_tables(self):
        """Create all necessary tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Create users table for authentication and role management
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'customer',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            """)

            # Create customers table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers (
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

            # Create service_plans table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS service_plans (
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

            # Create customer_usage table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS customer_usage (
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
                CREATE TABLE IF NOT EXISTS network_incidents (
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
                CREATE TABLE IF NOT EXISTS common_network_issues (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    issue_type TEXT NOT NULL,
                    symptoms TEXT NOT NULL,
                    solution TEXT NOT NULL,
                    category TEXT NOT NULL
                )
            """)

            conn.commit()
            print("Database tables created successfully!")
            
        except Exception as e:
            print(f"Error creating tables: {e}")
            conn.rollback()
        finally:
            conn.close()

db = Database()
