# Local Employee RAG — Qwen + Ollama

A beginner-friendly, local Retrieval-Augmented Generation (RAG) demonstration inspired by the architecture ideas in “Designing RAG for 100 Million Documents”.

## What it demonstrates

- Load employee records from a CSV file (sample records are fictional).
- Build a local TF-IDF retrieval index from the loaded rows.
- Retrieve relevant records for each question, with exact employee ID/name boosts.
- Send only retrieved evidence and the question to a locally running Ollama model.
- Instruct the model to answer only from the evidence and to abstain when information is missing.
- Display the retrieved source rows for verification.
- No cloud LLM API, external search, or hosted vector database is used by the app.

## Important model-name note

“Qwen 3.8B” may mean **Qwen3 8B**. Ollama model tags change, so confirm the available tag on the Ollama library and use the exact tag shown by `ollama list`. The default in this project is `qwen3:8b`; if that tag is unavailable or too large for your laptop, choose a smaller Qwen model and update the sidebar model tag.

## Requirements

- Windows 10/11, macOS, or Linux
- Python 3.10+
- Ollama installed and running
- Enough RAM/disk for your chosen local model

## Windows setup

Open Command Prompt or the VS Code terminal in this project folder.

### 1. Create a virtual environment (recommended)

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

If PowerShell blocks activation, use Command Prompt or run the commands without activating and use `.venv\Scripts\python -m pip ...`.

### 2. Install Python packages

```powershell
python -m pip install -r requirements.txt
```

### 3. Download the local model

```powershell
ollama pull qwen3:8b
```

If that exact tag is not available or your computer cannot run it, check installed/available Qwen tags and select a smaller supported model. Model download needs internet once. The app itself uses the local Ollama API.

### 4. Start the app

```powershell
python -m streamlit run app.py
```

Streamlit should open a browser tab, usually at `http://localhost:8501`.

If Ollama is not already running, open another terminal and run:

```powershell
ollama serve
```

Then verify the installed model with:

```powershell
ollama list
```

## Test questions

Try these using the sample CSV:

- What is the annual salary of EMP1004?
- Which department does EMP1010 work in?
- What is EMP1005's designation?
- Which office location is listed for Kiara Shah?
- What is the employment status of EMP1025?
- What is the salary of EMP9999? (Expected: not found in uploaded data.)

Salary values are sample annual salaries in INR and are not real employee data.

## Uploading your own CSV

Use the sidebar uploader. Required columns:
- `employee_id`
- `name`

Any additional columns are included in the retrieved row text. Keep headers simple and do not upload confidential or personal data unless you are explicitly authorized and have followed your organization's security requirements.

## Architecture

CSV file -> row-to-text conversion -> TF-IDF index -> top-k retrieval -> local Ollama/Qwen -> answer grounded in retrieved rows + visible source records.

## How this relates to large-scale RAG

The project implements the core retrieve-then-generate pattern, source traceability, and local inference. It intentionally does **not** implement a distributed vector database, sharding, replication, reranking models, authentication, or 100-million-document scaling. Those are future production extensions, not features claimed by this prototype.

## Limitations and safety

- TF-IDF is a lightweight lexical baseline, not a semantic embedding model.
- Retrieval can miss relevant rows. The model can still make mistakes, so verify the displayed sources.
- The app sends retrieved records to the local Ollama endpoint configured at `OLLAMA_URL` (default `http://localhost:11434`). Do not point it to a remote endpoint if data must remain local.
- This prototype has no user authentication or role-based access control and is not suitable for real sensitive HR data as-is.
- For confidential production data, add authentication, authorization before retrieval, encryption, audit logging, data-retention controls, tests, and an appropriate secure vector/index store.
