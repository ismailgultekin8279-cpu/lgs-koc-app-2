import requests
import json
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

def test_subjects():
    user = User.objects.get(username='iso')
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    
    subjects = ['matematik', 'fen-bilimleri', 'turkce']
    
    for sub in subjects:
        print(f"\n--- Testing Subject: {sub} ---")
        url = f"http://localhost:8000/api/v1/coaching/curriculum/?view=tree&subject={sub}"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        try:
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                data = res.json()
                print(f"Subject in Response: {data.get('subject')}")
                # Print first topic of first month to verify content
                if data.get('months'):
                    first_topic = data['months'][0]['weeks'][0]['topics'][0]['title']
                    print(f"First Topic: {first_topic}")
                else:
                    print("No months data found.")
            else:
                print(f"Failed. Status: {res.status_code}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_subjects()
