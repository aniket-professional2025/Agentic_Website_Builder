# Importing necessary libraries
import pathlib
import subprocess
from typing import Tuple
from langchain_core.tools import tool

# Defining the project root directory
PROJECT_ROOT = pathlib.Path.cwd() / "generated_project"

# Utility function to ensure safe file paths within the project root
def safe_path_for_project(path: str) -> pathlib.Path:
    p = (PROJECT_ROOT / path).resolve()
    if PROJECT_ROOT.resolve() not in p.parents and PROJECT_ROOT.resolve() != p.parent and PROJECT_ROOT.resolve() != p:
        raise ValueError("Attempt to write outside project root")
    return p

# Defining tool functions for file operations and command execution: write_file
@tool
def write_file(path: str, content: str) -> str:
    """Writes content to a file at the specified path within the project root."""
    p = safe_path_for_project(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding = "utf-8") as f:
        f.write(content)
    return f"WROTE:{p}"

# Defining tool functions for file operations and command execution: read_file
@tool
def read_file(path: str) -> str:
    """Reads content from a file at the specified path within the project root."""
    p = safe_path_for_project(path)
    if not p.exists():
        return ""
    with open(p, "r", encoding = "utf-8") as f:
        return f.read()

# Defining tool functions for file operations and command execution: get_current_directory
@tool
def get_current_directory() -> str:
    """Returns the current working directory."""
    return str(PROJECT_ROOT)

# Defining tool functions for file operations and command execution: list_files
@tool
def list_files(directory: str = ".") -> str:
    """Lists all files in the specified directory within the project root."""
    p = safe_path_for_project(directory)
    if not p.is_dir():
        return f"ERROR: {p} is not a directory"
    files = [str(f.relative_to(PROJECT_ROOT)) for f in p.glob("**/*") if f.is_file()]
    return "\n".join(files) if files else "No files found."

# Defining tool functions for file operations and command execution: run_cmd
@tool
def run_cmd(cmd: str, cwd: str = None, timeout: int = 30) -> Tuple[int, str, str]:
    """Runs a shell command in the specified directory and returns the result."""
    cwd_dir = safe_path_for_project(cwd) if cwd else PROJECT_ROOT
    res = subprocess.run(cmd, shell = True, cwd = str(cwd_dir), capture_output = True, text = True, timeout = timeout)
    return res.returncode, res.stdout, res.stderr

# Function to initialize the project root directory
def init_project_root():
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)

    # Write a minimal package.json if it doesn't exist
    pkg_file = PROJECT_ROOT / "package.json"
    if not pkg_file.exists():
        pkg_file.write_text("""{
                                "name": "generated-app",
                                "version": "1.0.0",
                                "scripts": {
                                    "dev": "vite",
                                    "build": "vite build",
                                    "preview": "vite preview"
                                    },
                                "dependencies": {
                                    "react": "^18.2.0",
                                    "react-dom": "^18.2.0"
                                },
                                "devDependencies": {
                                    "vite": "^4.0.0",
                                    "tailwindcss": "^3.3.0",
                                    "autoprefixer": "^10.4.0",
                                    "postcss": "^8.4.0"
                                }
                    }
""", encoding="utf-8")
    
    # Write a minimal index.html if it doesn't exist
    index_file = PROJECT_ROOT / "index.html"
    if not index_file.exists():
        index_file.write_text("""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Vite + React App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/App.jsx"></script>
  </body>
</html>
""", encoding="utf-8")

    return str(PROJECT_ROOT)