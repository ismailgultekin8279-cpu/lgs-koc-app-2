
import os
import django
import sys
from datetime import date

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student, StudyTask
from coaching.models import CoachingConfig, Topic, StudentProgress, Subject
from coaching.ai_service import AICoachingService

def diagnose_stuck():
    print("=== DIAGNOSE PLAN STUCK ===\n")
    
    try:
        student = Student.objects.get(id=10)
        print(f"👤 Student: {student.full_name}")
    except:
        print("❌ Student 10 not found")
        return
    
    # 1. Check Config
    config, _ = CoachingConfig.objects.get_or_create(student=student)
    print(f"\n📅 Academic Config:")
    print(f"   Current Month: {config.current_academic_month}")
    print(f"   Current Week: {config.current_academic_week}")
    print(f"   Week Started: {config.week_started_at}")
    
    # 2. Check Week Completion
    if config.current_academic_month and config.current_academic_week:
        week_topics = Topic.objects.filter(
            month=config.current_academic_month,
            week=config.current_academic_week
        )
        
        completed_in_week = StudentProgress.objects.filter(
            student=student,
            topic__in=week_topics,
            is_completed=True
        ).count()
        
        total_in_week = week_topics.count()
        
        print(f"\n📊 Week Completion:")
        print(f"   Total topics in active week: {total_in_week}")
        print(f"   Completed topics: {completed_in_week}")
        print(f"   Week is complete: {completed_in_week >= total_in_week}")
        
        # Show incomplete topics
        incomplete = week_topics.exclude(
            id__in=StudentProgress.objects.filter(
                student=student,
                is_completed=True
            ).values_list('topic_id', flat=True)
        )
        
        if incomplete.exists():
            print(f"\n❌ Incomplete topics in active week:")
            for t in incomplete[:5]:
                print(f"      - ID {t.id}: {t.subject.name} - {t.title}")
    
    # 3. Check AI Service Logic
    print(f"\n🤖 AI Service Analysis:")
    service = AICoachingService(student)
    m, w, week_topics = service._get_academic_week_scope()
    
    print(f"   AI Selected Scope: Month {m}, Week {w}")
    print(f"   Topics in scope: {week_topics.count()}")
    
    # 4. Check Today's Plan
    today = date.today()
    tasks_today = StudyTask.objects.filter(student=student, date=today).order_by('order')
    
    print(f"\n📋 Today's Plan ({today}):")
    if tasks_today.exists():
        for task in tasks_today:
            print(f"   {task.order}. {task.subject} - {task.topic_name}")
            print(f"      (Topic ID: {task.topic_id}, Status: {task.status})")
    else:
        print("   ❌ No tasks found for today!")
    
    # 5. Check if Pozitif is in the plan
    pozitif_in_plan = tasks_today.filter(topic_name__icontains="Pozitif").first()
    if pozitif_in_plan:
        print(f"\n⚠️  POZITIF STILL IN PLAN!")
        print(f"   Task ID: {pozitif_in_plan.id}")
        print(f"   Topic ID: {pozitif_in_plan.topic_id}")
        print(f"   Status: {pozitif_in_plan.status}")
        
        # Check if this topic is marked complete in DB
        if pozitif_in_plan.topic_id:
            prog = StudentProgress.objects.filter(
                student=student,
                topic_id=pozitif_in_plan.topic_id
            ).first()
            
            if prog:
                print(f"   Progress Status: {'COMPLETED ✅' if prog.is_completed else 'INCOMPLETE ❌'}")
            else:
                print(f"   ❌ NO PROGRESS RECORD!")

if __name__ == "__main__":
    diagnose_stuck()
