import google.generativeai as genai
import os
from dotenv import load_dotenv


class Chatbot:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-pro')
        self.message_history = []
        self.pdf_contents = []

    def add_pdf_content(self, content):
        self.pdf_contents.append(content)
        pdf_message = (f"Here's some additional content from a PDF: {content}\n\nPlease use this information along "
                       f"with any previous information to answer my questions.")
        self.add_message("user", pdf_message)
        bot_response = ("I've received the new PDF content. I'll incorporate this information into our conversation. "
                        "What would you like to know?")
        self.add_message("model", bot_response)
        return bot_response

    def add_message(self, role, content):
        # can pop back earlier messages to avoid memory overload
        self.message_history.append({"role": role, "parts": [content]})

    def chat(self, user_message):
        self.add_message("user", user_message)

        # Use the last 10 messages as context, or all messages if less than 10
        conversation = self.message_history[-10:]
        response = self.model.generate_content(conversation)
        self.add_message("model", response.text)

        return response.text

    def get_message_history(self):
        return [{"role": msg["role"], "content": msg["parts"][0]} for msg in self.message_history]
