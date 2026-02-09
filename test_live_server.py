
import requests
import json

# Test the LIVE running server
BASE_URL = "http://localhost:8000"

def test_live_server():
    print("=== TESTING LIVE SERVER ===\n")
    
    # 1. Login to get token
    print("1. Logging in as 'iso'...")
    login_response = requests.post(f"{BASE_URL}/api/v1/students/auth/login/", json={
        "username": "iso",
        "password": "iso123"
    })
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return
    
    token_data = login_response.json()
    access_token = token_data.get("access")
    student_id = token_data.get("student", {}).get("id")
    
    print(f"✅ Login successful! Student ID: {student_id}\n")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # 2. Check current plan
    print("2. Fetching current daily plan...")
    plan_response = requests.get(
        f"{BASE_URL}/students/daily-plan/?student_id={student_id}",
        headers=headers
    )
    
    if plan_response.status_code == 200:
        plan_data = plan_response.json()
        tasks = plan_data if isinstance(plan_data, list) else plan_data.get('tasks', [])
        
        print(f"Current plan has {len(tasks)} tasks:")
        for i, task in enumerate(tasks[:5], 1):
            topic_name = task.get('topic_name', 'N/A')
            status = task.get('status', 'N/A')
            print(f"  {i}. {topic_name} (Status: {status})")
        
        # Check if Pozitif is there
        pozitif_tasks = [t for t in tasks if 'pozitif' in t.get('topic_name', '').lower()]
        if pozitif_tasks:
            print(f"\n⚠️  POZITIF FOUND IN CURRENT PLAN!")
        else:
            print(f"\n✅ Pozitif NOT in current plan")
    else:
        print(f"❌ Failed to fetch plan: {plan_response.status_code}")
    
    # 3. Trigger plan regeneration
    print("\n3. Triggering plan regeneration...")
    regen_response = requests.post(
        f"{BASE_URL}/coaching/coach/{student_id}/generate_plan/",
        headers=headers
    )
    
    if regen_response.status_code in [200, 201]:
        print("✅ Plan regeneration triggered!")
        
        # Fetch new plan
        print("\n4. Fetching NEW plan...")
        new_plan_response = requests.get(
            f"{BASE_URL}/students/daily-plan/?student_id={student_id}",
            headers=headers
        )
        
        if new_plan_response.status_code == 200:
            new_plan_data = new_plan_response.json()
            new_tasks = new_plan_data if isinstance(new_plan_data, list) else new_plan_data.get('tasks', [])
            
            print(f"New plan has {len(new_tasks)} tasks:")
            for i, task in enumerate(new_tasks[:5], 1):
                topic_name = task.get('topic_name', 'N/A')
                status = task.get('status', 'N/A')
                print(f"  {i}. {topic_name} (Status: {status})")
            
            # Check results
            pozitif_in_new = [t for t in new_tasks if 'pozitif' in t.get('topic_name', '').lower()]
            asal_in_new = [t for t in new_tasks if 'asal' in t.get('topic_name', '').lower()]
            
            if pozitif_in_new:
                print(f"\n❌ POZITIF STILL IN NEW PLAN!")
            else:
                print(f"\n✅ Pozitif removed from plan")
            
            if asal_in_new:
                print(f"✅ Asal Çarpanlar added to plan!")
            else:
                print(f"⚠️  Asal Çarpanlar NOT in new plan")
    else:
        print(f"❌ Plan regeneration failed: {regen_response.status_code}")
        print(f"Response: {regen_response.text}")

if __name__ == "__main__":
    test_live_server()
