# Importing Required Packages
import time
import streamlit as st
import os
from main_app import run_pipeline

# Setting the Configurations
GENERATED_CODE_DIR = "generated_project/src"
APP_FILE = os.path.join(GENERATED_CODE_DIR, "App.jsx")
COMPONENTS_DIR = os.path.join(GENERATED_CODE_DIR, "components")

# Setting the Streamlit UI
st.set_page_config(page_title = "AI Website Builder", layout = "wide")
st.title("AI Website Builder")

# User Input Section
user_prompt = st.text_input(
    "Enter your app idea:", 
    placeholder = "e.g. Create a search bar with React + Tailwind CSS"
)

# Generate button placed right under the input
generate_clicked = st.button("Generate Website")

# Layout of the Streamlit App
col1, col2 = st.columns([1,2])

# Creating the Log Section
with col1:
    st.header("Live Logs")
    log_placeholder = st.empty()

# Code/Design Display Section
with col2:
    tab_code, tab_design = st.tabs(["Code", "Website Preview"])
    code_placeholder = tab_code.empty()
    design_placeholder = tab_design.empty()

# Store the logs to show
logs = [
    "Analysing prompt...", 
    "Generating task plan...", 
    "Breaking down tasks...", 
    "Starting coding...", 
    "Creating components...", 
    "Finalizing code..."
]

# Define the Actions on Button Click
if generate_clicked:
    if not user_prompt:
        st.warning("Please enter an app idea.")
    else:
        # Collect logs and display them
        collected_logs = []
        
        for log in run_pipeline(user_prompt):
            collected_logs.append(log["logs"][-1])
            log_placeholder.markdown("<br>".join(collected_logs), unsafe_allow_html = True) # "<br>".join(collected_logs), unsafe_allow_html=True |  "\n".join(collected_logs)
            time.sleep(3)

        # Load generated code if exists
        code_output = ""
        
        if os.path.exists(COMPONENTS_DIR):
            for filename in os.listdir(COMPONENTS_DIR):
                if filename.endswith(".jsx"):
                    fpath = os.path.join(COMPONENTS_DIR, filename)
                    with open(fpath, "r", encoding = "utf-8") as f:
                        code_output += f"// Component/{filename}\n{f.read()}\n\n"
        
        if os.path.exists(APP_FILE):
            with open(APP_FILE, "r", encoding = "utf-8") as f:
                code_output += f"// App.jsx\n{f.read()}\n\n"

        if code_output:
            code_placeholder.code(code_output, language = "javascript")
        else:
            code_placeholder.warning("No code files found in generated_project/src.")

        # Render Design Preview
        design_placeholder.markdown(
            """
            <iframe src="http://localhost:5173" width="100%" height="500" style="border:none;">
            </iframe>
            """,
            unsafe_allow_html=True
        )