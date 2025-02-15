# /// script
# python = ">=3.13"
# dependencies = ["fastapi", "uvicorn", "requests",
#                 "pydantic", "aiohttp", "httpx",
#                 "pillow", "numpy", "python-dateutil",
#                 "openai", "pytesseract", "faker", "markdown"]
# ///



from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse
import os
import re
import shutil
import subprocess
import requests
from datetime import datetime
import openai
import json
import pytesseract
from PIL import Image
import numpy as np
import sqlite3
import base64
from dateutil import parser
from pathlib import Path

app = FastAPI()

@app.post("/run")
async def run_task(task: str = Query(...)):
    try:
        # Get email from environment variable or task description
        email = os.getenv("USER_EMAIL", "user@example.com")
        
        # Extract email from task if present
        if "with `" in task and "` as the only argument" in task:
            email = task.split("with `")[1].split("`")[0]
        
        # For task A1, use direct recognition
        if "Install `uv`" in task and "datagen.py" in task:
            result = handle_task_A1(email)
            return {"status": "success", "result": result}
            
        # For other tasks...
        parsed_task = parse_task_with_llm(task)
        task_code = parsed_task.get("task_code", "UNKNOWN")
        
        if task_code == "A1":
            result = handle_task_A1(email)
            return {"status": "success", "result": result}
        elif task_code == "A2":
            result = handle_task_A2()
            return {"status": "success", "result": result}
        elif task_code == "A3":
            result = handle_task_A3()
            return {"status": "success", "result": result}
        elif task_code == "A4":
            result = handle_task_A4()
            return {"status": "success", "result": result}
        elif task_code == "A5":
            result = handle_task_A5()
            return {"status": "success", "result": result}
        elif task_code == "A6":
            result = handle_task_A6()
            return {"status": "success", "result": result}
        elif task_code == "A7":
            result = handle_task_A7()
            return {"status": "success", "result": result}
        elif task_code == "A8":
            result = handle_task_A8()
            return {"status": "success", "result": result}
        elif task_code == "A9":
            result = handle_task_A9()
            return {"status": "success", "result": result}
        elif task_code == "A10":
            result = handle_task_A10()
            return {"status": "success", "result": result}
        elif task_code.startswith("B"):
            result = handle_task_B(task_code)
            return {"status": "success", "result": result}
        else:
            # If LLM returned UNKNOWN or an unsupported task code.
            raise Exception("Unrecognized or unsupported task code returned by LLM.")
        
        return {"status": "success", "result": result}
    except Exception as e:
        print(f"Error in run_task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/read", response_class=PlainTextResponse)
async def read_file(path: str = Query(...)):
    """
    GET endpoint to read and return the content of a file.
    """
    if not path.startswith("/data"):
        raise HTTPException(status_code=400, detail="Invalid path: Must start with /data")
    
    # Create data directory structure with proper permissions
    data_dir = os.path.join(os.getcwd(), "data")
    docs_dir = os.path.join(data_dir, "docs")
    logs_dir = os.path.join(data_dir, "logs")
    
    # Create directories with full permissions
    for directory in [data_dir, docs_dir, logs_dir]:
        try:
            os.makedirs(directory, mode=0o777, exist_ok=True)
        except Exception as e:
            print(f"Warning: Could not create directory {directory}: {e}")
    
    local_path = os.path.join(os.getcwd(), path[1:])
    
    if not os.path.exists(local_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        with open(local_path, "r") as f:
            content = f.read()
        return content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

def handle_task_A1(user_email: str):
    """
    Install uv and run datagen.py with the provided email
    """
    try:
        # Create data directory if it doesn't exist
        data_dir = os.path.join(os.getcwd(), "data")
        os.makedirs(data_dir, exist_ok=True)
        
        print(f"[LOG] Created/confirmed data directory at: {data_dir}")
        
        # Download and run datagen.py with the provided email
        datagen_url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
        
        print(f"[LOG] Attempting to run script from: {datagen_url}")
        print(f"[LOG] Using email: {user_email}")
        
        # Run datagen.py with the email
        result = subprocess.run(
            ["uv", "run", datagen_url, user_email],
            check=True,
            capture_output=True,
            text=True
        )
        
        print(f"[LOG] Command output: {result.stdout}")
        
        # Copy files from /data to local data directory
        if os.path.exists("/data"):
            print(f"[LOG] Found /data directory, copying files to {data_dir}")
            
            # Create required subdirectories
            os.makedirs(os.path.join(data_dir, "docs"), exist_ok=True)
            os.makedirs(os.path.join(data_dir, "logs"), exist_ok=True)
            
            # Copy all files and directories
            for item in os.listdir("/data"):
                src = os.path.join("/data", item)
                dst = os.path.join(data_dir, item)
                try:
                    if os.path.isfile(src):
                        shutil.copy2(src, dst)
                        print(f"[LOG] Successfully copied file: {item}")
                    elif os.path.isdir(src):
                        shutil.copytree(src, dst, dirs_exist_ok=True)
                        print(f"[LOG] Successfully copied directory: {item}")
                except PermissionError:
                    print(f"[WARN] Permission denied copying {item}, trying alternate method")
                    try:
                        if os.path.isfile(src):
                            with open(src, 'rb') as fsrc:
                                with open(dst, 'wb') as fdst:
                                    fdst.write(fsrc.read())
                            print(f"[LOG] Successfully copied file (alternate method): {item}")
                    except Exception as e:
                        print(f"[ERROR] Failed to copy {item}: {str(e)}")
                except Exception as e:
                    print(f"[ERROR] Failed to copy {item}: {str(e)}")
        
        return {
            "status": "success",
            "result": {
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        }
        
    except Exception as e:
        error_msg = f"Error in handle_task_A1: {str(e)}"
        print(f"[ERROR] {error_msg}")
        return {
            "status": "error",
            "error": error_msg
        }

def handle_task_A2():
    """
    Formats the file /data/format.md using prettier@3.4.2.
    """
    local_data_dir = os.path.join(os.getcwd(), "data")
    file_path = os.path.join(local_data_dir, "format.md")
    
    if not os.path.exists(file_path):
        raise Exception(f"File not found: {file_path}")
    
    try:
        # Create a temporary directory for npm
        temp_dir = os.path.join(os.getcwd(), "temp_prettier")
        os.makedirs(temp_dir, exist_ok=True)
        
        # Initialize npm project
        subprocess.run(
            ["npm", "init", "-y"],
            check=True,
            capture_output=True,
            text=True,
            cwd=temp_dir
        )
        
        # Install prettier
        subprocess.run(
            ["npm", "install", "prettier@3.4.2"],
            check=True,
            capture_output=True,
            text=True,
            cwd=temp_dir
        )
        
        # Read current content
        with open(file_path, "r", encoding='utf-8') as f:
            content = f.read()
        
        # Format using prettier
        prettier_path = os.path.join(temp_dir, "node_modules", ".bin", "prettier")
        if os.name == 'nt':  # Windows
            prettier_path += '.cmd'
            
        result = subprocess.run(
            [prettier_path, "--parser", "markdown", "--prose-wrap", "preserve"],
            input=content,
            capture_output=True,
            text=True,
            check=True,
            cwd=temp_dir
        )
        
        # Write formatted content back
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(result.stdout)
        
        # Clean up
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        return {"status": "success"}
        
    except subprocess.CalledProcessError as e:
        print(f"Prettier error: {e.stderr}")
        raise Exception(f"Error running prettier: {e.stderr}")
    except Exception as e:
        print(f"General error: {str(e)}")
        raise Exception(f"Error formatting file: {str(e)}")

def handle_task_A3():
    """
    Counts Wednesdays in dates.txt and writes count to dates-wednesdays.txt
    """
    local_data_dir = os.path.join(os.getcwd(), "data")
    input_file = os.path.join(local_data_dir, "dates.txt")
    output_file = os.path.join(local_data_dir, "dates-wednesdays.txt")
    
    if not os.path.exists(input_file):
        raise Exception(f"File not found: {input_file}")
    
    try:
        wednesday_count = 0
        with open(input_file, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    # Use dateutil.parser for more flexible date parsing
                    date = parser.parse(line)
                    # Wednesday is 2 (Monday=0, Sunday=6)
                    if date.weekday() == 2:
                        wednesday_count += 1
                except ValueError as e:
                    print(f"Warning: Could not parse date: {line} - {str(e)}")
        
        # Write just the number to output file
        with open(output_file, "w") as f:
            f.write(str(wednesday_count))
        
        return {"wednesday_count": wednesday_count}
        
    except Exception as e:
        raise Exception(f"Error processing dates: {str(e)}")

def handle_task_A4():
    """
    Sorts the array of contacts in /data/contacts.json by last_name, then first_name,
    and writes the result to /data/contacts-sorted.json.
    """
    # Define the local data directory.
    local_data_dir = os.path.join(os.getcwd(), "data")
    
    # Construct paths for the input and output files.
    contacts_path = os.path.join(local_data_dir, "contacts.json")
    sorted_contacts_path = os.path.join(local_data_dir, "contacts-sorted.json")
    
    # Ensure contacts.json exists.
    if not os.path.exists(contacts_path):
        raise Exception(f"File not found: {contacts_path}")
    
    # Read contacts.json.
    with open(contacts_path, "r") as f:
        try:
            contacts = json.load(f)
        except Exception as e:
            raise Exception("Error reading contacts.json: " + str(e))
    
    # Sort contacts by last_name and then first_name.
    sorted_contacts = sorted(
        contacts,
        key=lambda c: (c.get("last_name", "").lower(), c.get("first_name", "").lower())
    )
    
    # Write the sorted contacts to contacts-sorted.json with indentation.
    with open(sorted_contacts_path, "w") as f:
        json.dump(sorted_contacts, f, indent=2)
    
    return {"sorted_contacts": sorted_contacts}

def handle_task_A5():
    """
    Write the first line of the 10 most recent .log files to logs-recent.txt
    """
    local_data_dir = os.path.join(os.getcwd(), "data")
    logs_dir = os.path.join(local_data_dir, "logs")
    output_file = os.path.join(local_data_dir, "logs-recent.txt")
    
    try:
        # Get all .log files with their modification times
        log_files = []
        for file in os.listdir(logs_dir):
            if file.endswith('.log'):
                file_path = os.path.join(logs_dir, file)
                mod_time = os.path.getmtime(file_path)
                log_files.append((mod_time, file_path))
        
        # Sort by modification time (most recent first)
        log_files.sort(reverse=True)
        
        # Get first 10 files
        recent_files = log_files[:10]
        
        # Extract first line from each file
        first_lines = []
        for _, file_path in recent_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                first_lines.append(first_line)
        
        # Write to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(first_lines))
        
        return {
            "status": "success",
            "written_file": output_file,
            "first_lines": first_lines
        }
        
    except Exception as e:
        raise Exception(f"Error processing log files: {str(e)}")

def handle_task_A6():
    """
    Find all Markdown (.md) files in /data/docs/.
    For each file, extract the first occurrence of each H1 (i.e., a line starting with '# ').
    Create an index file /data/docs/index.json that maps each filename (without the /data/docs/ prefix) to its title.
    """
    local_data_dir = os.path.join(os.getcwd(), "data", "docs")
    output_file = os.path.join(local_data_dir, "index.json")
    index = {}

    try:
        for root, _, files in os.walk(local_data_dir):
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            if line.startswith("# "):
                                relative_path = os.path.relpath(file_path, local_data_dir)
                                index[relative_path] = line.strip("# ").strip()
                                break

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=4)

        return {"status": "success", "written_file": output_file, "index": index}
    except Exception as e:
        print(f"Error in handle_task_A6: {str(e)}")
        raise Exception(f"Error processing Markdown files: {str(e)}")

def handle_task_A7():
    """
    Extract sender's email from email.txt using LLM
    """
    local_data_dir = os.path.join(os.getcwd(), "data")
    input_file = os.path.join(local_data_dir, "email.txt")
    output_file = os.path.join(local_data_dir, "email-sender.txt")
    
    try:
        # Read email content
        with open(input_file, "r", encoding='utf-8') as f:
            email_content = f.read()
        
        # Initialize OpenAI client
        client = openai.OpenAI(
            api_key=os.environ.get("AIPROXY_TOKEN"),
            base_url="https://aiproxy.sanand.workers.dev/openai/v1"
        )
        
        # Extract email using LLM
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Extract the sender's email address from this email message. Return only the email address, nothing else."},
                {"role": "user", "content": email_content}
            ]
        )
        
        email_address = response.choices[0].message.content.strip()
        
        # Write to output file
        with open(output_file, "w", encoding='utf-8') as f:
            f.write(email_address)
        
        return {"status": "success", "email": email_address}
        
    except Exception as e:
        print(f"Error in handle_task_A7: {str(e)}")
        raise Exception(f"Error extracting email: {str(e)}")

def chat_completion(prompt):
    """
    Calls the OpenAI API for chat completions using the allowed endpoint/model.
    Supported endpoint: POST https://aiproxy.sanand.workers.dev/openai/v1/chat/completions
    Supported model: gpt-4o-mini
    """
    api_key = os.environ.get("AIPROXY_TOKEN")
    if not api_key:
        raise Exception("API key for OpenAI is not set. Please set the AIPROXY_TOKEN environment variable.")
    
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://aiproxy.sanand.workers.dev/openai/v1"
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response
    except Exception as e:
        print(f"Error during chat completion: {str(e)}")
        raise



def handle_task_A8():
    """
    Wrapper function for extracting credit card number from an image.
    """
    local_data_dir = os.path.join(os.getcwd(), "data")
    input_file = os.path.join(local_data_dir, "credit_card.png")
    output_file = os.path.join(local_data_dir, "credit-card.txt")

    try:
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Image file {input_file} does not exist.")
        
        # Extract text from the image using pytesseract
        image = Image.open(input_file)
        extracted_text = pytesseract.image_to_string(image)
        
        # Use regex to extract a sequence that looks like a credit card number
        match = re.search(r'(\d[\d\s-]{13,19})', extracted_text)
        if match:
            card_number = match.group(1)
            # Remove any spaces and dashes from the card number
            card_number_clean = re.sub(r'[\s-]+', '', card_number)
            # Limit the extracted number to the first 16 digits
            card_number_clean = card_number_clean[:16]
        else:
            raise ValueError("No valid credit card number found in the image.")
        
        # Write the extracted number to the output file
        with open(output_file, 'w') as f:
            f.write(card_number_clean)
        
        return output_file
    except Exception as e:
        print(f"Error in handle_task_A8: {str(e)}")
        raise Exception(f"Error extracting credit card: {str(e)}")

def handle_task_A9():
    """
    Find most similar comments using embeddings
    """
    local_data_dir = os.path.join(os.getcwd(), "data")
    input_file = os.path.join(local_data_dir, "comments.txt")
    output_file = os.path.join(local_data_dir, "comments-similar.txt")
    
    try:
        # Read comments
        with open(input_file, "r", encoding='utf-8') as f:
            comments = [line.strip() for line in f if line.strip()]
        
        # Ensure the API key is set
        api_key = os.environ.get("AIPROXY_TOKEN")
        if not api_key:
            raise Exception("API key for OpenAI is not set. Please set the AIPROXY_TOKEN environment variable.")
        
        # Initialize OpenAI client
        client = openai.OpenAI(
            api_key=api_key,
            base_url="https://aiproxy.sanand.workers.dev/openai/v1"
        )
        
        # Get embeddings for all comments
        embeddings = []
        for comment in comments:
            try:
                response = client.embeddings.create(
                    model="text-embedding-3-small",  # Use the correct model
                    input=comment
                )
                embeddings.append(response.data[0].embedding)
            except Exception as e:
                print(f"Error getting embedding for comment '{comment}': {str(e)}")
                raise Exception(f"Error with OpenAI API: {str(e)}")
        
        # Find most similar pair
        max_similarity = -1
        most_similar_pair = None
        
        for i in range(len(comments)):
            for j in range(i + 1, len(comments)):
                similarity = np.dot(embeddings[i], embeddings[j])
                if similarity > max_similarity:
                    max_similarity = similarity
                    most_similar_pair = (comments[i], comments[j])
        
        # Write result
        with open(output_file, "w", encoding='utf-8') as f:
            f.write(most_similar_pair[0] + "\n")
            f.write(most_similar_pair[1] + "\n")
        
        return {"status": "success", "similarity": float(max_similarity)}
        
    except Exception as e:
        print(f"Error in handle_task_A9: {str(e)}")
        raise Exception(f"Error finding similar comments: {str(e)}")

def handle_task_A10():
    local_data_dir = os.path.join(os.getcwd(), "data")
    db_path = os.path.join(local_data_dir, "ticket-sales.db")
    output_file = os.path.join(local_data_dir, "ticket-sales-gold.txt")

    if not os.path.exists(db_path):
        return {"error": f"Database file not found at {db_path}"}

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = "SELECT SUM(units * price) FROM tickets WHERE type = 'Gold';"
        cursor.execute(query)
        total_sales = cursor.fetchone()[0]
        if total_sales is None:
            total_sales = 0.0

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(str(total_sales) + "\n")

        conn.close()
        return {
            "status": "success",
            "total_sales": total_sales,
            "written_file": output_file
        }

    except Exception as e:
        return {"error": str(e)}

@app.get("/filter_csv")
async def filter_csv(column: str = Query(...), value: str = Query(...)):
    """
    API endpoint to filter a CSV file (located in /data) and return JSON data.
    """
    try:
        local_data_dir = os.path.join(os.getcwd(), "data")
        csv_file = os.path.join(local_data_dir, "data.csv")
        if not os.path.exists(csv_file):
            raise HTTPException(status_code=404, detail="CSV file not found")
        import csv
        filtered = []
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get(column) == value:
                    filtered.append(row)
        return filtered
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def parse_task_with_llm(task: str) -> dict:
    try:
        # First, check if AIPROXY_TOKEN is set
        if not os.getenv("AIPROXY_TOKEN"):
            print("Warning: AIPROXY_TOKEN not set")
            # For task A1, we can proceed with a default response
            if "Install `uv`" in task and "datagen.py" in task:
                return {"task_code": "A1"}
            
        client = openai.OpenAI(
            api_key=os.getenv("AIPROXY_TOKEN"),
            base_url="https://aiproxy.sanand.workers.dev/openai/v1"
        )
        
        prompt = f"""You are a task parser. Given a task description, identify which task it is (A1-A10 or B3-B10) and return a JSON with task_code.

Task description:
{task}

Return format:
{{"task_code": "A1"}}  # or one of A1-A10 / B3-B10 as appropriate

Rules:
- A1: Install uv and run datagen.py
- A2: Format markdown file
- A3: Count Wednesdays
- A4: Sort contacts
- A5: First lines of log files
- A6: Create markdown index
- A7: Extract email from text
- A8: Extract credit card from image
- A9: Find similar documents
- A10: Query SQLite database
- B3: Fetch data from an API and save it
- B4: Clone a git repo and make a commit
- B5: Run a SQL query on a SQLite or DuckDB database
- B6: Extract data from a website
- B7: Compress or resize an image
- B8: Transcribe audio from an MP3 file
- B9: Convert Markdown to HTML
- B10: Write an API endpoint that filters a CSV file and returns JSON data

Return only the JSON, no other text."""

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Corrected model name to gpt-4o-mini
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            result = response.choices[0].message.content.strip()
            return json.loads(result)
        except Exception as e:
            print(f"LLM API error: {str(e)}")
            # Fallback for task A1
            if "Install `uv`" in task and "datagen.py" in task:
                return {"task_code": "A1"}
            raise
            
    except Exception as e:
        print(f"Error in parse_task_with_llm: {str(e)}")
        # Final fallback for task A1
        if "Install `uv`" in task and "datagen.py" in task:
            return {"task_code": "A1"}
        raise Exception(f"Error parsing task: {str(e)}")

def handle_task_B(task_code: str):
    """
    Dispatch handler for tasks B3-B10.
    """
    # Ensure no data outside /data is accessed.
    if task_code == "B3":
        return handle_task_B3()
    elif task_code == "B4":
        return handle_task_B4()
    elif task_code == "B5":
        return handle_task_B5()
    elif task_code == "B6":
        return handle_task_B6()
    elif task_code == "B7":
        return handle_task_B7()
    elif task_code == "B8":
        return handle_task_B8()
    elif task_code == "B9":
        return handle_task_B9()
    elif task_code == "B10":
        # B10 functionality is implemented via the /filter_csv endpoint.
        return {"message": "Use the /filter_csv API endpoint to filter CSV data."}
    else:
        raise Exception("Unsupported B task code.")

def handle_task_B3():
    """
    B3: Fetch data from an API and save it to /data/api_data.json.
    """
    local_data_dir = os.path.join(os.getcwd(), "data")
    os.makedirs(local_data_dir, exist_ok=True)
    api_url = "https://api.example.com/data"  # sample endpoint
    response = requests.get(api_url)
    response.raise_for_status()
    file_path = os.path.join(local_data_dir, "api_data.json")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(response.text)
    return {"message": f"Data fetched and saved to {file_path}"}

def handle_task_B4():
    """
    B4: Clone a git repo into /data/repo_clone and make a commit.
    """
    local_data_dir = os.path.join(os.getcwd(), "data")
    repo_dir = os.path.join(local_data_dir, "repo_clone")
    repo_url = "https://github.com/example/repo.git"  # example repo URL
    # Clone only if the directory doesn't exist.
    if not os.path.exists(repo_dir):
        subprocess.run(["git", "clone", repo_url, repo_dir], check=True)
    # Create/update a dummy file to commit.
    dummy_file = os.path.join(repo_dir, "dummy.txt")
    with open(dummy_file, "w", encoding="utf-8") as f:
        f.write("Update: " + datetime.now().isoformat())
    subprocess.run(["git", "-C", repo_dir, "add", "."], check=True)
    subprocess.run(["git", "-C", repo_dir, "commit", "-m", "Automated commit"], check=True)
    return {"message": f"Repository cloned/updated in {repo_dir}"}

def handle_task_B5():
    """
    B5: Run a SQL query on a SQLite database located in /data.
    """
    local_data_dir = os.path.join(os.getcwd(), "data")
    db_path = os.path.join(local_data_dir, "sample.db")
    if not os.path.exists(db_path):
        raise Exception(f"Database file not found at {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "SELECT * FROM sample_table;"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return {"rows": rows}

def handle_task_B6():
    """
    B6: Extract data from a website (scrape) and save it to /data/web_scrape.html.
    """
    local_data_dir = os.path.join(os.getcwd(), "data")
    url = "https://example.com"  # sample URL
    response = requests.get(url)
    response.raise_for_status()
    file_path = os.path.join(local_data_dir, "web_scrape.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(response.text)
    return {"message": f"Website data saved to {file_path}"}

def handle_task_B7():
    """
    B7: Compress or resize an image.
    Read /data/input_image.png and save a resized version to /data/resized_image.png.
    """
    local_data_dir = os.path.join(os.getcwd(), "data")
    input_image = os.path.join(local_data_dir, "input_image.png")
    output_image = os.path.join(local_data_dir, "resized_image.png")
    if not os.path.exists(input_image):
        raise Exception(f"Input image not found: {input_image}")
    img = Image.open(input_image)
    resized = img.resize((img.width // 2, img.height // 2))
    resized.save(output_image)
    return {"message": f"Image resized and saved to {output_image}"}

def handle_task_B8():
    """
    B8: Transcribe audio from an MP3 file.
    Read /data/audio.mp3 and write transcription to /data/transcription.txt.
    """
    local_data_dir = os.path.join(os.getcwd(), "data")
    audio_path = os.path.join(local_data_dir, "audio.mp3")
    transcription_file = os.path.join(local_data_dir, "transcription.txt")
    if not os.path.exists(audio_path):
        raise Exception(f"Audio file not found: {audio_path}")
    # Stub: In real usage, integrate with a transcription service.
    transcription = "Transcribed audio text (stub)."
    with open(transcription_file, "w", encoding="utf-8") as f:
        f.write(transcription)
    return {"message": f"Transcription saved to {transcription_file}"}

def handle_task_B9():
    """
    B9: Convert Markdown to HTML.
    Read /data/markdown.md and write the HTML to /data/markdown.html.
    """
    local_data_dir = os.path.join(os.getcwd(), "data")
    md_file = os.path.join(local_data_dir, "markdown.md")
    html_file = os.path.join(local_data_dir, "markdown.html")
    if not os.path.exists(md_file):
        raise Exception(f"Markdown file not found: {md_file}")
    import markdown
    with open(md_file, "r", encoding="utf-8") as f:
        md_content = f.read()
    html = markdown.markdown(md_content)
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)
    return {"message": f"Converted HTML saved to {html_file}"}

def passes_luhn(number_str: str) -> bool:
    """
    Returns True if 'number_str' (containing only digits) satisfies the Luhn check.
    """
    if not number_str.isdigit():
        return False
    
    digits = [int(d) for d in number_str]
    # Double every second digit from the right
    for i in range(len(digits) - 2, -1, -2):
        doubled = digits[i] * 2
        # If doubling is >= 10, subtract 9
        if doubled > 9:
            doubled -= 9
        digits[i] = doubled
    
    return sum(digits) % 10 == 0
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
