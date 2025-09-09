# Importing Required Libraries
import traceback
import sys
from agent.graph import agent
from agent.tools import init_project_root

# Define function to run the entire pipeline
def run_pipeline(user_prompt: str, recursion_limit: int = 100):
    """
    Run the agent pipeline for a given user prompt.
    Yields logs step by step for Streamlit UI.
    """
    logs = []

    try:
        
        # Initialize the project root directory and create package.json
        init_project_root() 

        logs.append("Analysing prompt...")
        yield {"logs": logs.copy()}

        logs.append("Generating task plan...")
        yield {"logs": logs.copy()}

        logs.append("Breaking down tasks...")
        yield {"logs": logs.copy()}

        logs.append("Starting coding...")
        yield {"logs": logs.copy()}

        logs.append("Creating components...")
        yield {"logs": logs.copy()}

        result = agent.invoke(
            {"user_prompt": user_prompt},
            {"recursion_limit": recursion_limit}
        )

        logs.append("Finalizing code...")
        yield {"logs": logs.copy()}

        # Final completion log
        logs.append("Pipeline finished successfully")
        yield {"logs": logs.copy(), "result": result}

    except KeyboardInterrupt:
        logs.append("Operation cancelled by user.")
        yield {"logs": logs.copy()}
        sys.exit(0)

    except Exception as e:
        logs.append(f"Error: {e}")
        yield {"logs": logs.copy()}
        traceback.print_exc()
        sys.exit(1)