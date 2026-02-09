
import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student
from coaching.models import CoachingConfig, Topic, StudentProgress
from coaching.ai_service import AICoachingService

student = Student.objects.get(id=10)
service = AICoachingService(student)
config, _ = CoachingConfig.objects.get_or_create(student=student)

print(f"--- TEST: Temporal Locking Verification ---")

# Setup: Set strict parameters
# Let's say we are in Month 9, Week 1 (Mat: Pozitif, Asal)
config.current_academic_month = 9
config.current_academic_week = 1
config.week_started_at = date.today() # Started TODAY
config.save()

# 1. Test: Completed all topics, but time < 7 days
print("\n[Case 1] All topics done, but started TODAY (0 days passed)")
topics = Topic.objects.filter(month=9, week=1)
for t in topics:
    StudentProgress.objects.update_or_create(student=student, topic=t, defaults={'is_completed': True})

m, w, _ = service._get_academic_week_scope()
print(f"Result: {m}.{w}")
if m == 9 and w == 1:
    print("SUCCESS: Stayed in Week 1 despite completion.")
else:
    print("FAILURE: Advanced prematurely.")

# 2. Test: Completed all topics, time >= 7 days
print("\n[Case 2] All topics done, AND 8 days passed")
config.week_started_at = date.today() - timedelta(days=8)
config.save()

m, w, _ = service._get_academic_week_scope()
print(f"Result: {m}.{w}")
# Should advance to next avail week (likely 9.2 or similar)
if not (m == 9 and w == 1):
    print(f"SUCCESS: Advanced to {m}.{w} correctly.")
else:
    print("FAILURE: Did not advance even though conditions met.")

# 3. Test: Time passed, but topics NOT done
print("\n[Case 3] 8 days passed, but topics NOT done (for next week)")
# Reset progress for new week topics
new_topics = Topic.objects.filter(month=m, week=w)
StudentProgress.objects.filter(student=student, topic__in=new_topics).delete()

# Ensure config is set to this new week, started 8 days ago
config.current_academic_month = m
config.current_academic_week = w
config.week_started_at = date.today() - timedelta(days=8)
config.save()

m_new, w_new, _ = service._get_academic_week_scope()
print(f"Result: {m_new}.{w_new}")

if m_new == m and w_new == w:
    print("SUCCESS: Stayed in week because work not done, even though time passed.")
else:
    print("FAILURE: Advanced without completing work.")
