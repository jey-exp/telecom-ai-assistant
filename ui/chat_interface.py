"""
Chat Interface Component
Renders the chat UI for interacting with AI agents.
"""

import streamlit as st

def render_chat_tab(tab_name, tab_obj):
    """Render chat interface for service tabs (Billing, Network, Plans, Knowledge)"""
    with tab_obj:
        if tab_name not in st.session_state.messages:
            st.session_state.messages[tab_name] = []
        
        # Display chat history
        for msg in st.session_state.messages[tab_name]:
            with st.chat_message(msg["role"]):
                # Escape $ to prevent LaTeX rendering
                st.markdown(msg["content"].replace("$", "\\$"))
        
        # Chat input at bottom
        placeholder = "Ask anything..." if tab_name == "Assistant" else f"Ask about {tab_name.lower()}..."
        if prompt := st.chat_input(placeholder, key=f"chat_{tab_name}"):
            st.session_state.messages[tab_name].append({"role": "user", "content": prompt})
            
            try:
                # Determine service type (None for Assistant to trigger classification)
                service_type = None if tab_name == "Assistant" else tab_name.lower()
                
                # Invoke LangGraph with customer context and explicit service type
                result = st.session_state.graph.invoke({
                    "query": prompt,
                    "service_type": service_type,
                    "chat_history": [],
                    "classification": None,
                    "intermediate_responses": {},
                    "final_response": None,
                    "user_email": st.session_state.user_email,
                    "customer_info": {"email": st.session_state.user_email}
                })
                
                response = result.get("final_response", "No response")
                st.session_state.messages[tab_name].append({"role": "assistant", "content": response})
                st.rerun()
            except Exception as e:
                st.session_state.messages[tab_name].append({"role": "assistant", "content": f"Error: {str(e)}"})
                st.rerun()
