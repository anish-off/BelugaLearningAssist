import os
import datetime
from dotenv import load_dotenv
from graph import app

load_dotenv()

def main():
    print("🎓 Personal Learning Assistant")
    print("=" * 40)
    
    # Get user input
    topic = input("What topic would you like to learn? ")
    user_level = input("What's your level? (beginner/intermediate/advanced) ")
    user_id = input("Enter your user ID: ")
    
    # Prepare input
    inputs = {
        "topic": topic,
        "user_level": user_level,
        "user_id": user_id,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    # Create config for thread
    config = {"configurable": {"thread_id": user_id}}
    
    print("\n🚀 Generating your personalized learning plan...")
    
    # Run the workflow without recursion limit
    result = app.invoke(inputs, config)
    
    # Display results
    print("\n📚 Your Learning Plan:")
    if "study_plan" in result and "steps" in result["study_plan"]:
        for step in result["study_plan"]["steps"]:
            print(f"\nStep {step['step']}: {step['title']}")
            print(f"  Concepts: {', '.join(step['concepts'])}")
            print(f"  Activities: {', '.join(step['activities'])}")
            print(f"  Time: {step['time_estimate']}")
    
    if "content" in result:
        print("\n📖 Learning Content:")
        print(result["content"][:500] + "..." if len(result["content"]) > 500 else result["content"])
    
    if "quiz" in result and "questions" in result["quiz"]:
        print("\n📝 Practice Quiz:")
        for i, q in enumerate(result["quiz"]["questions"], 1):
            print(f"\nQ{i}: {q['question']}")
            for opt, text in q["options"].items():
                print(f"  {opt}: {text}")
            print(f"  Answer: {q['correct_answer']}")
    
    if "progress" in result:
        print("\n📊 Progress:")
        print(f"  Completed steps: {result['progress'].get('completed_steps', [])}")
        print(f"  Current step: {result['progress'].get('current_step', 0)}")

if __name__ == "__main__":
    main()