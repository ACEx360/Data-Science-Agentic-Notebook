# DataScience AI Agent with Smart Notebook Interface

A minimal working prototype of a Data Science AI Agent that combines a chat interface with a persistent notebook-style execution environment.

## Features

- **Smart Notebook Interface**: Combines chat and code execution.
- **Persistent State**: Variables and DataFrames are preserved across executions.
- **AI-Powered**: Uses Google Gemini Pro via LangChain and LangGraph to generate code.
- **Auto-Visualization**: Automatically displays plots and outputs.
- **History Tracking**: All execution history is saved to a local SQLite database.

## Prerequisites

- Python 3.8+
- Google Gemini API Key
- uv

## Installation

1. Clone the repository or navigate to the project folder.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   recommended :
      ```bash
   uv sync
   ```
4. Set up your Google API Key:
   - Create a `.env` file in the root directory.
   - Add your key:
     ```
     GOOGLE_API_KEY=ye_gareeb_ki
     ```

## Running the Application

1. Run the Streamlit app:
   ```bash
   python run.py
   ```
2. Open your browser at `http://localhost:8501`.

## Usage

1. **Chat**: Type natural language queries in the right panel (e.g., "Load a sample dataframe", "Plot column A vs B").
2. **Execute**: The agent will generate Python code and execute it.
3. **View**: The left panel shows the history of executed code and outputs.


