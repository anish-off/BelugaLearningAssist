from langgraph.graph import Graph, END
from langgraph.checkpoint.memory import MemorySaver
from nodes.study_plan import generate_study_plan
from nodes.content_retriever import retrieve_content
from nodes.quiz_generator import generate_quiz
from nodes.progress_tracker import track_progress
from typing import Dict, Any

# Define the workflow graph
workflow = Graph()

# Add nodes
workflow.add_node("study_plan", generate_study_plan)
workflow.add_node("content_retriever", retrieve_content)
workflow.add_node("quiz_generator", generate_quiz)
workflow.add_node("progress_tracker", track_progress)

# Define edges
workflow.set_entry_point("study_plan")
workflow.add_edge("study_plan", "content_retriever")
workflow.add_edge("content_retriever", "quiz_generator")
workflow.add_edge("quiz_generator", "progress_tracker")

# Add conditional edge for progress tracking
def should_continue(state: Dict[str, Any]) -> str:
    """Determine if we should continue to next step or end"""
    study_plan = state.get("study_plan", {})
    current_step = state.get("current_step", 0)
    
    # Check if we've completed all steps
    if not study_plan or "steps" not in study_plan:
        return END
    
    total_steps = len(study_plan["steps"])
    if current_step >= total_steps - 1:
        return END
    
    # Otherwise, continue to the next step
    return "content_retriever"

workflow.add_conditional_edges(
    "progress_tracker",
    should_continue,
    {
        "content_retriever": "content_retriever",
        END: END
    }
)

# Compile the graph with memory checkpointer
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

