
import os
import google.generativeai as genai
from dotenv import load_dotenv

def test_key_v2():
    print("--- TESTING GEMINI API KEY V2 ---")
    
    # 1. Load .env
    load_dotenv('backend/.env')
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY is empty in .env!")
        return

    print(f"Key loaded: {api_key[:5]}...{api_key[-4:]}")

    # 2. Configure
    # Note: Using the google.generativeai package for testing as client logic might differ
    genai.configure(api_key=api_key)
    
    # 3. Test Call with STABLE model
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content("Say 'OK' if you see this.")
        print(f"✅ SUCCESS! Response: {response.text}")
    except Exception as e:
        print(f"❌ CONNECTION FAILED: {e}")

if __name__ == "__main__":
    test_key_v2()
