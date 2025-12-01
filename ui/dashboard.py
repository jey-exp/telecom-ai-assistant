"""
Dashboard Component  
Renders role-based dashboard - Admin overview or Customer account details.
"""

import streamlit as st
import pandas as pd
from services.customer_service import get_customer_profile, get_usage_history, get_all_customers

def render_dashboard():
    """Render role-based dashboard."""
    
    user_role = st.session_state.get('user_role', 'customer')
    
    if user_role == 'admin':
        render_admin_dashboard()
    else:
        render_customer_dashboard()

def render_admin_dashboard():
    """Render admin dashboard with system overview"""
    st.markdown("### 🔧 Admin Dashboard")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Refresh System Overview", type="secondary", use_container_width=True):
            try:
                customer_id, admin_data = get_customer_profile(st.session_state.user_email)
                st.session_state.account_data = {"admin": admin_data}
                st.success("Admin data loaded!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    if "account_data" in st.session_state and st.session_state.account_data:
        admin_data = st.session_state.account_data.get("admin")
        
        if admin_data and admin_data.get('type') == 'admin_dashboard':
            st.divider()
            
            # System Overview Metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📊 Total Customers", admin_data['total_customers'])
            
            with col2:
                st.metric("📋 Active Plans", len(admin_data['plan_statistics']))
            
            with col3:
                recent_customers = admin_data.get('recent_customers', [])
                st.metric("👥 Recent Signups", len(recent_customers))
            
            # Recent Customers
            st.markdown("#### 👥 Recent Customer Registrations")
            if recent_customers:
                recent_df = pd.DataFrame(recent_customers, 
                    columns=['Customer ID', 'Name', 'Email', 'Status', 'Registration Date'])
                st.dataframe(recent_df, use_container_width=True)
            else:
                st.info("No recent customer registrations")
            
            # Plan Statistics
            st.markdown("#### 📊 Plan Distribution")
            plan_stats = admin_data.get('plan_statistics', [])
            if plan_stats:
                plan_df = pd.DataFrame(plan_stats, columns=['Plan Name', 'Customer Count'])
                st.dataframe(plan_df, use_container_width=True)
                
                # Chart
                st.bar_chart(plan_df.set_index('Plan Name'))
            else:
                st.info("No plan statistics available")
            
            # Customer Management
            st.markdown("#### 🔧 Customer Management")
            all_customers = get_all_customers()
            
            if all_customers:
                customer_df = pd.DataFrame(all_customers, 
                    columns=['Customer ID', 'Name', 'Email', 'Phone', 'Status', 'Plan'])
                
                # Filter options
                col1, col2 = st.columns(2)
                with col1:
                    status_filter = st.selectbox("Filter by Status", 
                        ["All", "active", "suspended", "cancelled"])
                
                with col2:
                    search_term = st.text_input("Search by Name/Email")
                
                # Apply filters
                filtered_df = customer_df.copy()
                if status_filter != "All":
                    filtered_df = filtered_df[filtered_df['Status'] == status_filter]
                if search_term:
                    filtered_df = filtered_df[
                        filtered_df['Name'].str.contains(search_term, case=False) |
                        filtered_df['Email'].str.contains(search_term, case=False)
                    ]
                
                st.dataframe(filtered_df, use_container_width=True)
            else:
                st.info("No customer data available")
    else:
        st.info("Click 'Refresh System Overview' to load admin dashboard")

def render_customer_dashboard():
    """Render customer account dashboard."""
    st.markdown("### 👤 My Account Dashboard")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Refresh Account Details", type="secondary", use_container_width=True):
            try:
                # Fetch data using service layer
                customer_id, customer_data = get_customer_profile(st.session_state.user_email)
                
                if customer_id and customer_data:
                    usage_data = get_usage_history(customer_id)
                    st.session_state.account_data = {"customer": customer_data, "usage": usage_data}
                    st.success("Account details loaded!")
                    st.rerun()
                else:
                    st.error("Customer profile not found!")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    if "account_data" in st.session_state and st.session_state.account_data:
        cd = st.session_state.account_data.get("customer")
        ud = st.session_state.account_data.get("usage", [])
        
        if cd:
            st.divider()
            
            # Color-coded account status badge
            status = cd[5]
            if status == "Active":
                st.success(f"Account Status: **{status}**")
            elif status == "Suspended":
                st.error(f"Account Status: **{status}**")
            else:
                st.warning(f"Account Status: **{status}**")
            
            col1, col2 = st.columns(2)
            with col1:
                with st.container(border=True):
                    st.markdown("#### Personal Information")
                    st.write(f"**Name:** {cd[1]}")
                    st.write(f"**Email:** {cd[2]}")
                    st.write(f"**Phone:** {cd[3]}")
                    st.write(f"**Address:** {cd[4]}")
            
            with col2:
                with st.container(border=True):
                    st.markdown("#### Current Plan")
                    st.write(f"**Plan:** {cd[8]}")
                    st.write(f"**Cost:** \\${cd[9]}/month")
                    st.write(f"**Data:** {'Unlimited' if cd[13] else f'{cd[10]} GB'}")
                    st.write(f"**Voice:** {'Unlimited' if cd[14] else f'{cd[11]} min'}")
                    st.write(f"**SMS:** {'Unlimited' if cd[15] else f'{cd[12]}'}")
            
            st.divider()
            
            # Usage metrics with delta indicators
            if ud:
                st.markdown("### Recent Usage & Billing")
                latest = ud[0]
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Data Usage", 
                        f"{latest[2]:.1f} GB",
                        delta=f"{latest[2] - (cd[10] or 0):.1f} GB" if not cd[13] else "Unlimited",
                        delta_color="inverse"
                    )
                
                with col2:
                    st.metric(
                        "Voice Usage", 
                        f"{latest[3]} min",
                        delta=f"{latest[3] - (cd[11] or 0)} min" if not cd[14] else "Unlimited",
                        delta_color="inverse"
                    )
                
                with col3:
                    st.metric(
                        "SMS Usage", 
                        f"{latest[4]}",
                        delta=f"{latest[4] - (cd[12] or 0)}" if not cd[15] else "Unlimited",
                        delta_color="inverse"
                    )
                
                with col4:
                    st.metric(
                        "Latest Bill", 
                        f"\\${latest[6]:.2f}",
                        delta=f"\\${latest[5]:.2f} extra" if latest[5] > 0 else "No extras",
                        delta_color="inverse"
                    )
                
                st.write("")
                
                # Billing History Table
                with st.container(border=True):
                    st.markdown("#### Billing History")
                    df = pd.DataFrame(ud, columns=[
                        "Period Start", "Period End", "Data (GB)", 
                        "Voice (min)", "SMS", "Extra Charges", "Total Bill"
                    ])
                    df["Extra Charges"] = df["Extra Charges"].apply(lambda x: f"\\${x:.2f}")
                    df["Total Bill"] = df["Total Bill"].apply(lambda x: f"\\${x:.2f}")
                    st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Click the button above to load your account details")
