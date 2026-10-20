
import os
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load API key from the .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

APP_TITLE = "Local Employee RAG Assistant"
DATA_FILE = Path(__file__).parent / "data" / "employees.csv"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="👩‍💻",
    layout="wide",
)

st.title("Local Employee RAG Assistant")
st.caption("Employee data retrieval with Gemini Cloud and RAG")

@st.cache_data
def load_employee_data():
    return pd.read_csv(DATA_FILE, dtype={"employee_id": str})

if not DATA_FILE.exists():
    st.error(f"Employee CSV file not found: {DATA_FILE}")
    st.stop()

employees = load_employee_data()

st.success(f"Employee records loaded: {len(employees)}")

with st.expander("View employee dataset"):
    st.dataframe(employees, use_container_width=True)

question = st.text_input(
    "Ask a question about your employee dataset",
    placeholder="Example: What is the department of EMP1004?",
)

def retrieve_employee_context(question, dataframe):
    """Retrieve employee rows using employee IDs or keyword matching."""
    q = question.lower()
    matched = pd.DataFrame()

    # Exact employee ID matching
    for employee_id in dataframe["employee_id"].astype(str):
        if employee_id.lower() in q:
            matched = dataframe[
                dataframe["employee_id"].astype(str).str.lower()
                == employee_id.lower()
            ]
            break

    # Match employee names mentioned in the question
    if matched.empty and "name" in dataframe.columns:
        for name in dataframe["name"].dropna().astype(str):
            if name.lower() in q:
                matched = dataframe[
                    dataframe["name"].astype(str).str.lower()
                    == name.lower()
                ]
                break

    # Match a department, designation, or office location
    if matched.empty:
        searchable_columns = [
            col for col in [
                "department",
                "designation",
                "office_location",
                "employment_status",
            ]
            if col in dataframe.columns
        ]

        for column in searchable_columns:
            for value in dataframe[column].dropna().astype(str).unique():
                if value.lower() in q:
                    matched = dataframe[
                        dataframe[column].astype(str).str.lower()
                        == value.lower()
                    ]
                    break
            if not matched.empty:
                break

    # For broad questions, provide the complete dataset as context
    if matched.empty:
        matched = dataframe

    return matched

if question:
    if not GEMINI_API_KEY:
        st.error(
            "Gemini API key not found. Check the .env file "
            "in the same folder as app.py."
        )
        st.stop()

    context_df = retrieve_employee_context(question, employees)
    context = context_df.to_csv(index=False)

    prompt = f"""
You are an employee-data assistant using Retrieval-Augmented Generation (RAG).

Rules:
1. Answer using ONLY the employee data supplied below.
2. Never invent employee details, salaries, or dates.
3. If the data does not contain the answer, clearly say that
   the information is not available in the supplied employee data.
4. Keep the answer simple and direct.

Retrieved employee data:
{context}

User question:
{question}

Answer:
"""

    with st.spinner("Gemini is checking the retrieved employee data..."):
        try:
            client = genai.Client(api_key=GEMINI_API_KEY)

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )

            st.subheader("Answer")
            st.write(response.text or "No answer was returned.")

            st.subheader("Retrieved source records")
            st.dataframe(context_df, use_container_width=True)

        except Exception as error:
            st.error(f"Gemini API error: {error}")
            st.info(
                "Check your API key, internet connection, "
                "model availability, and API quota."
            )
