from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma  # Updated import
from typing import Dict, Any, List
from config import VECTOR_DB_PATH, GOOGLE_API_KEY

def retrieve_content(state: Dict[str, Any]) -> Dict[str, Any]:
    """Retrieve relevant content for the current learning step"""
    topic = state.get("topic", "")
    study_plan = state.get("study_plan", {})
    current_step = state.get("current_step", 0)
    
    if not study_plan or "steps" not in study_plan:
        return {**state, "content": "No study plan available"}
    
    # Get concepts for current step
    step_concepts = study_plan["steps"][current_step].get("concepts", [])
    query = f"{topic}: {', '.join(step_concepts)}"
    
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GOOGLE_API_KEY
    )
    vectorstore = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(query)
    
    return {
        **state,
        "content": "\n\n".join([doc.page_content for doc in docs])
    }