import streamlit as st

def add_sidebar():
    with st.sidebar:
        st.markdown("### Options")
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.session_state.messages.append({
            "role": "assistant",
            "content": "Hi! I'm your Conversational BI Agent. Ask me any data question and I'll help you explore your insights through natural language."
            })
            st.rerun()