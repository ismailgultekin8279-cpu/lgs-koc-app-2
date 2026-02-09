
import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student, StudyTask
from coaching.models import Topic, StudentProgress
from students.views import StudyTaskViewSet

def verify_sync():
    student_id = 10
    print(f"--- VERIFYING SYNC FOR STUDENT {student_id} ---")
    
    # 1. Create a mock task
    task = StudyTask.objects.create(
        student_id=student_id,
        date=timezone.now().date(),
        subject="Matematik",
        topic_name="Pozitif Tam Sayıların Çarpanları (Pekiştirme)",
        task_type="review",
        question_count=15,
        recommended_seconds=900,
        status="pending",
        order=1
    )
    print(f"Created task: {task.topic_name}")
    
    # 2. Trigger sync
    viewset = StudyTaskViewSet()
    viewset._sync_to_curriculum(task, True)
    
    # 3. Check result
    topic = Topic.objects.filter(title="Pozitif Tam Sayıların Çarpanları").first()
    if topic:
        progress = StudentProgress.objects.filter(student_id=student_id, topic=topic).first()
        if progress and progress.is_completed:
            print(f"✅ SUCCESS: Curriculum '{topic.title}' is now Green!")
        else:
            print(f"❌ FAILURE: Curriculum '{topic.title}' is still Gray.")
            # Debug info
            print(f"Topic ID: {topic.id}")
            print(f"Progress exists: {progress is not None}")
            if progress:
                print(f"Progress is_completed: {progress.is_completed}")
    else:
        print("❌ FAILURE: Topic not found in DB.")

    task.delete()

verify_sync()
