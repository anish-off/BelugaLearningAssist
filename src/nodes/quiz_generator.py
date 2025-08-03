from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Dict, Any, List
from utils.prompts import QUIZ_PROMPT
from config import LLM_MODEL, LLM_TEMPERATURE, GOOGLE_API_KEY

class QuizQuestion(BaseModel):
    question: str = Field(description="Question text")
    options: Dict[str, str] = Field(description="Options as a dictionary")
    correct_answer: str = Field(description="The correct option letter")

class Quiz(BaseModel):
    questions: List[QuizQuestion] = Field(description="List of quiz questions")

def generate_quiz(state: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a quiz on the current topic"""
    topic = state.get("topic", "")
    user_level = state.get("user_level", "beginner")
    
    # Map user level to difficulty
    difficulty_map = {
        "beginner": "easy",
        "intermediate": "medium",
        "advanced": "hard"
    }
    difficulty = difficulty_map.get(user_level, "medium")
    
    llm = ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        google_api_key=GOOGLE_API_KEY
    )
    parser = PydanticOutputParser(pydantic_object=Quiz)
    
    chain = QUIZ_PROMPT | llm | parser
    
    result = chain.invoke({"topic": topic, "difficulty": difficulty})
    
    return {
        **state,
        "quiz": result.dict()
    }