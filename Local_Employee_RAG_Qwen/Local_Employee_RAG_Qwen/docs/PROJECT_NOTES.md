# Project Notes: Local Employee RAG

## Objective
Build a local Q&A assistant that answers employee-data questions from an uploaded CSV and a locally running Qwen model through Ollama.

## Key terms
- **RAG:** Retrieves relevant external records and gives them to an LLM as evidence.
- **Ingestion:** Loading and preparing source records for retrieval.
- **Chunk/record:** A small unit of information that can be retrieved. This demo treats each CSV row as one record.
- **Retrieval:** Finding candidate records relevant to the question.
- **Grounded generation:** Asking the LLM to answer only from retrieved evidence.
- **Source traceability:** Showing the records used to form an answer.
- **Local inference:** Running the model through Ollama on the user's computer rather than calling a hosted LLM API.

## Flow
1. Load CSV records.
2. Convert each row to text.
3. Create a TF-IDF index locally.
4. Search the index for top matching rows, boosting exact employee ID/name matches.
5. Send only the selected evidence plus the question to local Ollama.
6. Display the generated answer and retrieved sources.

## What is deliberately not implemented
This is a small learning prototype, not a 100-million-document platform. It does not have distributed sharding, replication, enterprise access controls, a production vector database, or a separate reranking model.

## Demo checklist
- Ask for the salary of EMP1004 and check the source row.
- Ask for EMP1025's status.
- Ask for a nonexistent ID (EMP9999) and check the model abstains.
- Ask a question not covered by the CSV.
- Explain that source evidence is visible and must be checked if an answer seems incorrect.
