from typing import Dict, Any
import json
import os
from config import CHECKPOINTER_PATH

def save_progress(user_id: str, progress_data: Dict[str, Any]):
    """Save user progress to file"""
    os.makedirs(CHECKPOINTER_PATH, exist_ok=True)
    file_path = os.path.join(CHECKPOINTER_PATH, f"{user_id}.json")
    
    with open(file_path, 'w') as f:
        json.dump(progress_data, f)

def load_progress(user_id: str) -> Dict[str, Any]:
    """Load user progress from file"""
    file_path = os.path.join(CHECKPOINTER_PATH, f"{user_id}.json")
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return {}

def track_progress(state: Dict[str, Any]) -> Dict[str, Any]:
    """Track and update user progress"""
    user_id = state.get("user_id", "default_user")
    current_step = state.get("current_step", 0)
    study_plan = state.get("study_plan", {})
    
    # Load existing progress
    progress = load_progress(user_id)
    
    # Mark current step as completed
    if "completed_steps" not in progress:
        progress["completed_steps"] = []
    
    if current_step not in progress["completed_steps"]:
        progress["completed_steps"].append(current_step)
    
    # Calculate next step
    total_steps = len(study_plan.get("steps", [])) if study_plan else 0
    next_step = current_step + 1 if current_step < total_steps - 1 else None
    
    # Update progress
    progress["current_step"] = next_step if next_step is not None else current_step
    progress["last_updated"] = str(state.get("timestamp", ""))
    
    # Save progress
    save_progress(user_id, progress)
    
    # Update current_step in state for the next iteration
    if next_step is not None:
        state["current_step"] = next_step
    
    return {
        **state,
        "progress": progress,
        "next_step": next_step
    }