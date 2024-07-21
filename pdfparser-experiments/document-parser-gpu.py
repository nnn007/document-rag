import pdfplumber
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import io
import torch
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


def extract_text_from_captioning(image):
    inputs = processor(images=image, return_tensors="pt").to(device)
    out = model.generate(**inputs, max_new_tokens=50)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption


def process_pdf(file_path):
    final_text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            final_text += f"Extracted page text:\n{text}\n" if text else ""

            for img in page.images:
                x0, top, x1, bottom = img["x0"], img["top"], img["x1"], img["bottom"]
                im = page.to_image()
                cropped_image = im.original.crop((x0, top, x1, bottom))
                cropped_image = cropped_image.convert("RGB")

                byte_arr = io.BytesIO()
                cropped_image.save(byte_arr, format="PNG")
                byte_arr = byte_arr.getvalue()

                image = Image.open(io.BytesIO(byte_arr))
                extracted_text = extract_text_from_captioning(image)
                final_text += f"Extracted image/table text: {extracted_text}\n"
    return final_text


# # Example usage
# file_path = "sample-documents/...."
# processed_text = process_pdf(file_path)
# print(processed_text)
