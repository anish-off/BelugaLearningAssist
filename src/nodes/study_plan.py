from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from utils.prompts import STUDY_PLAN_PROMPT
from config import LLM_MODEL, LLM_TEMPERATURE, GOOGLE_API_KEY

class StudyStep(BaseModel):
    step: int = Field(description="Step number")
    title: str = Field(description="Step title")
    concepts: List[str] = Field(description="Key concepts to learn")
    activities: List[str] = Field(description="Suggested activities")
    time_estimate: str = Field(description="Time estimate")

class StudyPlan(BaseModel):
    steps: List[StudyStep] = Field(description="Study plan steps")

def generate_study_plan(state: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a personalized study plan"""
    topic = state.get("topic", "")
    user_level = state.get("user_level", "beginner")
    
    llm = ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        google_api_key=GOOGLE_API_KEY
    )
    parser = PydanticOutputParser(pydantic_object=StudyPlan)
    
    chain = STUDY_PLAN_PROMPT | llm | parser
    
    result = chain.invoke({"topic": topic, "user_level": user_level})
    
    return {
        **state,
        "study_plan": result.dict(),
        "current_step": 0
    }