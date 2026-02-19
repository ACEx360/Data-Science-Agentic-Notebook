import os
import sys

def main():
    """Runs the Streamlit application."""
    print("Starting Smart Notebook Agent...")
    # Using 'streamlit run' command
    os.system("streamlit run src/ui/app.py")

if __name__ == "__main__":
    main()
