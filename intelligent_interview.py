#!/usr/bin/env python3
"""
Intelligent Interview Orchestration System using CrewAI
This script uses a multi-agent system to:
1. Generate interview questions for different domains (Soft Skills, Technical).
2. Analyze the generated questions to create a comprehensive candidate report.
This version configures the LLM directly on the agents to ensure correct provider usage.
"""

import os
import sys
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

# Load environment variables from .env file
load_dotenv()

# Ensure the Google API key is available
if not os.getenv('GOOGLE_API_KEY'):
    print("❌ Error: GOOGLE_API_KEY not found in environment variables.")
    print("Please set it in your .env file.")
    sys.exit(1)
else:
    print("✅ GOOGLE_API_KEY found.")

# Define the model to be used by the agents
GEMINI_MODEL = 'gemini/gemini-pro'

# --- Agent Definitions ---
def create_interview_crew(candidate_name, candidate_role):
    """Creates and configures the interview crew."""

    # Agent 1: Soft Skills and Behavioral Interviewer
    soft_skills_agent = Agent(
        role="Soft Skills and Communication Assessment Specialist",
        goal=f"Generate 5 insightful soft skills questions for {candidate_name} to evaluate communication, teamwork, and adaptability for the {candidate_role} position.",
        backstory=(
            "You are a senior HR professional specializing in organizational psychology. "
            "You craft questions that reveal a candidate's true character and interpersonal skills."
        ),
        llm=GEMINI_MODEL,
        verbose=True,
        allow_delegation=False
    )

    # Agent 2: Technical and Coding Interviewer
    coding_agent = Agent(
        role="Technical and Coding Assessment Specialist",
        goal=f"Generate 5 challenging technical and coding questions for {candidate_name} to evaluate their programming skills, algorithms, and data structures knowledge for the {candidate_role} position.",
        backstory=(
            "You are a senior software architect with a passion for identifying top technical talent. "
            "Your questions are designed to test not just what a candidate knows, but how they think and solve problems."
        ),
        llm=GEMINI_MODEL,
        verbose=True,
        allow_delegation=False
    )

    # Agent 3: Report Generator
    report_generator_agent = Agent(
        role="Performance Analyst and Report Generator",
        goal=f"Analyze the interview questions provided for {candidate_name} and generate a comprehensive performance report. The report must include a rating out of 10 and personalized skill improvement suggestions.",
        backstory=(
            "You are an AI-powered performance analyst. You take in the full context of an interview "
            "(in this case, the questions asked) and produce an objective, data-driven performance "
            "report. Your analysis synthesizes all available information into a final rating and "
            "actionable feedback for the candidate."
        ),
        llm=GEMINI_MODEL,
        verbose=True,
        allow_delegation=False
    )

    # --- Task Definitions ---

    # Task 1: Generate Soft Skills Questions
    soft_skills_task = Task(
        description=f"Generate 5 soft skills questions for {candidate_name}, a candidate for the {candidate_role} role.",
        expected_output="A numbered list of 5 questions.",
        agent=soft_skills_agent
    )

    # Task 2: Generate Technical Questions
    coding_task = Task(
        description=f"Generate 5 technical questions for {candidate_name}, a candidate for the {candidate_role} role.",
        expected_output="A numbered list of 5 questions, including at least one coding challenge.",
        agent=coding_agent
    )

    # Task 3: Generate the Final Report
    report_task = Task(
        description=(
            "Review and analyze the collected interview questions (soft skills and technical) "
            f"for the candidate, {candidate_name}. Based on this information, create a final performance report."
        ),
        expected_output=(
            "A comprehensive report formatted in Markdown. It must contain:\n"
            "1. A brief introduction.\n"
            "2. A summary of the candidate's presumed strengths based on the topics covered.\n"
            "3. A final performance rating on a scale of 1 to 10.\n"
            "4. A section with personalized, actionable suggestions for skill improvement."
        ),
        context=[soft_skills_task, coding_task],
        agent=report_generator_agent
    )

    # --- Crew Assembly ---
    interview_crew = Crew(
        agents=[soft_skills_agent, coding_agent, report_generator_agent],
        tasks=[soft_skills_task, coding_task, report_task],
        process=Process.sequential,
        verbose=True
    )

    return interview_crew

# --- Main Execution ---
if __name__ == "__main__":
    candidate_name = "John Doe"
    candidate_role = "Senior Python Developer"

    print(f"🚀 Starting Interview Orchestration for {candidate_name} ({candidate_role})...")
    print("="*60)

    try:
        # Create and run the interview crew
        interview_crew = create_interview_crew(candidate_name, candidate_role)
        result = interview_crew.kickoff()

        print("\n\n✅ Interview Orchestration Completed!")
        print("="*60)
        print("Final Report:")
        print(result)

    except Exception as e:
        print(f"\n❌ An error occurred during the interview process: {e}")
        import traceback
        traceback.print_exc()
