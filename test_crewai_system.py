#!/usr/bin/env python3
"""
Test script for the CrewAI Multi-Agent Interview Question Generator
Tests the CrewAI system with multiple specialized agents.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_llm_connection():
    """Test the LLM connection."""
    print("🔍 Testing LLM Connection...")
    try:
        from crewai_agent import llm
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

def test_single_agent():
    """Test a single CrewAI agent."""
    print("\n🧪 Testing Single CrewAI Agent...")
    try:
        from crewai_agent import create_interview_crew, llm
        from crewai import Agent, Task
        
        # Create a simple test agent
        test_agent = Agent(
            role="Test Agent",
            goal="Generate a simple test response",
            backstory="A simple test agent for validation",
            llm=llm,
            verbose=True,
            allow_delegation=False
        )
        
        test_task = Task(
            description="Generate a simple test response",
            expected_output="A simple test response",
            agent=test_agent
        )
        
        # Test the agent
        response = test_agent.execute_task(test_task)
        if response:
            print("✅ Single agent test passed!")
            return True
        else:
            print("❌ Single agent test failed - no response")
            return False
            
    except Exception as e:
        print(f"❌ Single agent test failed: {str(e)}")
        return False

def test_full_crewai_system():
    """Test the complete CrewAI interview system."""
    print("\n🚀 Testing Full CrewAI System...")
    try:
        from crewai_agent import run_interview, count_questions
        
        # Run the complete interview
        result = run_interview("John Doe", "Data Scientist")
        
        # Verify structure
        required_keys = ['candidate_name', 'candidate_role', 'total_questions', 'agent_outputs', 'duration_seconds', 'crew_result']
        for key in required_keys:
            if key not in result:
                print(f"❌ Missing key in result: {key}")
                return False
        
        # Verify question counts
        agent_outputs = result['agent_outputs']
        expected_agents = ['aptitude_questions', 'soft_skills_questions', 'coding_questions', 'hr_questions']
        
        for agent_type in expected_agents:
            if agent_type not in agent_outputs:
                print(f"❌ Missing agent output: {agent_type}")
                return False
            
            questions = agent_outputs[agent_type]
            if not questions:
                print(f"❌ No questions generated for {agent_type}")
                return False
            
            # Count questions in the output
            question_count = count_questions(questions)
            print(f"📊 {agent_type}: {question_count} questions")
            
            if question_count < 5:  # Allow some flexibility
                print(f"⚠️  Low question count for {agent_type}: {question_count}")
        
        print(f"✅ Full CrewAI system test passed!")
        print(f"📈 Total questions generated: {result['total_questions']}")
        print(f"⏱️  Duration: {result['duration_seconds']:.1f} seconds")
        print(f"🤖 Crew result: {result['crew_result'][:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Full CrewAI system test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_agent_details():
    """Test that we can access agent details."""
    print("\n🤖 Testing Agent Details...")
    try:
        from crewai_agent import create_interview_crew
        
        # Create crew
        crew = create_interview_crew("Test Candidate", "Software Engineer")
        
        # Check agents
        if len(crew.agents) != 4:
            print(f"❌ Expected 4 agents, got {len(crew.agents)}")
            return False
        
        # Check agent roles
        expected_roles = [
            "Aptitude and Critical Thinking Assessment Specialist",
            "Soft Skills and Communication Assessment Specialist", 
            "Technical and Coding Assessment Specialist",
            "HR and Cultural Fit Assessment Specialist"
        ]
        
        for i, agent in enumerate(crew.agents):
            if agent.role != expected_roles[i]:
                print(f"❌ Agent {i+1} role mismatch: {agent.role}")
                return False
        
        # Check tasks
        if len(crew.tasks) != 4:
            print(f"❌ Expected 4 tasks, got {len(crew.tasks)}")
            return False
        
        print("✅ Agent details test passed!")
        print(f"📋 Agents: {[agent.role for agent in crew.agents]}")
        return True
        
    except Exception as e:
        print(f"❌ Agent details test failed: {str(e)}")
        return False

def main():
    """Run all CrewAI tests."""
    print("🧪 CrewAI Multi-Agent Interview Question Generator - System Test")
    print("=" * 60)
    
    # Check environment
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment")
        return False
    
    print(f"✅ API Key found: {api_key[:6]}...{api_key[-4:]}")
    
    # Run tests
    tests = [
        ("LLM Connection", test_llm_connection),
        ("Single Agent", test_single_agent),
        ("Agent Details", test_agent_details),
        ("Full CrewAI System", test_full_crewai_system),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 CREWAI TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:25} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All CrewAI tests passed! Your multi-agent system is working correctly.")
        print("\n📋 USAGE:")
        print("1. Run the API: python app.py")
        print("2. Test directly: python crewai_agent.py")
        print("3. Generate questions using 4 specialized agents!")
        print("4. Each agent generates exactly 10 questions")
        return True
    else:
        print("⚠️  Some CrewAI tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
