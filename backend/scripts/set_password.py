
import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from django.contrib.auth.models import User

# Reset iso password to a known value
user = User.objects.get(username='iso')
user.set_password('iso123')
user.save()

print(f"Password for '{user.username}' has been set to 'iso123'")
