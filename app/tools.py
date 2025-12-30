from langchain_chroma import Chroma
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults
from DB_Builder import DBBuilder
from typing import Any,List,TypedDict,Optional

from chat_model import llm, embedding_model

class State(TypedDict):
    query: str
    rag_docs: List[str]
    web_docs: List[str]
    answer: Optional[str]
    confidence: float


@tool
def retrieve(query:str):
    '''
    Retrieve the Documents From the ChromaDB Vector Store based on Similarity Search
    '''
    from DB_Builder import DBBuilder
    db_builder = DBBuilder()
    vector_store  = db_builder.load_db()

    results = vector_store.similarity_search(query=query)
    docs = []
    for res in results:
        docs.append(res.page_content)
    return {"docs":docs
    }


@tool
def RAG(query: str) -> str:
    """RAG - Retrieval Augmented Generation"""
    docs = retrieve.invoke(query)
    context = docs["docs"]
    
    return context


@tool
def duck_duckgo_search(query:str):
    """
    Web Search Using DuckDuckGO
    """
    search = DuckDuckGoSearchResults(backend="news")
    return search.invoke(query)

def rag_retrieve(state: State):
    result = RAG.invoke(state["query"])
    state["rag_docs"].append(result)
    return state

def evaluate_confidence(state: State):
    docs = state.get("rag_docs", [])

    docs = docs[:3]

    contents = []
    for d in docs:
        if isinstance(d, str):
            text = d
        elif isinstance(d, dict):
            text = d.get("content", "")
        else:
            text = str(d)

        contents.append(text[:2000])

    text = "\n\n".join(contents)

    prompt = f"""
    Based on the following retrieved knowledge, can we confidently answer the query?

    Query: {state['query']}

    Context:
    {text}

    Return ONLY a number between 0 and 1 representing confidence.
    """

    confidence_str = llm.invoke(prompt).content.strip()
    try:
        confidence = float(confidence_str)
    except:
        confidence = 0.4
    state["confidence"] = confidence

    return state

def web_search(state: State):
    results = duck_duckgo_search.invoke(state["query"])
    state["web_docs"].append(results)
    return state

def final_answer(state: State):
    all_sources = state.get("rag_docs", []) + state.get("web_docs", []) or state.get("rag_docs", [])

    merged = []
    for d in all_sources:
        if isinstance(d, str):
            merged.append(d[:2000])
        elif isinstance(d, dict):
            merged.append(d.get("content","")[:2000])
        else:
            merged.append(str(d)[:2000])

    context = "\n\n".join(
        f"Source {i+1}: {t}"
        for i, t in enumerate(merged)
    )

    prompt = f"""
    Answer the question using ONLY the provided sources.
    Be concise. If unknown, say "Not enough information".

    Question:
    {state['query']}

    Sources:
    {context}

    Provide:
    1) Final Answer with Brief Explanation
    2) List of Sources Used
    """

    response = llm.invoke(prompt)

    return {
        **state,
        "answer": response
    }