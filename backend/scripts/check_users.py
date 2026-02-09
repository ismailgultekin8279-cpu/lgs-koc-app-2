
import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from django.contrib.auth.models import User

# List all users and check if password is usable
users = User.objects.all()

for user in users:
    print(f"Username: {user.username}")
    print(f"  Has usable password: {user.has_usable_password()}")
    print(f"  Is active: {user.is_active}")
    print()
