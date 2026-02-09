
import os
import django
import sys
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.views import CurriculumViewSet

def final_debug():
    print("--- STARTING FINAL DEBUG ---")
    try:
        user = User.objects.get(username='iso')
        factory = APIRequestFactory()
        request = factory.get('/api/v1/coaching/curriculum/', {'view': 'tree', 'subject': 'matematik'})
        force_authenticate(request, user=user)
        view = CurriculumViewSet.as_view({'get': 'list'})
        response = view(request)
        print(f"STATUS: {response.status_code}")
        if response.status_code == 200:
            print("SUCCESS")
        else:
            print(f"ERROR: {response.data}")
    except Exception as e:
        print("EXCEPTION CAUGHT:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    final_debug()
