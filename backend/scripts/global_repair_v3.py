
import os
import django
import sys
from django.db import transaction

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, Subject

def repair_curriculum():
    print("=== GLOBAL CURRICULUM REPAIR ===\n")
    
    # 1. Subject Slug Cleanup (ensure no junk slugs like ta14rkae)
    # Already deleted ID 9, but let's check others
    for s in Subject.objects.all():
        if not s.slug or len(s.slug) > 20 or not s.slug.islower():
             print(f"⚠️ Suspicious Subject: {s.name} (Slug: {s.slug})")

    # 2. Topic Repair mapping (Latin1 to UTF-8 mojibake repair)
    # Common patterns: Ã¼ -> ü, Ã¶ -> ö, c383c2bc -> c3bc
    
    topics = Topic.objects.all()
    print(f"Auditing {topics.count()} topics...\n")
    
    month_names = {
        9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık", 
        1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan", 5: "Mayıs", 6: "Haziran"
    }
    
    repaired_count = 0
    unique_count = 0
    
    with transaction.atomic():
        for t in topics:
            old_title = t.title
            new_title = old_title
            
            # A. Fix Mojibake (Double encoded UTF-8)
            try:
                # If it's corrupted, it might be double encoded
                # Example: Ã¼ (c3 83 c2 bc) -> bytes -> latin1 -> utf8 -> ü (c3 bc)
                if "Ã" in old_title or "Å" in old_title or "Ä" in old_title:
                     new_title = old_title.encode('latin1').decode('utf-8')
                     repaired_count += 1
            except:
                pass
            
            # B. Diversify (Add Week info to break the 40x duplicate loop)
            # Strategy: "Topic Title (Month Week)"
            sub_name = t.subject.name
            m_name = month_names.get(t.month, f"{t.month}.Ay")
            suffix = f"({m_name} {t.week}.Hafta)"
            
            if suffix not in new_title:
                new_title = f"{new_title} {suffix}"
                unique_count += 1
            
            if new_title != old_title:
                t.title = new_title
                t.save()
                
    print(f"Repaired Mojibake in {repaired_count} topics.")
    print(f"Unique-ified {unique_count} topics.")
    print("\n✅ GLOBAL REPAIR COMPLETE.")

if __name__ == "__main__":
    repair_curriculum()
