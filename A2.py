import subprocess, os

def A2(prettier_version="prettier@3.4.2", filename="data/format.md"):
    directory = "data/"
    filename = "format.md"
    file_path = os.path.join(directory, filename)
    command = [r"C:/Program Files/nodejs/npx.cmd", prettier_version, "--write", file_path]
    try:
        subprocess.run(command, check=True)
        print("Prettier executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
if __name__ == "__main__":
    A2(prettier_version="prettier@3.4.2", filename="/data/format.md")