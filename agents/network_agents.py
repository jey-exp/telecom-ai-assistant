"""
Network Agent - AutoGen multi-agent troubleshooting system.
Checks account status first, then provides diagnostics or reactivation guidance.
"""

import autogen
from utils.database import db
from config.config import config

# Define network troubleshooting agents with database context
config_list = [{"model": "gpt-4o", "api_key": config.OPENAI_API_KEY}]

Diagnostics_Agent = autogen.AssistantAgent(
    name="Diagnostics_Agent",
    system_message="""You are a telecom network diagnostics specialist. 

CRITICAL INSTRUCTION: You will receive customer information including their account status.

**CHECK ACCOUNT STATUS FIRST:**
- If account status is "Suspended" or "Cancelled":
  → IMMEDIATELY inform the customer their account is suspended/cancelled
  → Explain this is WHY they can't make calls/use services  
  → Tell them to contact billing/customer service to reactivate
  → DO NOT provide generic network troubleshooting
  
- If account status is "Active":
  → Proceed with normal network diagnostic steps
  → Check signal, device settings, network outages, etc.

Always prioritize account status before any other troubleshooting!""",
    llm_config={"config_list": config_list, "temperature": 0.7}
)

Solution_Integrator = autogen.AssistantAgent(
    name="Solution_Integrator",
    system_message="""You are a network solution integrator providing final solutions.

Based on the diagnostics:
- If account is suspended → Provide clear steps to reactivate account
- If network issue → Provide step-by-step troubleshooting
- Be concise and actionable""",
    llm_config={"config_list": config_list, "temperature": 0.7}
)

user_proxy = autogen.UserProxyAgent(
    name="User_Proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=0,
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
    code_execution_config=False
)

# Setup group chat
groupchat = autogen.GroupChat(
    agents=[user_proxy, Diagnostics_Agent, Solution_Integrator],
    messages=[],
    max_round=6
)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})

def process_network_query(query, customer_email="user@example.com"):
    """Run the AutoGen network troubleshooting flow with customer context."""
    
    # Import here to avoid circular imports
    from services.customer_service import get_user_role, get_customer_profile
    
    # Get user role first
    user_role = get_user_role(customer_email)
    
    if user_role == 'admin':
        # Admin gets network system overview
        return handle_admin_network_query(query, customer_email)
    elif user_role == 'customer':
        # Customer gets personal troubleshooting
        return handle_customer_network_query(query, customer_email)
    else:
        return "⚠️ Access denied: Invalid user credentials"

def handle_admin_network_query(query, admin_email):
    """Handle network queries for admin users"""
    
    # Get network system overview for admin
    try:
        # Get network incidents summary
        incidents_query = """
        SELECT COUNT(*) as total_incidents, 
               COUNT(CASE WHEN status = 'open' THEN 1 END) as open_incidents
        FROM network_incidents
        """
        incidents = db.query_one(incidents_query, [])
        
        # Get customer account status summary
        status_query = """
        SELECT account_status, COUNT(*) as count
        FROM customers
        GROUP BY account_status
        """
        status_summary = db.query(status_query, [])
        
        admin_context = f"""
NETWORK SYSTEM OVERVIEW (Admin View):
- Total Network Incidents: {incidents[0] if incidents else 0}
- Open Incidents: {incidents[1] if incidents else 0}
- Customer Status Summary: {status_summary}

Admin Query: {query}
"""
        
        # Use AutoGen for admin analysis
        user_proxy.initiate_chat(
            manager,
            message=f"{admin_context}\n\nProvide network system analysis and recommendations for admin."
        )
        
        return user_proxy.last_message()["content"] if user_proxy.chat_messages else "Admin network analysis completed."
        
    except Exception as e:
        return f"⚠️ Admin network query error: {str(e)}"

def handle_customer_network_query(query, customer_email):
    """Handle network queries for customer users"""
    
    # Get customer info from database
    try:
        customer_query = """
        SELECT c.customer_id, c.name, c.account_status, c.service_plan_id,
               p.name as plan_name
        FROM customers c
        LEFT JOIN service_plans p ON c.service_plan_id = p.plan_id
        WHERE c.email = ?
        """
        customer_data = db.query_one(customer_query, [customer_email])
        
        if not customer_data:
            return f"⚠️ Customer profile not found for email: {customer_email}"
        
        customer_context = f"""
CUSTOMER INFORMATION (CHECK THIS FIRST!):
- Customer Name: {customer_data[1]}
- Account Status: {customer_data[2]} ← **CRITICAL: Check this first!**
- Current Plan: {customer_data[4]}
"""
    except Exception as e:
        customer_context = f"Error fetching customer data: {str(e)}\nProceeding with generic troubleshooting."
    
    # Reset chat history
    groupchat.messages = []
    
    # Initiate chat with customer context
    chat_result = user_proxy.initiate_chat(
        manager,
        message=f"""{customer_context}

Customer Issue: {query}

IMPORTANT INSTRUCTIONS:
1. READ the account status above CAREFULLY
2. If account is Suspended/Cancelled → Address this IMMEDIATELY as the root cause
3. If account is Active → Then proceed with network diagnostics
4. End your final response with TERMINATE"""
    )
    
    # Extract the final response
    if chat_result.chat_history:
        agent_messages = [m for m in chat_result.chat_history if m['name'] != 'User_Proxy']
        if agent_messages:
            last_msg = agent_messages[-1]['content']
            return last_msg.replace("TERMINATE", "").strip()
    
    return "I'm sorry, I couldn't diagnose the network issue at this time."
