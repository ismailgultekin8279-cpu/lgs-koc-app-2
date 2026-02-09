
import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, StudentProgress, Subject
from students.models import Student

def surgical_strike():
    sid = 10
    student = Student.objects.get(id=sid)
    
    print("--- SURGICAL STRIKE INITIATED ---")
    
    # 1. Force Topic 2430 (Math Order 0) to be completed
    t2430 = Topic.objects.get(id=2430)
    prog, created = StudentProgress.objects.update_or_create(
        student=student,
        topic=t2430,
        defaults={'is_completed': True, 'completed_at': timezone.now()}
    )
    print(f"Topic 2430 (Pozitif) marked COMPLETED: {prog.is_completed}")

    # 2. Fix the "TÃ¼rkÃ§e" subject mojibake
    try:
        bad_subj = Subject.objects.get(id=9)
        good_subj = Subject.objects.get(id=3)
        # Re-link logic if needed, but for now just delete the bad one if it has no topics
        if bad_subj.topics.count() == 0:
            bad_subj.delete()
            print("Deleted corrupted 'TÃ¼rkÃ§e' subject.")
        else:
            # Re-link topics to the good one
            bad_subj.topics.update(subject=good_subj)
            bad_subj.delete()
            print("Merged corrupted 'TÃ¼rkÃ§e' into correct 'Türkçe'.")
    except:
        print("Corrupted subject already handled or missing.")

    # 3. DIVERSIFY the curriculum to prevent "Pseudo-Stuck" feel
    # We will add suffixes to the duplicated topics (Order 0, 1, 2...) across weeks
    # to ensure they are unique.
    math_topics = Topic.objects.filter(subject__name="Matematik").order_by('month', 'week', 'order')
    
    # We want each week to feel unique.
    # Current issue: POOLS[0] = "Pozitif..." is in EVERY week.
    # We should at least change the Title for Week 2, 3, 4 etc.
    
    print("Diversifying Math curriculum titles...")
    for t in math_topics:
        # Suffix based on month and week
        # Use literal Turkish to avoid mojibake
        month_name = {9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık", 1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan", 5: "Mayıs", 6: "Haziran"}.get(t.month, str(t.month))
        # Optional: only add suffix if it's NOT week 1 or special
        # But we want uniqueness to break the loop.
        new_title = f"{t.title} ({month_name} {t.week}. Hafta)"
        if not t.title.endswith(")"):
            t.title = new_title
            t.save()

    print("--- SURGICAL STRIKE COMPLETE ---")

if __name__ == "__main__":
    surgical_strike()
