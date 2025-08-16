from flask import Flask, request, jsonify, render_template
import os
import sys
import time
import traceback
from dotenv import load_dotenv
from simple_agent import run_interview, llm, test_llm_connection
from pprint import pprint

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Global variable to store the LLM instance
try:
    # Test the LLM connection on startup
    if test_llm_connection():
        print("✅ LLM connection test successful")
        test_llm = llm
    else:
        print("❌ LLM connection test failed")
        test_llm = None
except Exception as e:
    print(f"❌ LLM connection test failed: {str(e)}")
    test_llm = None
    print("\nTroubleshooting steps:")
    print("1. Verify GOOGLE_API_KEY in .env file")
    print("2. Check billing status at https://console.cloud.google.com/billing")
    print("3. Enable Generative Language API at https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com")

@app.route('/interview', methods=['POST'])
def run_interview_endpoint():
    data = request.get_json()
    if not data or 'candidate_name' not in data or 'candidate_role' not in data:
        return jsonify({'error': 'Missing candidate_name or candidate_role'}), 400

    candidate_name = data.get('candidate_name')
    candidate_role = data.get('candidate_role')

    try:
        # Quick LLM connectivity check
        if not test_llm_connection():
            return jsonify({'error': 'LLM connectivity failed. Check terminal logs for details.'}), 500

        # Use the CrewAI run_interview function
        result = run_interview(candidate_name, candidate_role)
        
        # Structure the response
        response = {
            'candidate_name': result['candidate_name'],
            'candidate_role': result['candidate_role'],
            'total_questions': result['total_questions'],
            'duration_seconds': result['duration_seconds'],
            'question_sets': {
                'aptitude': {
                    'title': 'Aptitude Questions',
                    'count': 10,
                    'questions': result['agent_outputs']['aptitude_questions']
                },
                'soft_skills': {
                    'title': 'Soft Skills Questions', 
                    'count': 10,
                    'questions': result['agent_outputs']['soft_skills_questions']
                },
                'coding': {
                    'title': 'Technical & Coding Questions',
                    'count': 10, 
                    'questions': result['agent_outputs']['coding_questions']
                },
                'hr': {
                    'title': 'HR & Cultural Fit Questions',
                    'count': 10,
                    'questions': result['agent_outputs']['hr_questions']
                }
            },
            'status': 'success',
            'message': f'Successfully generated {result["total_questions"]} questions across 4 categories in {result["duration_seconds"]:.1f} seconds using CrewAI',
            'crew_result': result.get('crew_result', '')
        }
        
        return jsonify(response)
        
    except Exception as e:
        # Print full traceback to terminal for debugging
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'error_type': e.__class__.__name__,
            'status': 'error'
        }), 500

@app.route('/health/llm', methods=['GET'])
def health_llm():
    """Check the health status of the LLM connection."""
    try:
        # Get model information
        model_info = {
            'model': 'gemini-1.5-flash',
            'provider': 'Google Generative AI',
            'api_key_present': bool(os.getenv('GOOGLE_API_KEY')),
            'api_key_masked': f"{os.getenv('GOOGLE_API_KEY', '')[:3]}...{os.getenv('GOOGLE_API_KEY', '')[-3:]}" if os.getenv('GOOGLE_API_KEY') else 'not set',
            'environment': os.getenv('FLASK_ENV', 'development')
        }
        
        # Test connectivity
        if test_llm_connection():
            health_status = {
                'status': 'operational',
                'model': model_info,
                'response_time': 'tested',
                'timestamp': time.time()
            }
            return jsonify(health_status), 200
        else:
            return jsonify({
                'status': 'error',
                'model': model_info,
                'error': 'LLM connection test failed'
            }), 500
        
    except Exception as e:
        error_info = {
            'status': 'error',
            'error': str(e),
            'error_type': e.__class__.__name__,
            'troubleshooting': [
                'Verify GOOGLE_API_KEY in .env file',
                'Check billing status at https://console.cloud.google.com/billing',
                'Enable Generative Language API',
                'Check API quota and limits'
            ]
        }
        return jsonify(error_info), 500

@app.route('/api/status', methods=['GET'])
def api_status():
    """Check the overall API status."""
    return jsonify({
        'status': 'operational',
        'version': '3.1.0',
        'llm_connected': test_llm is not None,
        'features': {
            'question_generation': True,
            'agents_count': 4,
            'questions_per_agent': 10,
            'total_questions': 40,
            'crewai_integration': True,
            'multi_agent_system': True
        }
    }), 200

@app.route('/', methods=['GET'])
def home():
    """Simple home page with API information."""
    return jsonify({
        'message': 'CrewAI Multi-Agent Interview Question Generator API',
        'version': '3.1.0',
        'endpoints': {
            'POST /interview': 'Generate interview questions using CrewAI agents',
            'GET /health/llm': 'Check LLM connectivity',
            'GET /api/status': 'Check API status',
            'GET /test': 'Test CrewAI system',
            'GET /agents': 'List all agents'
        },
        'usage': {
            'method': 'POST',
            'endpoint': '/interview',
            'body': {
                'candidate_name': 'string',
                'candidate_role': 'string'
            },
            'response': {
                'total_questions': 40,
                'question_sets': {
                    'aptitude': '10 questions (Aptitude Agent)',
                    'soft_skills': '10 questions (Soft Skills Agent)', 
                    'coding': '10 questions (Coding Agent)',
                    'hr': '10 questions (HR Agent)'
                }
            }
        },
        'features': {
            'gemini_1_5_flash': True,
            'crewai_multi_agent': True,
            'specialized_agents': True,
            'sequential_processing': True,
            'agentic_ui': True
        }
    }), 200

@app.route('/test', methods=['GET'])
def test_endpoint():
    """Test endpoint to verify the CrewAI system is working."""
    try:
        # Run a quick test
        result = run_interview("Test User", "Test Role")
        return jsonify({
            'status': 'success',
            'message': 'CrewAI system is working correctly',
            'test_result': {
                'total_questions': result['total_questions'],
                'duration_seconds': result['duration_seconds'],
                'categories_generated': len([v for v in result['agent_outputs'].values() if v]),
                'agents_used': 4
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'CrewAI system test failed',
            'error': str(e)
        }), 500

@app.route('/agents', methods=['GET'])
def list_agents():
    """List the available agents in the CrewAI system."""
    return jsonify({
        'agents': [
            {
                'name': 'Aptitude and Critical Thinking Assessment Specialist',
                'role': 'Generates 10 aptitude questions',
                'expertise': 'Psychometric evaluation, cognitive assessment',
                'focus': 'Logical reasoning, numerical analysis, pattern recognition'
            },
            {
                'name': 'Soft Skills and Communication Assessment Specialist',
                'role': 'Generates 10 soft skills questions',
                'expertise': 'HR, soft skills assessment, organizational psychology',
                'focus': 'Communication, teamwork, leadership, adaptability'
            },
            {
                'name': 'Technical and Coding Assessment Specialist',
                'role': 'Generates 10 technical and coding questions',
                'expertise': 'Software architecture, technical expertise',
                'focus': 'Programming, algorithms, data structures, system design'
            },
            {
                'name': 'HR and Cultural Fit Assessment Specialist',
                'role': 'Generates 10 HR questions',
                'expertise': 'Cultural assessment, employee engagement',
                'focus': 'Career goals, work style, cultural fit, values alignment'
            }
        ],
        'total_agents': 4,
        'process': 'Sequential execution',
        'total_questions': 40
    }), 200

if __name__ == '__main__':
    print("🚀 Starting CrewAI Multi-Agent Interview Question Generator API...")
    print("🤖 4 specialized agents will generate exactly 10 questions each")
    print("🔗 API will be available at http://localhost:5001")
    print("✅ Using CrewAI with Gemini 1.5 Flash for multi-agent collaboration")
    app.run(debug=True, port=5001)
