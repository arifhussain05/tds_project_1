import pytesseract
from PIL import Image
import openai
import re
import os

# Set your OpenAI API key
openai.api_key = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIyZHMyMDAwMDkxQGRzLnN0dWR5LmlpdG0uYWMuaW4ifQ.-bLj3zVGOkq8TiW1DDM19cayzI35sNOTq10BqiIUlik"  # Replace with your actual API key

# Load the image
directory = "/data/"
image_get = 'credit-card.png'
filepath = os.path.join(directory, image_get)
img = Image.open("D:/data/credit-card.png")

# Use OCR to extract text
ocr_text = pytesseract.image_to_string(img)

# LLM prompt
prompt = f"""Extract the credit card number from the following text.
Return only the credit card number without spaces.

Extracted text:
{ocr_text}
"""

# Call GPT-4o-Mini (or another model)
response = openai.ChatCompletion.create(
    model="gpt-4o-mini",  # Specify the model
    messages=[{"role": "system", "content": "You are an expert in extracting credit card numbers."},
              {"role": "user", "content": prompt}]
)

# Extract the number from the response
card_number = response["choices"][0]["message"]["content"].strip()

# Ensure it's a valid credit card format (16 digits)
card_number = re.sub(r"\D", "", card_number)  # Remove non-numeric characters

# Save to a file
output_path = "data/credit-card.txt"

with open(output_path, "w", encoding="utf-8") as f:
    f.write(card_number)

print(f"Credit card number saved to {output_path}: {card_number}")