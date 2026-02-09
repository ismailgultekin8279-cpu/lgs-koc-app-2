
import os
import google.generativeai as genai
from dotenv import load_dotenv

def test_key():
    print("--- TESTING GEMINI API KEY ---")
    
    # 1. Load .env
    load_dotenv('backend/.env')
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY is empty in .env!")
        return

    print(f"Key loaded: {api_key[:5]}...{api_key[-4:]}")

    # 2. Configure
    genai.configure(api_key=api_key)
    
    # 3. Test Call
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content("Say 'Hello' in Turkish.")
        print(f"✅ SUCCESS! Response: {response.text}")
    except Exception as e:
        print(f"❌ CONNECTION FAILED: {e}")

if __name__ == "__main__":
    test_key()
