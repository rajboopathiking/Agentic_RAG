# Agentic_RAG
**Agentic RAG (Retrieval-Augmented Generation with Agents)** is an evolution of traditional RAG systems.
Instead of a single static retrieve-then-answer pipeline, an LLM acts as an agent that can reason about what information it needs, decide actions, and iteratively refine retrieval and answers.

### Fork Repo :
    ```bash
    git clone <repo>
    ```
### STEPS :

**move to directory** : 
```bash
  cd Agentic_RAG
```

**note : if you donot have UV install it or use Python virtual environment**

**create virtual environmen and install dependencies**
```bash
uv venv rag
uv pip install -r requirements
```

***To Start Server***

```bash
uv run app/main.py
```

### click on the url the **/docs** for swagger UI 

### API Documentation:

**/upload_pdf** - To upload PDF Documents Which is Need for RAG
**/build_db** - To Build a Chroma Database in ***./chroma_db*** and collection_name - ***"agentic_rag_collection"***
**/query** - To Get Agentic RAG response


