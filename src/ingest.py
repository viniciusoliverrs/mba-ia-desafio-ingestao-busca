import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME", )

def get_embeddings_model():
    if os.getenv("OPENAI_API_KEY"):
        return OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL"))
    elif os.getenv("GOOGLE_API_KEY"):
        return GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL"))
    else:
        raise ValueError("Nenhuma API Key encontrada (OPENAI ou GOOGLE). Verifique o arquivo .env")

def ingest_pdf():
    print(f"Iniciando ingestão do arquivo: {PDF_PATH}")
    
    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f"Arquivo não encontrado: {PDF_PATH}")
        
    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()
    print(f"Carregado {len(docs)} páginas.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    splits = text_splitter.split_documents(docs)
    print(f"Dividido em {len(splits)} chunks.")

    embeddings = get_embeddings_model()
    
    print("Conectando ao banco de dados e salvando vetores...")
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=DATABASE_URL,
        use_jsonb=True,
    )
    
    vector_store.add_documents(splits)
    print("Ingestão concluída com sucesso!")

if __name__ == "__main__":
    ingest_pdf()