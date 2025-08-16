#!/usr/bin/env python3
"""
Simple Interview Question Generator using LangChain and Gemini 1.5 Flash
This version bypasses CrewAI complexity and works directly with LangChain.
Each category generates exactly 10 questions.
"""

import os
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage

# Load environment variables
load_dotenv()

# Configure Google Generative AI
try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.7,
        max_tokens=8192,
        convert_system_message_to_human=True,
        top_p=0.9,
        top_k=40
    )
    print("✅ Successfully initialized Gemini 1.5 Flash model")
    
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
            top_k=40
        )
        print("✅ Successfully initialized Gemini Pro model")
    except Exception as e2:
        print(f"❌ Error initializing Gemini Pro: {str(e2)}")
        raise

def generate_aptitude_questions(candidate_name, candidate_role):
    """Generate 10 aptitude questions."""
    system_prompt = """You are an expert psychometric evaluator with deep knowledge in cognitive assessment. 
    Your specialty is creating challenging, non-memorizable aptitude questions that reveal true problem-solving abilities."""
    
    user_prompt = f"""Generate exactly 10 unique aptitude questions for {candidate_name} applying for {candidate_role}. 
    Questions should cover:
    - Logical reasoning and deduction
    - Numerical analysis and problem-solving
    - Pattern recognition and sequence completion
    - Critical thinking and analytical skills
    
    Make questions challenging but fair, avoiding memorizable patterns. 
    Format your response as a numbered list from 1 to 10."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    
    response = llm.invoke(messages)
    return response.content

def generate_soft_skills_questions(candidate_name, candidate_role):
    """Generate 10 soft skills questions."""
    system_prompt = """You are a senior HR professional with expertise in soft skills assessment and organizational psychology. 
    You excel at crafting questions that reveal authentic communication patterns and predict workplace success."""
    
    user_prompt = f"""Generate exactly 10 soft skills questions for {candidate_name} applying for {candidate_role}. 
    Questions should cover:
    - Communication and presentation skills
    - Teamwork and collaboration
    - Leadership and initiative
    - Adaptability and problem-solving
    
    Focus on real-world scenarios and behavioral examples. 
    Format your response as a numbered list from 1 to 10."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    
    response = llm.invoke(messages)
    return response.content

def generate_technical_questions(candidate_name, candidate_role):
    """Generate 10 technical questions."""
    system_prompt = """You are a senior software architect and technical expert with years of experience in technical hiring. 
    You specialize in creating questions that test both theoretical knowledge and practical coding skills."""
    
    user_prompt = f"""Generate exactly 10 technical and coding questions for {candidate_name} applying for {candidate_role}. 
    Questions should cover:
    - Programming fundamentals and best practices
    - Data structures and algorithms
    - System design and architecture
    - Code optimization and debugging
    
    Include both theoretical concepts and practical coding scenarios. 
    Format your response as a numbered list from 1 to 10."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    
    response = llm.invoke(messages)
    return response.content

def generate_hr_questions(candidate_name, candidate_role):
    """Generate 10 HR questions."""
    system_prompt = """You are a senior HR manager with expertise in cultural assessment and employee engagement. 
    You understand how to evaluate whether candidates will thrive in the company culture and contribute positively to the team."""
    
    user_prompt = f"""Generate exactly 10 HR questions for {candidate_name} applying for {candidate_role}. 
    Questions should cover:
    - Career goals and motivation
    - Work style and preferences
    - Cultural fit and values alignment
    - Professional development and growth
    
    Focus on understanding the candidate's long-term fit and potential. 
    Format your response as a numbered list from 1 to 10."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    
    response = llm.invoke(messages)
    return response.content

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
    Run the complete interview process and return structured results.
    """
    print(f"\n🚀 Starting interview process for {candidate_name} - {candidate_role}")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        # Generate questions for each category
        print("\n🤖 Generating Aptitude questions...")
        aptitude_questions = generate_aptitude_questions(candidate_name, candidate_role)
        print(f"✅ Generated {count_questions(aptitude_questions)} Aptitude questions")
        
        print("\n🤖 Generating Soft Skills questions...")
        soft_skills_questions = generate_soft_skills_questions(candidate_name, candidate_role)
        print(f"✅ Generated {count_questions(soft_skills_questions)} Soft Skills questions")
        
        print("\n🤖 Generating Technical questions...")
        technical_questions = generate_technical_questions(candidate_name, candidate_role)
        print(f"✅ Generated {count_questions(technical_questions)} Technical questions")
        
        print("\n🤖 Generating HR questions...")
        hr_questions = generate_hr_questions(candidate_name, candidate_role)
        print(f"✅ Generated {count_questions(hr_questions)} HR questions")
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Calculate total questions
        total_questions = (
            count_questions(aptitude_questions) +
            count_questions(soft_skills_questions) +
            count_questions(technical_questions) +
            count_questions(hr_questions)
        )
        
        print(f"\n✅ Interview completed in {duration:.1f} seconds!")
        print(f"📊 Generated {total_questions} questions across 4 categories")
        
        return {
            'candidate_name': candidate_name,
            'candidate_role': candidate_role,
            'total_questions': total_questions,
            'agent_outputs': {
                'aptitude_questions': aptitude_questions,
                'soft_skills_questions': soft_skills_questions,
                'coding_questions': technical_questions,
                'hr_questions': hr_questions
            },
            'duration_seconds': duration,
            'status': 'success'
        }
        
    except Exception as e:
        print(f"❌ Error during interview process: {str(e)}")
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
            
            print("\n📋 Interview Results:")
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
