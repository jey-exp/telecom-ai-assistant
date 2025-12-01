"""
User Management Module - Handles user creation, authentication, and role management.
Provides functions to add admin and customer users to the system.
"""

import hashlib
import sqlite3
from datetime import datetime
from utils.database import db


class UserManager:
    def __init__(self):
        self.db = db
        
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username, email, password, role='customer'):
        """Create a new user account"""
        try:
            password_hash = self.hash_password(password)
            
            user_id = self.db.execute(
                """INSERT INTO users (username, email, password_hash, role) 
                   VALUES (?, ?, ?, ?)""",
                (username, email, password_hash, role)
            )
            
            print(f"User '{username}' created successfully with role '{role}' (ID: {user_id})")
            return user_id
            
        except sqlite3.IntegrityError as e:
            print(f"Error creating user: {e}")
            return None
    
    def create_customer_profile(self, user_id, customer_id, name, email, phone_number=None, address=None, service_plan_id=None):
        """Create a customer profile linked to a user account"""
        try:
            self.db.execute(
                """INSERT INTO customers (user_id, customer_id, name, email, phone_number, address, service_plan_id) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (user_id, customer_id, name, email, phone_number, address, service_plan_id)
            )
            
            print(f"Customer profile created for '{name}' with ID '{customer_id}'")
            return True
            
        except sqlite3.IntegrityError as e:
            print(f"Error creating customer profile: {e}")
            return False
    
    def add_admin_user(self, username, email, password, name):
        """Add an admin user to the system"""
        user_id = self.create_user(username, email, password, 'admin')
        if user_id:
            print(f"Admin user '{username}' added successfully!")
            return user_id
        return None
    
    def add_customer_user(self, username, email, password, name, customer_id, phone_number=None, address=None, service_plan_id=1):
        """Add a customer user with profile"""
        user_id = self.create_user(username, email, password, 'customer')
        if user_id:
            success = self.create_customer_profile(
                user_id, customer_id, name, email, phone_number, address, service_plan_id
            )
            if success:
                print(f"Customer user '{username}' added successfully!")
                return user_id
        return None
    
    def list_users(self):
        """List all users in the system"""
        users = self.db.query("SELECT id, username, email, role, created_at, is_active FROM users")
        return users
    
    def get_user_by_username(self, username):
        """Get user by username"""
        user = self.db.query_one("SELECT * FROM users WHERE username = ?", (username,))
        return user
    
    def authenticate_user(self, email, password):
        """Authenticate user credentials by email"""
        password_hash = self.hash_password(password)
        user = self.db.query_one(
            "SELECT * FROM users WHERE email = ? AND password_hash = ? AND is_active = 1",
            (email, password_hash)
        )
        return user is not None


# Initialize user manager
user_manager = UserManager()
