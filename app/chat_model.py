import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

load_dotenv()

if os.getenv("GOOGLE_API_KEY"):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

    embedding_model = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004"
    )

else:
    raise ValueError("Neither GOOGLE_API_KEY nor GROQ_API_KEY found in .env")
