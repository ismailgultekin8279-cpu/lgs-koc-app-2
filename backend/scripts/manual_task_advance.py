
import os
import django
import sys
from datetime import date

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, StudentProgress
from students.models import Student, StudyTask

def manual_advance():
    print("=== MANUAL TASK ADVANCEMENT ===")
    student = Student.objects.get(id=10)
    today = date.today()
    
    # 1. Topic 2431 (Asal Çarpanlara Ayırma)
    topic = Topic.objects.get(id=2431)
    
    # 2. Delete any existing Math tasks for today to avoid duplicates
    StudyTask.objects.filter(student=student, date=today, subject="Matematik").delete()
    
    # 3. Create fresh task
    task = StudyTask.objects.create(
        student=student,
        date=today,
        topic_id=topic.id,
        topic_name=topic.title,
        subject="Matematik",
        task_type="practice",
        question_count=30,
        recommended_seconds=45 * 60,
        status="pending"
    )
    print(f"Created task: {task.topic_name} for {today}")

if __name__ == "__main__":
    manual_advance()
