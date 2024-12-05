
import sys
import os

# Add the parent directory of the project to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from chat_assistant import ChatAssistant
from chat_assistant import ChatHistoryManager, ChatExporter
from chat_assistant import BASE_URL, MODEL, DB_CONNECTION



# Streamlit Page Configuration
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

# Initialize Chat Assistant
assistant = ChatAssistant(base_url=BASE_URL, model=MODEL, db_connection=DB_CONNECTION)
chat_exporter = ChatExporter()

# App Title
st.title("🤖 AI Chatbot")
st.write("Chat with your AI assistant. Type your messages below to get started!")

# Sidebar for User Settings
with st.sidebar:
    st.header("User Settings")
    user_id = st.text_input("Enter your User ID", value="user_101")

    # Export Button
    if st.button("Prepare Conversation for Download"):
        history_manager = ChatHistoryManager(DB_CONNECTION)
        messages = history_manager.get_user_messages(user_id)

        try:
            # Prepare text content
            text_content = chat_exporter.prepare_conversation_content(user_id, messages)
            
            # Prepare PDF file
            pdf_file_path = chat_exporter.export_conversation_as_pdf(user_id, messages)

            # Download as text button
            st.download_button(
                label="Download as Text",
                data=text_content,
                file_name=f"chat_{user_id}.txt",
                mime="text/plain",
            )

            # Download as PDF button
            with open(pdf_file_path, "rb") as pdf_file:
                st.download_button(
                    label="Download as PDF",
                    data=pdf_file,
                    file_name=f"chat_{user_id}.pdf",
                    mime="application/pdf",
                )

        except ValueError as e:
            st.error(f"Error: {e}")

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
        try:
            full_response = st.write_stream(assistant.chat_stream(session_id=user_id,user_input=user_input))
        except Exception as e:
            raise ValueError(f"Error: {e}")

    # Save assistant's response to chat history
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": full_response
    })
