
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, Subject
from students.models import StudyTask

# Safe strings map
REPAIRS = {
    # MATH
    "Temel": "Temel \u0130\u015flem Yetene\u011fi",
    "Mant": "Mant\u0131k Muhakeme (Giri\u015f)",
    "Say": "Say\u0131sal Analiz Becerisi",
    "Problem": "Problem \u00c7\u00f6zme Stratejileri",
    "Hiz": "\u0130\u015flem H\u0131z\u0131 Geli\u015ftirme",
    "Analiz": "LGS Tipi Soru Analizi",
    "Genel": "Genel Matematik Tekrar\u0131",
    
    # TURKISH
    "Paragraf": "Paragraf Yorumlama",
    "Anlam": "S\u00f6zc\u00fckte Anlam Prati\u011fi",
    "Okuma": "Okuma Anlama \u00c7al\u0131\u015fmas\u0131",
    
    # SCIENCE
    "Bilimsel": "Bilimsel S\u00fcre\u00e7 Becerileri",
    "Deney": "Deney Analizi ve Yorumlama",
    "Fen": "Fen Bilimleri Soru \u00c7\u00f6z\u00fcm\u00fc",
    
    # GUIDANCE
    "Dikkat": "Dikkat ve Odaklanma"
}

print("Running Global Nuclear Repair (Weeks 2-30)...")

# 1. Topic Repair
# We iterate over all topics. If a topic title looks like one of our known "Extras" (via substring match),
# we FORCE update it to the clean Unicode string.
all_topics = Topic.objects.all()
t_count = 0
for t in all_topics:
    for key, safe_title in REPAIRS.items():
        # Match if key is in title AND title is corrupted (or just different)
        # Note: 'Temel' is in 'Temel İşlem Yeteneği'. match is safe.
        if key in t.title or key in t.title.encode('ascii', 'ignore').decode('ascii'):
            # Just force update to be safe, especially if it's an "Extra" (order >= 10 usually)
            if t.title != safe_title:
                # Only update if it seems to be that specific extra topic type
                # Simple heuristic: if it contains the key, assume it's that topic type
                # Be careful not to overwrite "Genel" in unrelated ways? 
                # "Genel" -> "Genel Matematik Tekrarı" might be dangerous for other subjects.
                # Let's check Subject for safety on generic keys.
                if key == "Genel" and t.subject.name != "Matematik": continue
                if key == "Fen" and t.subject.name != "Fen Bilimleri": continue

                t.title = safe_title
                t.save()
                t_count += 1
                break

print(f"Repaired {t_count} Topics.")

# 2. StudyTask Repair
# Existing tasks in the Daily Plan also have the titles copied. We must fix them too.
print("Repairing StudyTasks...")
# tasks = StudyTask.objects.filter(is_completed=False) # is_completed doesn't exist, it's 'status'
tasks = StudyTask.objects.exclude(status='done')
task_count = 0

for task in tasks:
    # 2a. Fix Title
    orig_title = task.topic_name
    new_title = orig_title
    
    # Fix the base topic part
    for key, safe_title in REPAIRS.items():
         if key in new_title:
             # Preserve the suffix like (Pekiştirme)
             # Regex replace might be better but let's try simple replace of the corrupted part
             # Actually, simpler: if we find the key, replace the MAIN part.
             # E.g. "Bilimsel SÃ¼reÃ§... (Pekiştirme)" -> "Bilimsel Süreç Becerileri (Pekiştirme)"
             
             # Split to check suffix
             suffix = ""
             if "(" in new_title and ")" in new_title and "Peki" in new_title:
                 suffix = " (Peki\u015ftirme)"
             elif "Öğrenme" in new_title or "\u00d6\u011frenme" in new_title: # Öğrenme
                 suffix = " (\u00d6\u011frenme)"
             
             new_title = safe_title + suffix
             break

    if new_title != orig_title:
        task.topic_name = new_title
        task.save()
        task_count += 1

print(f"Repaired {task_count} StudyTasks.")
print("Done.")
