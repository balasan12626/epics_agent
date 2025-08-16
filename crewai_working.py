#!/usr/bin/env python3
"""
Working CrewAI Multi-Agent Interview Question Generator
This version properly configures CrewAI with Gemini 1.5 Flash.
Each agent generates exactly 10 questions.
"""

import os
import time
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# Configure Google Generative AI for CrewAI
try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.7,
        max_tokens=8192,
        convert_system_message_to_human=True,
        top_p=0.9,
        top_k=40,
        google_api_key=os.getenv('GOOGLE_API_KEY')
    )
    print("✅ Successfully initialized Gemini 1.5 Flash model for CrewAI")
    
except Exception as e:
    print(f"❌ Error initializing Gemini 1.5 Flash: {str(e)}")
    # Try alternative model
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.7,
            max_tokens=8192,
            convert_system_message_to_human=True,
            top_p=0.9,
            top_k=40,
            google_api_key=os.getenv('GOOGLE_API_KEY')
        )
        print("✅ Successfully initialized Gemini Pro model for CrewAI")
    except Exception as e2:
        print(f"❌ Error initializing Gemini Pro: {str(e2)}")
        raise

def create_interview_crew(candidate_name, candidate_role):
    """
    Create a comprehensive interview crew with 4 specialized agents.
    Each agent will generate exactly 10 questions.
    """
    
    # Aptitude Assessment Agent
    aptitude_agent = Agent(
        role="Aptitude and Critical Thinking Assessment Specialist",
        goal=f"Generate exactly 10 unique aptitude questions for {candidate_name} to assess problem-solving, logical reasoning, numerical analysis, and critical thinking skills relevant to the {candidate_role} position.",
        backstory=(
            "You are an expert psychometric evaluator with deep knowledge in cognitive assessment. "
            "Your specialty is creating challenging, non-memorizable aptitude questions that reveal true problem-solving abilities. "
            "You analyze role requirements to tailor questions that measure the specific cognitive skills needed for success in the target position."
        ),
        llm=llm, 
        verbose=True, 
        allow_delegation=False
    )

    # Soft Skills and Behavioral Agent
    soft_skills_agent = Agent(
        role="Soft Skills and Communication Assessment Specialist",
        goal=f"Generate exactly 10 insightful soft skills questions for {candidate_name} to evaluate communication, teamwork, leadership, adaptability, and emotional intelligence relevant to the {candidate_role} position.",
        backstory=(
            "You are a senior HR professional with expertise in soft skills assessment and organizational psychology. "
            "You excel at crafting questions that reveal authentic communication patterns and predict workplace success. "
            "Your questions are designed to uncover real examples of interpersonal skills and emotional intelligence."
        ),
        llm=llm, 
        verbose=True, 
        allow_delegation=False
    )

    # Technical and Coding Agent
    coding_agent = Agent(
        role="Technical and Coding Assessment Specialist",
        goal=f"Generate exactly 10 challenging technical and coding questions for {candidate_name} to evaluate programming skills, algorithms, data structures, and system design relevant to the {candidate_role} position.",
        backstory=(
            "You are a senior software architect and technical expert with years of experience in technical hiring. "
            "You specialize in creating questions that test both theoretical knowledge and practical coding skills. "
            "Your questions range from fundamental programming concepts to advanced system design scenarios."
        ),
        llm=llm, 
        verbose=True, 
        allow_delegation=False
    )

    # HR and Cultural Fit Agent
    hr_agent = Agent(
        role="HR and Cultural Fit Assessment Specialist",
        goal=f"Generate exactly 10 HR-focused questions for {candidate_name} to evaluate cultural fit, career motivation, work preferences, and alignment with company values for the {candidate_role} position.",
        backstory=(
            "You are a senior HR manager with expertise in cultural assessment and employee engagement. "
            "You understand how to evaluate whether candidates will thrive in the company culture and contribute positively to the team. "
            "Your questions focus on values alignment, career goals, and work style preferences."
        ),
        llm=llm, 
        verbose=True, 
        allow_delegation=False
    )

    # Define the tasks - Each task generates exactly 10 questions
    aptitude_task = Task(
        description=(
            f"Generate exactly 10 unique aptitude questions for {candidate_name} applying for {candidate_role}. "
            "Questions should cover:\n"
            "- Logical reasoning and deduction\n"
            "- Numerical analysis and problem-solving\n"
            "- Pattern recognition and sequence completion\n"
            "- Critical thinking and analytical skills\n"
            "Make questions challenging but fair, avoiding memorizable patterns. "
            "Format your response as a numbered list from 1 to 10."
        ),
        expected_output="A numbered list of exactly 10 high-quality aptitude questions, each with clear instructions.",
        agent=aptitude_agent
    )

    soft_skills_task = Task(
        description=(
            f"Generate exactly 10 soft skills questions for {candidate_name} applying for {candidate_role}. "
            "Questions should cover:\n"
            "- Communication and presentation skills\n"
            "- Teamwork and collaboration\n"
            "- Leadership and initiative\n"
            "- Adaptability and problem-solving\n"
            "Focus on real-world scenarios and behavioral examples. "
            "Format your response as a numbered list from 1 to 10."
        ),
        expected_output="A numbered list of exactly 10 soft skills questions designed to assess communication and interpersonal abilities.",
        agent=soft_skills_agent
    )

    coding_task = Task(
        description=(
            f"Generate exactly 10 technical and coding questions for {candidate_name} applying for {candidate_role}. "
            "Questions should cover:\n"
            "- Programming fundamentals and best practices\n"
            "- Data structures and algorithms\n"
            "- System design and architecture\n"
            "- Code optimization and debugging\n"
            "Include both theoretical concepts and practical coding scenarios. "
            "Format your response as a numbered list from 1 to 10."
        ),
        expected_output="A numbered list of exactly 10 technical questions with varying difficulty levels.",
        agent=coding_agent
    )

    hr_task = Task(
        description=(
            f"Generate exactly 10 HR questions for {candidate_name} applying for {candidate_role}. "
            "Questions should cover:\n"
            "- Career goals and motivation\n"
            "- Work style and preferences\n"
            "- Cultural fit and values alignment\n"
            "- Professional development and growth\n"
            "Focus on understanding the candidate's long-term fit and potential. "
            "Format your response as a numbered list from 1 to 10."
        ),
        expected_output="A numbered list of exactly 10 HR questions focused on cultural fit and career alignment.",
        agent=hr_agent
    )

    # Create the crew with sequential processing
    interview_crew = Crew(
        agents=[aptitude_agent, soft_skills_agent, coding_agent, hr_agent],
        tasks=[aptitude_task, soft_skills_task, coding_task, hr_task],
        process=Process.sequential,
        verbose=True,
    )

    return interview_crew

def count_questions(text):
    """Count the number of numbered questions in the text."""
    if not text:
        return 0
    
    lines = text.split('\n')
    question_count = 0
    for line in lines:
        line = line.strip()
        if any(line.startswith(f"{i}.") for i in range(1, 11)):
            question_count += 1
    
    return question_count

def run_interview(candidate_name, candidate_role):
    """
    Run the complete interview process using CrewAI and return structured results.
    """
    print(f"\n🚀 Starting CrewAI interview process for {candidate_name} - {candidate_role}")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        # Create and run the crew
        interview_crew = create_interview_crew(candidate_name, candidate_role)
        result = interview_crew.kickoff()
        
        # Extract individual agent outputs
        agent_outputs = {
            'aptitude_questions': None,
            'soft_skills_questions': None,
            'coding_questions': None,
            'hr_questions': None
        }
        
        # Map task outputs to categories
        for i, task in enumerate(interview_crew.tasks):
            if hasattr(task, 'output') and task.output:
                output_text = str(task.output)
                if i == 0:  # Aptitude task
                    agent_outputs['aptitude_questions'] = output_text
                elif i == 1:  # Soft skills task
                    agent_outputs['soft_skills_questions'] = output_text
                elif i == 2:  # Coding task
                    agent_outputs['coding_questions'] = output_text
                elif i == 3:  # HR task
                    agent_outputs['hr_questions'] = output_text
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Calculate total questions
        total_questions = sum(count_questions(q) for q in agent_outputs.values() if q)
        
        print(f"\n✅ CrewAI interview completed in {duration:.1f} seconds!")
        print(f"📊 Generated {total_questions} questions across {len([v for v in agent_outputs.values() if v])} categories")
        
        return {
            'candidate_name': candidate_name,
            'candidate_role': candidate_role,
            'total_questions': total_questions,
            'agent_outputs': agent_outputs,
            'duration_seconds': duration,
            'status': 'success',
            'crew_result': str(result)
        }
        
    except Exception as e:
        print(f"❌ Error during CrewAI interview process: {str(e)}")
        raise

def test_llm_connection():
    """Test the LLM connection."""
    print("🔍 Testing LLM Connection...")
    try:
        response = llm.invoke("Hello, please respond with 'OK' if you can hear me.")
        content = str(response.content) if hasattr(response, 'content') else str(response)
        
        if 'OK' in content or 'ok' in content.lower():
            print("✅ LLM connection successful!")
            return True
        else:
            print(f"⚠️  Unexpected response: {content[:100]}...")
            return False
    except Exception as e:
        print(f"❌ LLM connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Test the system
    test_candidate = "John Doe"
    test_role = "Software Engineer"
    
    try:
        # Test LLM connection first
        if test_llm_connection():
            print("✅ LLM connection test passed!")
            
            # Run full interview
            result = run_interview(test_candidate, test_role)
            
            print("\n📋 CrewAI Interview Results:")
            print("=" * 40)
            for category, questions in result['agent_outputs'].items():
                if questions:
                    question_count = count_questions(questions)
                    print(f"\n{category.replace('_', ' ').title()} ({question_count} questions):")
                    print("-" * 40)
                    print(questions[:300] + "..." if len(questions) > 300 else questions)
        else:
            print("❌ LLM connection test failed")
    except Exception as e:
        print(f"Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
