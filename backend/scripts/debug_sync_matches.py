
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lgs_dershane.settings')
django.setup()

from coaching.models import Topic, Subject

def normalize(text):
    if not text: return ""
    text = text.lower()
    replacements = {
        'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c', 
        'İ': 'i', 'Ğ': 'g', 'Ü': 'u', 'Ş': 's', 'Ö': 'o', 'Ç': 'c'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return "".join(c for c in text if c.isalnum())

def test_match(subject_name, task_name):
    print(f"--- Testing Match for Subject: '{subject_name}' Task: '{task_name}' ---")
    
    clean_name = task_name
    if " - " in clean_name:
        clean_name = clean_name.split(" - ", 1)[1]
    if "(" in clean_name:
        clean_name = clean_name.split("(")[0].strip()
        
    norm_task = normalize(clean_name)
    print(f"Clean Name: '{clean_name}'")
    print(f"Norm Task:  '{norm_task}'")
    
    # Get subjects
    subjects = Subject.objects.filter(name__iexact=subject_name)
    if not subjects.exists():
        print(f"ERROR: Subject '{subject_name}' not found!")
        print("Available subjects:", list(Subject.objects.values_list('name', flat=True)))
        return

    subject_topics = Topic.objects.filter(subject__name__iexact=subject_name)
    print(f"Found {len(subject_topics)} topics for subject '{subject_name}'.Checking...")
    
    matched = False
    for topic in subject_topics:
        norm_topic = normalize(topic.title)
        
        is_match = False
        if norm_task == norm_topic:
            print(f"  [MATCH EXACT] Topic: '{topic.title}' -> '{norm_topic}'")
            is_match = True
        elif len(norm_task) > 5 and len(norm_topic) > 5:
            if norm_task in norm_topic:
                print(f"  [MATCH SUBSTRING (Task in Topic)] Topic: '{topic.title}' -> '{norm_topic}'")
                is_match = True
            elif norm_topic in norm_task:
                 print(f"  [MATCH SUBSTRING (Topic in Task)] Topic: '{topic.title}' -> '{norm_topic}'")
                 is_match = True
        
        if is_match:
            matched = True
            break
            
    if not matched:
        print("FAIL: No match found.")
        # Print first 5 normalized topics to see what we are dealing with
        for t in subject_topics[:5]:
             print(f"  - DB Topic: '{t.title}' -> '{normalize(t.title)}'")

if __name__ == "__main__":
    # Test Case 1: The user's specific issue
    test_match("Matematik", "Pozitif Tam Sayıların Çarpanları")
    
    # Test Case 2: Full string
    test_match("Matematik", "Matematik - Pozitif Tam Sayıların Çarpanları")
