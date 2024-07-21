import pdfplumber
import io
import base64
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging


class PDFProcessor:
    def __init__(self):
        load_dotenv()
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.vision_model = genai.GenerativeModel('gemini-pro-vision')

    def image_to_base64(self, image):
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def extract_text_from_image(self, image):
        try:
            base64_image = self.image_to_base64(image)
            response = self.vision_model.generate_content([
                "Describe the content of this image in detail, including any text or table information visible.",
                {"mime_type": "image/png", "data": base64_image}
            ])

            if hasattr(response, 'text') and response.text:
                return response.text
            else:
                # Check safety ratings (Gemini specific)
                if hasattr(response, 'prompt_feedback') and response.prompt_feedback.safety_ratings:
                    return "Image content could not be extracted due to safety concerns."
                else:
                    return "Unable to extract content from the image."
        except Exception as e:
            logging.error(f"Error extracting text from image: {str(e)}")
            return "Error occurred while processing the image."

    def process_pdf(self, file_path):
        content = []
        try:
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

                        extracted_text = self.extract_text_from_image(cropped_image)
                        content.append({"type": "image", "content": extracted_text, "page": page_num})

            content.sort(key=lambda x: x["page"])
        except Exception as e:
            logging.error(f"Error processing PDF: {str(e)}")
            content.append({"type": "error", "content": f"Error processing PDF: {str(e)}", "page": 0})

        return content

    def format_output(self, content):
        formatted_text = ""
        for item in content:
            if item["type"] == "text":
                formatted_text += f"Page {item['page']} - Extracted text:\n{item['content']}\n\n"
            elif item["type"] == "image":
                formatted_text += f"Page {item['page']} - Extracted image/table content:\n{item['content']}\n\n"
            elif item["type"] == "error":
                formatted_text += f"Error: {item['content']}\n\n"
        return formatted_text
