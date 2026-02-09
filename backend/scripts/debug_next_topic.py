import os
import django
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, StudentProgress, Subject
from students.models import Student
from coaching.ai_service import AICoachingService

def trace_next_topic():
    print("--- TRACING NEXT TOPIC ---")
    
    try:
        student = Student.objects.get(id=10) # Using ID 10 as confirmed before
    except Student.DoesNotExist:
        student = Student.objects.first()
        
    print(f"Student: {student.full_name} (ID: {student.id})")
    
    service = AICoachingService(student)
    
    # We want to debug 'Matematik'
    subject_name = "Matematik"
    
    try:
        subject = Subject.objects.get(name__iexact=subject_name)
    except Subject.DoesNotExist:
        print(f"Subject {subject_name} not found")
        return

    print(f"\nScanning topics for {subject.name}...")
    topics = Topic.objects.filter(subject=subject).order_by('month', 'week', 'order')
    
    # Dump all completion to see what IS completed
    all_progs = StudentProgress.objects.filter(student_id=student.id).select_related('topic')
    print("\n[DIAGNOSTIC] All Progress Entries for this student:")
    
    # We need a set of ACTUALLY completed IDs for the loop check
    completed_ids = set()
    
    for p in all_progs:
        status_str = "DONE" if p.is_completed else "PENDING"
        print(f" - {p.topic.title} (ID: {p.topic.id}) -> {status_str}")
        if p.is_completed and p.topic.subject.name == subject_name:
            completed_ids.add(p.topic.id)
            
    print(f"\n[Computed] Completed IDs Set for {subject_name}: {completed_ids}")
    print(f"\nScanning sequential order...")
    
    for i, topic in enumerate(topics):
        status = "COMPLETED" if topic.id in completed_ids else "PENDING"
        print(f"[{i}] ID: {topic.id} | {topic.title} (M:{topic.month}, W:{topic.week}, O:{topic.order}) -> {status}")
        
        if topic.id not in completed_ids:
            print(f"\n>>> MATCH FOUND! The service SHOULD return: {topic.title} (ID: {topic.id})")
            return

    print("\nNo next topic found (All completed?)")

if __name__ == "__main__":
    trace_next_topic()
