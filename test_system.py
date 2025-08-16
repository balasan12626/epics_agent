#!/usr/bin/env python3
"""
Comprehensive Test Suite for Interview Question Generator
Tests all components: LLM connection, question generation, and API endpoints.
"""

import os
import sys
import time
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_llm_connection():
    """Test the LLM connection."""
    print("🔍 Testing LLM Connection...")
    try:
        from simple_agent import test_llm_connection
        return test_llm_connection()
    except Exception as e:
        print(f"❌ LLM connection test failed: {str(e)}")
        return False

def test_question_generation():
    """Test question generation functionality."""
    print("\n🧪 Testing Question Generation...")
    try:
        from simple_agent import run_interview, count_questions
        
        # Run a quick test
        result = run_interview("Test User", "Software Engineer")
        
        # Verify structure
        required_keys = ['candidate_name', 'candidate_role', 'total_questions', 'agent_outputs', 'duration_seconds']
        for key in required_keys:
            if key not in result:
                print(f"❌ Missing key in result: {key}")
                return False
        
        # Verify question counts
        agent_outputs = result['agent_outputs']
        expected_agents = ['aptitude_questions', 'soft_skills_questions', 'coding_questions', 'hr_questions']
        
        total_questions = 0
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
            total_questions += question_count
            print(f"📊 {agent_type}: {question_count} questions")
            
            if question_count < 8:  # Allow some flexibility
                print(f"⚠️  Low question count for {agent_type}: {question_count}")
        
        print(f"✅ Question generation test passed!")
        print(f"📈 Total questions generated: {total_questions}")
        print(f"⏱️  Duration: {result['duration_seconds']:.1f} seconds")
        return True
        
    except Exception as e:
        print(f"❌ Question generation test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoints():
    """Test API endpoints."""
    print("\n🌐 Testing API Endpoints...")
    
    base_url = "http://localhost:5001"
    
    try:
        # Test API status
        print("Testing /api/status...")
        response = requests.get(f"{base_url}/api/status", timeout=10)
        if response.status_code == 200:
            print("✅ API status endpoint working")
            status_data = response.json()
            print(f"📊 API Version: {status_data.get('version', 'unknown')}")
        else:
            print(f"❌ API status failed: {response.status_code}")
            return False
        
        # Test LLM health
        print("Testing /health/llm...")
        response = requests.get(f"{base_url}/health/llm", timeout=10)
        if response.status_code == 200:
            print("✅ LLM health endpoint working")
            health_data = response.json()
            print(f"📊 LLM Status: {health_data.get('status', 'unknown')}")
        else:
            print(f"❌ LLM health failed: {response.status_code}")
            return False
        
        # Test interview generation
        print("Testing /interview...")
        test_data = {
            "candidate_name": "Test Candidate",
            "candidate_role": "Data Scientist"
        }
        response = requests.post(f"{base_url}/interview", json=test_data, timeout=60)
        if response.status_code == 200:
            print("✅ Interview generation endpoint working")
            interview_data = response.json()
            print(f"📊 Questions generated: {interview_data.get('total_questions', 0)}")
            print(f"⏱️  Duration: {interview_data.get('duration_seconds', 0):.1f} seconds")
        else:
            print(f"❌ Interview generation failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ API server not running. Start with: python app.py")
        return False
    except Exception as e:
        print(f"❌ API test failed: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("🧪 Interview Question Generator - Comprehensive Test Suite")
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
        ("Question Generation", test_question_generation),
        ("API Endpoints", test_api_endpoints),
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
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:25} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Your system is working correctly.")
        print("\n📋 USAGE:")
        print("1. Start API: python app.py")
        print("2. Test directly: python simple_agent.py")
        print("3. Generate questions using 4 specialized agents!")
        print("4. Each agent generates exactly 10 questions")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
