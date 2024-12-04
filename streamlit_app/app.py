
import sys
import os

# Add the parent directory of the project to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from chat_assistant import ChatAssistant
from chat_assistant import ChatHistoryManager
from chat_assistant import BASE_URL, MODEL, DB_CONNECTION



# Streamlit Page Configuration
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

# Initialize Chat Assistant
assistant = ChatAssistant(base_url=BASE_URL, model=MODEL, db_connection=DB_CONNECTION)

# App Title
st.title("🤖 AI Chatbot")
st.write("Chat with your AI assistant. Type your messages below to get started!")

# Sidebar for User Settings
with st.sidebar:
    st.header("User Settings")
    user_id = st.text_input("Enter your User ID", value="user_101")

    # Start a new conversation
    if st.button("Start New Conversation"):
        st.session_state.chat_history = []
        history_manager = ChatHistoryManager(DB_CONNECTION)
        history_manager.clear_user_history(user_id)
        st.success("Conversation cleared!")


# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display existing chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input prompt
user_input = st.chat_input("Type your message...")

if user_input:
    # Append user message to chat history
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response using the assistant
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        try:
            for chunk in assistant.runnable_with_history.stream(
                {"input": user_input},
                config={"configurable": {"session_id": user_id}}
            ):
                full_response += chunk
                response_placeholder.markdown(full_response)
        except Exception as e:
            response_placeholder.markdown(f"Error: {e}")

    # Save assistant's response to chat history
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": full_response
    })
