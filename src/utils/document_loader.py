from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma 
from config import KNOWLEDGE_BASE_PATH, VECTOR_DB_PATH, GOOGLE_API_KEY

def load_and_process_documents():
    """Load PDFs and create vector store"""
    loader = DirectoryLoader(
        KNOWLEDGE_BASE_PATH,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader,
        recursive=True,
        show_progress=True
    )
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    texts = text_splitter.split_documents(documents)
    
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GOOGLE_API_KEY
    )
    vectorstore = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH
    )
    
    return vectorstore