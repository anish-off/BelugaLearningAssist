from langchain_core.prompts import ChatPromptTemplate

STUDY_PLAN_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an expert educational curriculum designer. Create structured, personalized learning plans."),
    ("human", """
    Create a 5-step study plan for learning {topic} at a {user_level} level.
    Each step should include:
    - Key concepts to learn
    - Suggested activities
    - Estimated time to complete
    
    Return the plan as a JSON object with this structure:
    {{
        "steps": [
            {{
                "step": 1,
                "title": "Step title",
                "concepts": ["concept1", "concept2"],
                "activities": ["activity1", "activity2"],
                "time_estimate": "X hours"
            }}
        ]
    }}
    """)
])

QUIZ_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are an expert educator. Create challenging but fair multiple-choice questions."),
    ("human", """
    Generate 3 multiple-choice questions about {topic} at {difficulty} difficulty.
    Each question should have 4 options (A, B, C, D) with one correct answer.
    
    Return as JSON:
    {{
        "questions": [
            {{
                "question": "Question text",
                "options": {{
                    "A": "Option A",
                    "B": "Option B",
                    "C": "Option C",
                    "D": "Option D"
                }},
                "correct_answer": "A"
            }}
        ]
    }}
    """)
])