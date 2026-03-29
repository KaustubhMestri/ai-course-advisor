#!/usr/bin/env python
from course_planning_assistant.crew import CoursePlanningAssistant

def run():
    query = input("🎓 Enter your course planning question:\n> ")
    
    inputs = {"query": query}
    
    print("\n🚀 Running Course Planning Assistant...\n")
    result = CoursePlanningAssistant().crew().kickoff(inputs=inputs)
    
    print("\n" + "="*50)
    print("FINAL PLAN:")
    print("="*50)
    print(result)

if __name__ == "__main__":
    run()