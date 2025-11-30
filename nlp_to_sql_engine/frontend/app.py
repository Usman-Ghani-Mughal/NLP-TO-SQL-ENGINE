import streamlit as st
import styles.custom_css as custom_css
import components.sidebar as sidebar
from nlp_to_sql_engine.backend.main import start_agent

# Page configuration
st.set_page_config(
    page_title="Conversational BI Agent",
    page_icon="💬",
    layout="centered"
)

# Custom CSS for Claude-like styling
st.markdown(custom_css.main_css, unsafe_allow_html=True)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add initial greeting
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hi! I'm your Conversational BI Agent. Ask me any data question and I'll help you explore your insights through natural language."
    })

# Display title
st.title("💬 Conversational BI Agent")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me about your data..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    
    # CALL YOUR BACKEND HERE (before the chat_message block)
    response = start_agent(prompt)
    
    # Here you'll integrate your backend
    with st.chat_message("assistant"):
        st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    

# Add sidebar
sidebar.add_sidebar()