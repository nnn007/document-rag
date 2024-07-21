import streamlit as st
import requests
import json

API_URL = "http://localhost:8000"

st.title("RAG Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    with st.chat_message("user" if role == "user" else "assistant"):
        st.markdown(content)

# File uploader for PDF
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    files = {"file": ("uploaded.pdf", uploaded_file, "application/pdf")}
    response = requests.post(f"{API_URL}/upload_pdf", files=files)
    if response.status_code == 200:
        st.success("PDF uploaded and processed successfully!")
        pdf_content = response.json()["content"]
        bot_response = response.json()["bot_response"]
        st.session_state.messages.append({"role": "model", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(bot_response)
    else:
        st.error(f"Error processing PDF: {response.text}")

# Accept user input
if prompt := st.chat_input("What is your question?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    message_placeholder = st.empty()
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={"messages": st.session_state.messages}
        )
        response.raise_for_status()
        full_response = response.json()["response"]

        # Update the entire message history (can be optimized here)
        st.session_state.messages = response.json()["message_history"]

        # Display the bot's response
        with st.chat_message("assistant"):
            message_placeholder.markdown(full_response)
    except requests.exceptions.RequestException as e:
        error_message = f"An error occurred: {str(e)}"
        with st.chat_message("assistant"):
            message_placeholder.error(error_message)
        st.session_state.messages.append({"role": "model", "content": error_message})
