# Importing necessary libraries
import argparse
import sys
import traceback
from agent.graph import agent

# Defining a main function to handle command-line arguments and run the agent
def main():
    parser = argparse.ArgumentParser(description = "Run engineering project planner")
    parser.add_argument("--recursion-limit", "-r", type = int, default = 100, help = "Recursion limit for processing (default: 100)")

    args = parser.parse_args()

    try:
        user_prompt = input("Enter your project prompt: ")
        result = agent.invoke(
            {"user_prompt": user_prompt},
            {"recursion_limit": args.recursion_limit}
        )
        print("Final State:", result)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        traceback.print_exc()
        print(f"Error: {e}", file = sys.stderr)
        sys.exit(1)

# Inference Block to run the main function
if __name__ == "__main__":
    main()