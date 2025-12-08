import streamlit as st
import styles.custom_css as custom_css
import components.sidebar as sidebar
import components.result_df as format_df
from nlp_to_sql_engine.backend.main import start_agent

# Page configuration
st.set_page_config(
    page_title="Conversational BI Agent",
    page_icon="💬",
    layout="centered"
)

# Custom CSS for Claude-like styling
st.markdown(custom_css.main_css, unsafe_allow_html=True)

# Display title
st.title("💬 Conversational BI Agent")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add initial greeting
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hi! I'm your Conversational BI Agent. Ask me any data question and I'll help you explore your insights through natural language."
    })


# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Handle different content types
        if isinstance(message["content"], dict) and "success" in message["content"]:
            # This is a query result response
            if message["content"]["success"]:
                st.markdown("✅ Query executed successfully!")
                
                with st.expander("📝 View Generated SQL Query", expanded=False):
                    st.code(message["content"]["query"], language="sql")
                
                if message["content"]["response"] is not None and len(message["content"]["response"]) > 0:
                    #st.markdown(f"**Results:** {message['content']['row_count']} rows returned")
                    df = message["content"]["response"]
                    # Show metrics
                    format_df.display_dataframe(df)
                else:
                    st.info("✓ Query executed successfully but returned no results.")
            else:
                st.error(f"❌ Query execution failed: ")
                if message["content"]["query"]:
                    with st.expander("📝 View Generated SQL Query"):
                        st.code(message["content"]["query"], language="sql")
        else:
            # Regular text message (like initial greeting)
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me about your data..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Call your backend to get SQL query and results
    try:
        # Get response from backend
        backend_response = start_agent(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            if backend_response["success"]:
                # Show success message
                st.markdown("✅ Query executed successfully!")
                
                # Display the SQL query in an expandable section
                with st.expander("📝 View Generated SQL Query", expanded=False):
                    st.code(backend_response["query"], language="sql")
                
                # Display the results
                if backend_response["response"] is not None and len(backend_response["response"]) > 0:
                    # st.markdown(f"**Results:** {backend_response['row_count']} rows returned")
                    df = backend_response["response"]
                    
                    format_df.display_dataframe(df)
                    
                    # Display as interactive dataframe
                    # st.dataframe(
                    #     backend_response["response"],
                    #     use_container_width=True,
                    #     hide_index=True
                    # )
                    
                else:
                    st.info("✓ Query executed successfully but returned no results.")
                
                # Add to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": backend_response
                })
            else:
                # Show error
                st.error(f"❌ Query execution failed:")
                with st.expander("📝 View Generated SQL Query"):
                    st.code(backend_response["query"], language="sql")
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": backend_response
                })
    
    except Exception as e:
        with st.chat_message("assistant"):
            st.error(f"❌ An error occurred: {str(e)}")
            st.session_state.messages.append({
                "role": "assistant",
                "content": {"success": False, "error": str(e), "query": None}
            })

    

# Add sidebar
sidebar.add_sidebar()