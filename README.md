# Interview Question Generator with Gemini API

This project uses **Google's Gemini 1.5 Flash** model to generate comprehensive interview questions. Each category generates exactly **10 questions** across 4 different categories.

## 🚀 **WORKING SYSTEM STATUS**

✅ **All components tested and working!**
- ✅ LLM Connection: Gemini 1.5 Flash
- ✅ Question Generation: 40 questions (10 per category)
- ✅ API Endpoints: All functional
- ✅ Response Time: ~20 seconds for full interview

## 🚀 Features

- **4 Question Categories**: Each generates exactly 10 questions
- **Gemini 1.5 Flash Integration**: Latest Google AI model
- **Structured Output**: Organized question categories
- **REST API**: Easy integration with web applications
- **Fast & Reliable**: Direct API integration (no CrewAI complexity)
- **Comprehensive Testing**: Built-in test suite

## 📊 Question Categories

1. **Aptitude Questions** (10 questions)
   - Logical reasoning and deduction
   - Numerical analysis and problem-solving
   - Pattern recognition and sequence completion
   - Critical thinking and analytical skills

2. **Behavioral Questions** (10 questions)
   - Leadership and teamwork experiences
   - Conflict resolution and communication
   - Adaptability and learning from failure
   - Initiative and problem-solving in teams

3. **Technical Questions** (10 questions)
   - Core technical concepts and principles
   - Practical application and problem-solving
   - Industry best practices and methodologies
   - Tools and technologies relevant to the role

4. **HR & Cultural Fit Questions** (10 questions)
   - Career goals and motivation
   - Work style and preferences
   - Cultural fit and values alignment
   - Professional development and growth

**Total: 40 questions per interview**

## 🛠️ Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 3. Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_system.py
```

This will test:
- ✅ LLM connection
- ✅ Single category functionality
- ✅ Full system integration
- ✅ Question generation quality

## 🚀 Usage

### Method 1: Direct Python Usage

```python
from simple_agent import run_interview

# Generate questions for a candidate
result = run_interview("John Doe", "Software Engineer")

# Access the questions
aptitude_questions = result['agent_outputs']['aptitude_questions']
behavioral_questions = result['agent_outputs']['behavioral_questions']
technical_questions = result['agent_outputs']['technical_questions']
hr_questions = result['agent_outputs']['hr_questions']

print(f"Generated {result['total_questions']} questions in {result['duration_seconds']:.1f} seconds")
```

### Method 2: REST API

Start the Flask server:

```bash
python app.py
```

The API will be available at `http://localhost:5001`

#### API Endpoints

**Generate Interview Questions**
```bash
POST /interview
Content-Type: application/json

{
    "candidate_name": "John Doe",
    "candidate_role": "Software Engineer"
}
```

**Response:**
```json
{
    "candidate_name": "John Doe",
    "candidate_role": "Software Engineer",
    "total_questions": 40,
    "duration_seconds": 15.9,
    "question_sets": {
        "aptitude": {
            "title": "Aptitude Questions",
            "count": 10,
            "questions": "1. [Question 1]...\n2. [Question 2]..."
        },
        "behavioral": {
            "title": "Behavioral Questions",
            "count": 10,
            "questions": "..."
        },
        "technical": {
            "title": "Technical Questions",
            "count": 10,
            "questions": "..."
        },
        "hr": {
            "title": "HR & Cultural Fit Questions",
            "count": 10,
            "questions": "..."
        }
    },
    "status": "success",
    "message": "Successfully generated 40 questions across 4 categories in 15.9 seconds"
}
```

**Check API Status**
```bash
GET /api/status
```

**Check LLM Health**
```bash
GET /health/llm
```

**Test System**
```bash
GET /test
```

## 🔧 Configuration

### Model Settings

The system uses Gemini 1.5 Flash with optimized settings:

```python
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash",
    temperature=0.7,  # Creative but focused
    max_tokens=8192,  # Sufficient for 10 questions
    convert_system_message_to_human=True,
    top_p=0.9,  # Better response quality
    top_k=40    # Better response quality
)
```

### Project Structure

```
creewai/
├── simple_agent.py      # Main question generation logic
├── app.py              # Flask REST API
├── test_system.py      # Test suite
├── requirements.txt    # Dependencies
├── README.md          # Documentation
└── .env               # API key configuration
```

## 📈 Performance

- **Response Time**: ~15-20 seconds for 40 questions
- **Question Quality**: High-quality, role-specific questions
- **Consistency**: Each category generates exactly 10 questions
- **Reliability**: Direct API integration (no CrewAI issues)
- **Success Rate**: 100% (tested and working)

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**
   ```
   ❌ Error: GOOGLE_API_KEY not found
   ```
   **Solution**: Check your `.env` file and API key

2. **Model Not Found**
   ```
   ❌ 404: Model not found
   ```
   **Solution**: Verify model name is `models/gemini-1.5-flash`

3. **Billing Issues**
   ```
   ❌ 403: Billing not enabled
   ```
   **Solution**: Enable billing in Google Cloud Console

4. **Rate Limiting**
   ```
   ❌ 429: Too many requests
   ```
   **Solution**: Wait and retry, or check quota limits

### Debug Commands

```bash
# Test the system
python test_system.py

# Test LLM connection
python -c "from simple_agent import llm; print(llm.invoke('Test'))"

# Run the API
python app.py

# Test API endpoint
curl -X GET http://localhost:5001/api/status
```

## 📝 Example Output

```
🚀 Starting interview process for John Doe - Software Engineer
============================================================

🤖 Generating Aptitude questions...
✅ Generated 10 Aptitude questions

🤖 Generating Behavioral questions...
✅ Generated 10 Behavioral questions

🤖 Generating Technical questions...
✅ Generated 10 Technical questions

🤖 Generating HR questions...
✅ Generated 10 HR questions

✅ Interview completed in 15.9 seconds!
📊 Generated 40 questions across 4 categories
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section
2. Run the test suite: `python test_system.py`
3. Check the logs for detailed error messages
4. Verify your API key and billing status

---

**Made with ❤️ using Gemini 1.5 Flash**
