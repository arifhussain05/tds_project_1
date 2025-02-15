import os
from urllib.parse import urlparse

def install_uv_and_run_datagen(user_email: str = None,url: str = None):
    """
    Install 'uv', download and execute datagen.py.
    """
    print(f"User email: {user_email}")
    if not user_email:
        user_email = "22ds2000091@ds.study.iitm.ac.in"
    print(f"URL: {url}")
    if not url:
        url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
    
    file_name = os.path.basename(urlparse(url).path)
    file_path = os.path.join(u)

    # Ensure DATA_DIR exists

    os.path('/data/').mkdir(parents=True, exist_ok=True)

    # Install 'uv' if not already installed
    try:
        subprocess.run(["uv", "--version"], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        subprocess.run(["python", "-m", "pip", "install", "uv"], check=True)

    # Install 'requests' if needed
    subprocess.run(["python", "-m", "pip", "install", "requests"], check=True)

    # Download datagen.py using requests
    # url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        file_path = file_path
        print(f"Downloaded datagen.py to {file_path}")
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"datagen.py successfully downloaded to {file_path}")
    except requests.RequestException as e:
        raise ValueError(f"Failed to download datagen.py: {e}")

    # Run datagen.py using uv
    try:
        subprocess.run(["uv", "run", str(file_path), user_email, "--root", DATA_DIR], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to execute datagen.py: {e}")

    return f"A1 Completed: datagen.py executed with email {user_email}"

install_uv_and_run_datagen("22ds2000091@ds.study.iitm.ac.in","https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py")