"""
Sidebar Component
Handles login/logout functionality and navigation menu with database authentication.
"""

import streamlit as st
from services.customer_service import get_user_role
from utils.user_management import user_manager

def render_sidebar():
    """Render the sidebar with login form or user info."""
    with st.sidebar:
        st.header("🔐 Login")
        
        if not st.session_state.logged_in:
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="admin@telecom.com or john.doe@email.com")
                password = st.text_input("Password", type="password", placeholder="Enter password")
                
                submitted = st.form_submit_button("Login", type="primary", use_container_width=True)
                
                if submitted:
                    if email and password:
                        # Authenticate user
                        if user_manager.authenticate_user(email, password):
                            user_role = get_user_role(email)
                            
                            if user_role:
                                st.session_state.logged_in = True
                                st.session_state.user_email = email
                                st.session_state.user_role = user_role
                                st.session_state.user_type = "Admin" if user_role == 'admin' else "Customer"
                                st.success(f"Welcome, {user_role}!")
                                st.rerun()
                            else:
                                st.error("User role not found")
                        else:
                            st.error("Invalid email or password")
                    else:
                        st.error("Please enter both email and password")
            
            # Show demo credentials
            with st.expander("Demo Credentials"):
                st.markdown("""
                **Admin:**
                - Email: admin@telecom.com
                - Password: admin123
                
                **Customers:**
                - Email: john.doe@email.com
                - Password: customer123
                - Email: jane.smith@email.com  
                - Password: customer456
                """)
                
        else:
            st.success(f"Logged in as **{st.session_state.user_type}**")
            st.write(f"📧 {st.session_state.user_email}")
            
            if hasattr(st.session_state, 'user_role'):
                if st.session_state.user_role == 'admin':
                    st.write("🛡️ Administrator Access")
                else:
                    st.write("👤 Customer Access")
            
            if st.button("Logout", use_container_width=True):
                # Clear all session state on logout
                st.session_state.logged_in = False
                st.session_state.user_email = ""
                st.session_state.user_role = ""
                st.session_state.user_type = ""
                st.session_state.messages = {}
                st.session_state.graph_initialized = False
                st.session_state.graph = None
                if "account_data" in st.session_state:
                    del st.session_state.account_data
                st.rerun()
        
        st.divider()
        
        if st.session_state.logged_in:
            if st.session_state.user_type == "Admin":
                st.header("🔧 Admin Tools")
                st.markdown("""
                - Customer Management
                - System Overview
                - Network Status
                - Plan Analytics
                """)
            else:
                st.header("📱 Services")
                st.markdown("""
                - My Account
                - Billing Support
                - Network Help
                - Plan Options
                - Knowledge Base
                """)

def authenticate_user(email, password):
    """Authenticate user credentials"""
    try:
        return user_manager.authenticate_user(email, password)
    except Exception as e:
        st.error(f"Authentication error: {e}")
        return False
