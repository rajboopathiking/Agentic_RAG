
from Orchestration import app as orchestration_app
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi import UploadFile, File, HTTPException,FastAPI, status
import os
import shutil
import uuid

FILES_DIR = "./app/files"
os.makedirs(FILES_DIR, exist_ok=True)

print(os.getcwd())


if os.path.exists(FILES_DIR) is False:
    os.makedirs(FILES_DIR, exist_ok=True)

class QueryRequest(BaseModel):
    query: str = Field(..., json_schema_extra={"example": "What is the capital of France?"})

app = FastAPI(title="Agentic RAG API")

@app.get("/")
async def root():
    return {"message": "Welcome to the Agentic RAG API"}

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files allowed")

    new_filename = f"{uuid.uuid4()}.pdf"
    file_path = os.path.join(FILES_DIR, new_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "detail": "File uploaded successfully",
        "saved_as": new_filename
    }


@app.post("/build_db")
async def build_database():

    from DB_Builder import DBBuilder
    db_builder = DBBuilder()
    result = db_builder.build_db()
    return {"detail": "Database built successfully", "db_info": result}


@app.post("/query")
async def handle_query(request: QueryRequest):
    state = {
        "query": request.query,
        "rag_docs": [],
        "web_docs": [],
        "answer": None,
        "confidence": 0.0
    }

    try:
        config = {"configurable": {"thread_id":"1"}}
        final_state = orchestration_app.invoke(state, config=config)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
   

    return final_state


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)