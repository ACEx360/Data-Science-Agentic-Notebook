import streamlit as st
import pandas as pd
import json
import sqlite3
import sys
import os

# Add project root to sys.path so we can import from src
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.agent.graph import app as agent_app
from src.core.shared import set_global_executor
from src.core.database import init_db, get_history, add_cell
from src.core.executor import CodeExecutor

# Initialize DB on first run
init_db()

st.set_page_config(layout="wide", page_title="Smart Notebook Agent")

st.title("DataScience AI Agent with Smart Notebook Interface")

# Initialize shared CodeExecutor in session state
if "code_executor" not in st.session_state:
    st.session_state.code_executor = CodeExecutor()

# Set the global executor for the agent to use
set_global_executor(st.session_state.code_executor)

# Custom CSS for that "Premium" look
st.markdown("""
<style>
    /* Chat message container */
    [data-testid="stChatMessage"] {
        background-color: #000000 !important;
        color: #ffffff !important;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
    }

    /* Chat text */
    [data-testid="stChatMessage"] p {
        color: #ffffff !important;
    }

    /* Optional: darker chat input */
    [data-testid="stChatInput"] textarea {
        background-color: #1e1e1e !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)


# Layout: 70% Notebook, 30% Chat
col1, col2 = st.columns([7, 3])

# Notebook Interface
if "cells" not in st.session_state:
    # Load history from DB on first load
    history = get_history()
    st.session_state.cells = []
    if history:
        for row in history:
            # row: id, code, output, variables, timestamp
            st.session_state.cells.append({
                "code": row[1],
                "output": row[2],
                "status": "executed",
                "variables": json.loads(row[3]) if row[3] else {}
            })
    else:
        # Start with one empty cell if no history
        st.session_state.cells.append({"code": "", "output": "", "status": "idle", "variables": {}})

def run_cell(index):
    cell = st.session_state.cells[index]
    code = cell["code"]
    if code.strip():
        try:
            result = st.session_state.code_executor.execute(code)
            cell["output"] = result["output"]
            cell["variables"] = result["variables"]
            cell["status"] = "executed"
            # Save to DB
            add_cell(code, result["output"], result["variables"])
        except Exception as e:
            cell["output"] = str(e)
            cell["status"] = "error"

def delete_cell(index):
    if 0 <= index < len(st.session_state.cells):
        del st.session_state.cells[index]


def add_new_cell():
    st.session_state.cells.append({"code": "", "output": "", "status": "idle", "variables": {}})

# Left Column: Interactive Notebook
with col1:
    st.header("Interactive Notebook")
    
    for i, cell in enumerate(st.session_state.cells):
     with st.container():

        header_col1, header_col2 = st.columns([9, 1])

        with header_col1:
            st.markdown(f"### Cell {i+1}")

        with header_col2:
            if st.button("🗑️", key=f"delete_{i}"):
                delete_cell(i)
                st.rerun()

        cell_code = st.text_area(
            label="",
            value=cell["code"],
            height=200,
            key=f"code_{i}"
        )

        st.session_state.cells[i]["code"] = cell_code

        btn_col1, btn_col2 = st.columns([1, 4])

        with btn_col1:
            if st.button("Run", key=f"run_{i}"):
                run_cell(i)
                st.rerun()

        with btn_col2:
            if cell["status"] == "executed":
                st.success("Executed", icon="✅")
            elif cell["status"] == "error":
                st.error("Error", icon="❌")

        if cell["output"]:
            st.markdown("**Output:**")
            st.markdown(
                f'<div class="output-cell">{cell["output"]}</div>',
                unsafe_allow_html=True
            )

        if cell.get("variables"):
            with st.expander("Variables"):
                st.json(cell["variables"])

        st.markdown("---")


    # Add Cell Button
    if st.button("Measured + Add Cell"):
        add_new_cell()
        st.rerun()

# Right Column: Chat Interface
with col2:
    st.header("AI Assistant")
    
    # Maintain chat history in session state for the UI
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Ask me to do something with data..."):
        # Add user message to state
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Invoke Agent
        with st.spinner("Agent is planning and executing..."):
            try:
                # Prepare input for LangGraph
                # We simply pass the chat history or just the latest message?
                # The agent expects "messages".
                # Let's pass the list of strings (content only) for simplicity as expected by planner_node
                input_messages = [msg["content"] for msg in st.session_state.messages if msg["role"] == "user"]
                
                # Invoke
                result = agent_app.invoke({"messages": input_messages})
                
                # Result contains 'output' and 'code' from the state
                generated_code = result.get("code", "")
                execution_output = result.get("output", "")
                
                # Add assistant response (summary of what happened)
                response_content = f"Executed successfully.\nOutput:\n{execution_output}"
                
                st.session_state.messages.append({"role": "assistant", "content": response_content})
                with st.chat_message("assistant"):
                    st.markdown(response_content)
                
                # Add to notebook state so it appears on the left
                if generated_code:
                    st.session_state.cells.append({
                        "code": generated_code,
                        "output": execution_output,
                        "status": "executed",
                        "variables": {} # We could fetch variables if passed back, but 'result' might not have them in this version of agent output.
                    })

                # Rerun to update the Notebook History on the left
                st.rerun()
                
            except Exception as e:
                st.error(f"Error executing agent: {e}")
