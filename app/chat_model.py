import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()

google_key = os.getenv("GOOGLE_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

if google_key:
    os.environ["GOOGLE_API_KEY"] = google_key

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

    embedding_model = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004"
    )

elif openai_key:
    os.environ["OPENAI_API_KEY"] = openai_key
    
    llm = ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0
    )

    embedding_model = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

else:
    raise ValueError("Neither GOOGLE_API_KEY nor OPENAI_API_KEY found in .env")
