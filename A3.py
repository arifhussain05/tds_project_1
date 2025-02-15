from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests, os
from flask import Flask
import json

from datetime import datetime





def a3_subprocess(date_string, formats):
    """
    Tries to convert a string to a date using multiple formats.

    Args:
        date_string: The string to convert.
        formats: A list of date format strings (e.g., ["%Y-%m-%d", "%m/%d/%Y"]).

    Returns:
        A datetime object if successful, None otherwise.  Also returns the format used.
    """
    for fmt in formats:
        
        try:
            date_object = datetime.strptime(date_string, fmt)
            #print("ddddddddddddddd",date_object, fmt, "date format", "<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>")
            return date_object # Return the date object and the format used.
        except ValueError:
            pass  # Try the next format

    return None, None  # No matching format found
formats = ["%Y-%m-%d", "%m/%d/%Y","%Y-%m-%d", "%m/%d/%Y", "%d-%m-%Y", "%Y/%m/%d", "%d-%b-%Y", "%Y/%m/%d %H:%M:%S", "%B %d, %Y", "%b %d, %Y"]

#app = FastAPI()
app = Flask(__name__)

@app.get("/a2")
def A2(prettier_version="prettier@3.4.2", filename="/data/format.md"):
    command = [r"C:\Program Files\nodejs\npx.cmd", prettier_version, "--write", filename]
    try:
        subprocess.run(command, check=True)
        print("Prettier executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


@app.get("/data_wednesday")
def a3():
    directory = "/data/"
    filename = "dates.txt"
    file_path = os.path.join(directory, filename)
    wednesday_count = 0
    #print(file_path, formats, "=======;;;;;;;;;")
    '''
    with open(file_path, "r") as file:
        contents = file.readlines()
    '''
    contents = []
    with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:  # Iterate line by line
                contents.append(line.strip())  # Process and add each line

    print(contents)
    #print("type of contents", type(contents))
    current_date = 0
    while current_date < len(contents):
        #print(contents[current_date], formats, "=======;;;;;;;;;")
        start = a3_subprocess(contents[current_date], formats)
        try:
            if start.weekday() == 2:  # weekday() returns 2 for Wednesday
                wednesday_count += 1
        except:
            pass
        current_date = current_date + 1
        
    print("wednesday_count====<<<>>>>", wednesday_count)
    directory = "/data/"
    filename = "dates-wednesdays.txt"
    file_path = os.path.join(directory, filename)
    fopen = open(file_path, 'a')
    fopen.write(str(wednesday_count))
    fopen.close()
    return wednesday_count





@app.get("/sort_lastname")
def a4():
    
    """Sorts contacts by last name, then first name.

    Args:
        contacts_json: A JSON string containing contact data.

    Returns:
        A JSON string containing the sorted contact data, or an error message if the input is invalid.
    """
    directory = "/data/"
    filename = "contacts.json"
    file_path = os.path.join(directory, filename)
    print(file_path, "===========>>>")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            contacts = json.load(f)

        # Sort by last name (case-insensitive), then first name (case-insensitive)
        contacts.sort(key=lambda contact: (contact.get("last_name", "").lower(), contact.get("first_name", "").lower()))  # Handle missing names

        directory = "/data/"
        filename = "contacts-sorted.json"
        file_path = os.path.join(directory, filename)
        with open("/data/contacts-sorted.json", "w", encoding="utf-8") as file:
            json.dump(contacts, file, indent=4)

        return json.dumps(contacts, indent=2)  # Convert the sorted list back to a JSON string

    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {filepath}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

        

@app.get("/last_modified_file")
def a5():
    """Lists the top 15 last modified files in a directory and saves them to a file.

    Args:
        directory: The path to the directory.
        output_file: The path to the output file.
    """
    import time
    directory = "/data/logs/"  # Replace with the actual directory path
    output_filepath = "/data/logs-recent.txt"  # Replace with the desired output file path

    files = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):  # Only include files (not directories)
            last_modified_time = os.path.getmtime(filepath)
            files.append((filepath, last_modified_time)) # Store filepath and modification time

    # Sort files by last modified time (most recent first)
    files.sort(key=lambda x: x[1], reverse=True)

    # Get the top 10 files (or fewer if there are less than 15)
    top_15 = files[:10]

    with open(output_filepath, 'w', encoding='utf-8') as outfile:
        for filepath, _ in top_15: # Write only the filepaths
            contents = []
            print("====<<>>>", top_15)
            with open(filepath, "r") as file:
                contents = file.readlines()
            outfile.write(contents[0])


    return True

'''
@app.get("/md_files")
def create_markdown_index():
    
    docs_dir = "/data/docs/"
    index_file = "/data/docs/index.json"
    index = {}
    import re
    try:
        for root, _, files in os.walk(docs_dir):  # Walk through the directory and subdirectories
            for file in files:
                if file.endswith(".md"):
                    filepath = os.path.join(root, file)
                    relative_path = os.path.relpath(filepath, docs_dir)  # Path relative to docs_dir

                    try:
                        with open(filepath, 'r', encoding='utf-8') as md_file:
                            for line in md_file:
                                match = re.match(r"^#\s*(.+)", line)  # Regex for H1
                                if match:
                                    title = match.group(1).strip()
                                    index[relative_path] = title
                                    break  # Stop after the first H1
                    except Exception as e:
                        print(f"Error processing {filepath}: {e}")

        with open(index_file, 'w', encoding='utf-8') as outfile:
            json.dump(index, outfile, indent=4, ensure_ascii=False)  # Save as JSON

        print(f"Markdown index created at {index_file}")

    except FileNotFoundError:
        print(f"Error: Directory not found at {docs_dir}")
    except Exception as e:
        print(f"An error occurred: {e}")
'''

@app.get("/md_files")
def a6():
    docs_dir = "/data/docs/"
    index_file = "/data/docs/index.json"
    index = {}
    import re
    
    docs_dir = "/data/docs/"
    index_file = os.path.join(docs_dir, "index.json")

    # Dictionary to store filename-to-title mapping
    index = {}

    # Iterate through all Markdown files in the directory
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, docs_dir)  # Get path relative to /data/docs/

                # Read file and extract first H1 title
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("# "):  # H1 title
                            index[rel_path] = line[2:].strip()  # Remove "# " and extra spaces
                            break  # Stop after first H1

    # Write index to JSON file
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=4)
    return "Success"

#with open("/data/email.txt", "r", encoding="utf-8") as f:
#        email_content = f.read()    
@app.get("/a7_sub")
def a7_subprocess():
    # ... inside your /run endpoint handler ...
    if "extract the sender’s email" in task_description.lower() or "extract Sender’s Email" in task_description:  # More robust matching
        try:
            email_file_path = os.path.join('/data/', "email.txt") # Use DATA_DIR
            with open(email_file_path, "r", encoding="utf-8") as f: # Specify encoding
                email_content = f.read()

            sender_email = extract_sender_email(email_content)

            output_file_path = os.path.join('/data/', "email-sender.txt") # Use DATA_DIR
            with open(output_file_path, "w", encoding="utf-8") as outfile: # Specify encoding
                outfile.write(sender_email)
            
            return jsonify({"message": "Sender email extracted successfully"}), 200

        except FileNotFoundError:
            return jsonify({"error": "/data/email.txt not found"}), 404
        except Exception as e:  # Catch any other potential errors
            return jsonify({"error": f"Error processing email: {e}"}), 500

@app.get("/a7")
def A7(filename='/data/email.txt', output_file='/data/email-sender.txt'):
    # Read the content of the email
    with open(filename, 'r') as file:
        email_content = file.readlines()

    sender_email = "sujay@gmail.com"
    for line in email_content:
        if "From" == line[:4]:
            sender_email = (line.strip().split(" ")[-1]).replace("<", "").replace(">", "")
            break

    # Get the extracted email address

    # Write the email address to the output file
    with open(output_file, 'w') as file:
        file.write(sender_email)



import sqlite3
import subprocess
from dateutil.parser import parse
from datetime import datetime
import json
from pathlib import Path
import os
import requests
from scipy.spatial.distance import cosine
from dotenv import load_dotenv

load_dotenv()

AIPROXY_TOKEN = os.getenv(str('eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIyZHMyMDAwMDkxQGRzLnN0dWR5LmlpdG0uYWMuaW4ifQ.-bLj3zVGOkq8TiW1DDM19cayzI35sNOTq10BqiIUlik').strip())


import base64
def png_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_string
# def A8():
#     input_image = "data/credit_card.png"
#     output_file = "data/credit-card.txt"

#     # Step 1: Extract text using OCR
#     try:
#         image = Image.open(input_image)
#         extracted_text = pytesseract.image_to_string(image)
#         print(f"Extracted text:\n{extracted_text}")
#     except Exception as e:
#         print(f"❌ Error reading or processing {input_image}: {e}")
#         return

#     # Step 2: Pass the extracted text to the LLM to validate and extract card number
#     prompt = f"""Extract the credit card number from the following text. Respond with only the card number, without spaces:

#     {extracted_text}
#     """
#     try:
#         card_number = ask_llm(prompt).strip()
#         print(f"Card number extracted by LLM: {card_number}")
#     except Exception as e:
#         print(f"❌ Error processing with LLM: {e}")
#         return

#     # Step 3: Save the extracted card number to a text file
#     try:
#         with open(output_file, "w", encoding="utf-8") as file:
#             file.write(card_number + "\n")
#         print(f"✅ Credit card number saved to: {output_file}")
#     except Exception as e:
#         print(f"❌ Error writing {output_file}: {e}")
@app.get("/a8")
def A8(filename='/data/credit_card.txt', image_path='/data/credit_card.png'):
    # Construct the request body for the AIProxy call
    body = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "There is 8 or more digit number is there in this image, with space after every 4 digit, only extract the those digit number without spaces and return just the number without any other characters"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{png_to_base64(image_path)}"
                        }
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AIPROXY_TOKEN}"
    }

    # Make the request to the AIProxy service
    response = requests.post("http://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
                             headers=headers, data=json.dumps(body))
    # response.raise_for_status()

    # Extract the credit card number from the response
    result = response.json()
    # print(result); return None
    print(result, "=============<<<<<>>>>>")
    card_number = result['choices'][0]['message']['content'].replace(" ", "")

    # Write the extracted card number to the output file
    with open(filename, 'w') as file:
        file.write(card_number)



def get_embedding(text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AIPROXY_TOKEN}"
    }
    data = {
        "model": "text-embedding-3-small",
        "input": [text]
    }
    response = requests.post("http://aiproxy.sanand.workers.dev/openai/v1/embeddings", headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response.json()["data"][0]["embedding"]

@app.get("/a9")
def A9():
    filename='/data/comments.txt'
    output_filename='/data/comments-similar.txt'
    # Read comments
    with open(filename, 'r') as f:
        comments = [line.strip() for line in f.readlines()]

    # Get embeddings for all comments
    embeddings = [get_embedding(comment) for comment in comments]

    # Find the most similar pair
    min_distance = float('inf')
    most_similar = (None, None)

    for i in range(len(comments)):
        for j in range(i + 1, len(comments)):
            distance = cosine(embeddings[i], embeddings[j])
            if distance < min_distance:
                min_distance = distance
                most_similar = (comments[i], comments[j])

    # Write the most similar pair to file
    with open(output_filename, 'w') as f:
        f.write(most_similar[0] + '\n')
        f.write(most_similar[1] + '\n')

@app.get("/a10")
def A10(filename='/data/ticket-sales.db', output_filename='/data/ticket-sales-gold.txt', query="SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'"):
    # Connect to the SQLite database
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    # Calculate the total sales for the "Gold" ticket type
    cursor.execute(query)
    total_sales = cursor.fetchone()[0]

    # If there are no sales, set total_sales to 0
    total_sales = total_sales if total_sales else 0

    # Write the total sales to the file
    with open(output_filename, 'w') as file:
        file.write(str(total_sales))

    # Close the database connection
    conn.close()


if __name__ == "__main__":
    app.run(debug = True)
    #import uvicorn
    #uvicorn.run(app, host="0.0.0.0", port=8001)
    #python -m uvicorn q3:app --reload --port 8001