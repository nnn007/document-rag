import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from pdf_processor import PDFProcessor
from chatbot import Chatbot
from typing import List
import os
import logging

app = FastAPI()
pdf_processor = PDFProcessor()
chatbot = Chatbot()

logging.basicConfig(level=logging.INFO)


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    try:
        contents = await file.read()
        with open(file.filename, "wb") as f:
            f.write(contents)

        processed_content = pdf_processor.process_pdf(file.filename)
        formatted_output = pdf_processor.format_output(processed_content)

        os.remove(file.filename)  # Clean up the temporary file

        # Add the PDF content to the chatbot and get the response
        bot_response = chatbot.add_pdf_content(formatted_output)

        return {"message": "PDF processed successfully", "content": formatted_output, "bot_response": bot_response}
    except Exception as e:
        logging.error(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        user_message = request.messages[-1].content
        response = chatbot.chat(user_message)
        return {"response": response, "message_history": chatbot.get_message_history()}
    except Exception as e:
        logging.error(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in chat: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
