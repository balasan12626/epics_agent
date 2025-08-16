import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

def test_gemini_connection():
    print("🔍 Testing Gemini API connection...")
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in .env file")
        return False
    
    print("✅ Found GOOGLE_API_KEY in .env")
    
    try:
        # Initialize the LLM with Google's Gemini Pro
        llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.7,
            google_api_key=api_key
        )
        
        # Test with a simple prompt
        response = llm.invoke("Say 'OK' if you can hear me!")
        
        if response and hasattr(response, 'content') and 'OK' in response.content:
            print("✅ Successfully connected to Gemini Pro!")
            print(f"Response: {response.content}")
            return True
        else:
            print("❌ Unexpected response from Gemini Pro")
            return False
            
    except Exception as e:
        print(f"❌ Error connecting to Gemini Pro: {str(e)}")
        print("\nTROUBLESHOOTING STEPS:")
        print("1. Verify your GOOGLE_API_KEY is correct")
        print("2. Check billing status at https://console.cloud.google.com/billing")
        print("3. Enable Generative Language API: https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com")
        print("4. Check API quotas at: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas")
        return False

if __name__ == "__main__":
    test_gemini_connection()
