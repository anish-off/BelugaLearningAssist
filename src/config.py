import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/vector_store")
KNOWLEDGE_BASE_PATH = "./data/knowledge_base"

LLM_MODEL = "gemini-1.5-flash"  
LLM_TEMPERATURE = 0.3

CHECKPOINTER_PATH = "./data/checkpoints"