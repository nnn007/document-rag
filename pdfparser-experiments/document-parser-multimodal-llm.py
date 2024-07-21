import pdfplumber
# from PIL import Image
import io
import base64
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro-vision')


def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


def extract_text_from_image(image):
    base64_image = image_to_base64(image)
    response = model.generate_content([
        "Describe the content of this image in detail, including any text or table information visible.",
        {"mime_type": "image/png", "data": base64_image}
    ])
    return response.text


def process_pdf(file_path):
    content = []
    with pdfplumber.open(file_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                content.append({"type": "text", "content": text, "page": page_num})

            for img in page.images:
                x0, top, x1, bottom = img["x0"], img["top"], img["x1"], img["bottom"]
                im = page.to_image()
                cropped_image = im.original.crop((x0, top, x1, bottom))
                cropped_image = cropped_image.convert("RGB")

                extracted_text = extract_text_from_image(cropped_image)
                content.append({"type": "image", "content": extracted_text, "page": page_num})

    content.sort(key=lambda x: x["page"])

    return content


def format_output(content):
    formatted_text = ""
    for item in content:
        if item["type"] == "text":
            formatted_text += f"Page {item['page']} - Extracted text:\n{item['content']}\n\n"
        else:
            formatted_text += f"Page {item['page']} - Extracted image/table content:\n{item['content']}\n\n"
    return formatted_text


# # Example usage
# example_file_path = "sample-documents/your-filename.pdf"
# processed_content = process_pdf(example_file_path)
# formatted_output = format_output(processed_content)
# print(formatted_output)
