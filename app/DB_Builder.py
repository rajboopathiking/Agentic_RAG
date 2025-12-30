from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from typing import List

from chat_model import embedding_model
import os 

pdf_dir = "./app/files"
pdf_path_list = [
    os.path.join(pdf_dir, f)
    for f in os.listdir(pdf_dir)
    if f.lower().endswith(".pdf")
]


class DBBuilder:
    def __init__(self, persist_directory: str = "./chroma_db",
                collection_name: str = "agentic_rag_collection", 
                pdf_path_list: List[str] = pdf_path_list ,
                Batch_size : int =10,
                embedding_model=embedding_model):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        self.pdf_path_list = pdf_path_list
        self.db = Chroma(persist_directory=self.persist_directory, collection_name=self.collection_name, embedding_function=self.embedding_model)
        self.Batch_size = Batch_size

    def split_documents(self, documents):
        spilter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=20,
            separators=["\n\n", "\n", " ", ""]
        )
        return spilter.split_documents(documents)

    def load_spilt_documents(self):
        all_documents = []
        for pdf_path in self.pdf_path_list:
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            all_documents.extend(documents)
        
        return self.split_documents(all_documents)
    
    def build_db(self):
        spilt_docs = self.load_spilt_documents()
        from tqdm.auto import tqdm

        n_docs = len(spilt_docs)

        for start in tqdm(range(0, n_docs, self.Batch_size)):
            end = min(start + self.Batch_size, n_docs)
            batch = spilt_docs[start:end]

            try:
                self.db.add_documents(batch)
                print(f"Processed documents {start} to {end - 1}")
            except Exception as e:
                print(f"Failed batch {start}–{end-1}: {e}")
                pass

        return "DB Created Successfully"
    
    def load_db(self):
        self.db = Chroma(persist_directory=self.persist_directory, collection_name=self.collection_name, embedding_function=self.embedding_model)
        return self.db

        


        
    
    
