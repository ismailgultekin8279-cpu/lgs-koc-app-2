
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    print("=== Testing Login ===")
    try:
        login_res = requests.post(f"{BASE_URL}/api/v1/students/auth/login/", json={
            "username": "iso",
            "password": "iso123"
        })
        print(f"Login Status: {login_res.status_code}")
        print(f"Login Data: {login_res.json().keys()}") # Check keys
        if 'student' in login_res.json():
             print(f"Student ID found in login: {login_res.json()['student']['id']}")
        else:
             print("!!! STUDENT KEY MISSING IN LOGIN RESPONSE !!!")
        
        if login_res.status_code != 200:
            print(f"Login Failed: {login_res.text}")
            return
        
        token = login_res.json()['access']
        headers = {"Authorization": f"Bearer {token}"}
        
        print("\n=== Testing Curriculum API (Türkçe) ===")
        curr_res = requests.get(f"{BASE_URL}/api/v1/coaching/curriculum/?view=tree&subject=turkce", headers=headers)
        print(f"Curriculum Status: {curr_res.status_code}")
        
        if curr_res.status_code == 200:
            print("Curriculum API Success!")
            try:
                data = curr_res.json()
                print(f"Subject returned: {data.get('subject')}")
                print(f"Months: {[m['name'] for m in data.get('months', [])]}")
            except json.JSONDecodeError:
                print("Error: Response is not valid JSON!")
                print(curr_res.text[:500])
        else:
            print(f"Curriculum API Error: {curr_res.text[:1000]}")
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_api()
