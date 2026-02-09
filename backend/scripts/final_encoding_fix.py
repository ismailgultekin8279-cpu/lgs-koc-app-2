
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, Subject

def run_fix():
    print("--- STARTING FINAL CHARACTER FIX ---")
    
    # We will target specifically the Week 1 topics the user sees.
    # We use very basic string replacements that are known to fix mojibake 
    # when UTF-8 is misread as Latin1/Windows-1254.
    
    # İÅŸ -> İş
    # ÄŸ -> ğ
    # Ä± -> ı
    # Ã‡ -> Ç
    # Ã§ -> ç
    # Ã– -> Ö
    # Ã¶ -> ö
    # Ãœ -> Ü
    # Ã¼ -> ü
    
    replaces = [
        ("İÅŸ", "İş"),
        ("neÄŸi", "neği"),
        ("GiriÅŸ", "Giriş"),
        ("GeliÅŸ", "Geliş"),
        ("HÄ±z", "Hız"),
        ("SÃ¼reÃ§", "Süreç"),
        ("Ã‡Ã¶zme", "Çözme"),
        ("Ã‡arpanlar", "Çarpanlar"),
        ("AyÄ±rma", "Ayırma"),
        ("SayÄ±lar", "Sayılar"),
        ("TÃ¼rkÃ§e", "Türkçe"),
        ("Ä°ÅŸlem", "İşlem")
    ]
    
    # 1. Fix Subjects
    for s in Subject.objects.all():
        new_name = s.name
        for bad, good in replaces:
            new_name = new_name.replace(bad, good)
        
        if new_name != s.name:
            print(f"Subject Fix: {s.name} -> {new_name}")
            # Check for name collision
            if Subject.objects.filter(name=new_name).exists():
                # Merge
                existing = Subject.objects.get(name=new_name)
                Topic.objects.filter(subject=s).update(subject=existing)
                s.delete()
            else:
                s.name = new_name
                s.save()

    # 2. Fix Topics
    topics = Topic.objects.all()
    count = 0
    for t in topics:
        orig = t.title
        new_title = orig
        for bad, good in replaces:
            new_title = new_title.replace(bad, good)
        
        if new_title != orig:
            t.title = new_title
            t.save()
            count += 1
            
    print(f"Fixed {count} Topic titles.")
    
    # 3. Double check specifically "Temel İşlem Yeteneği" which looked bad in screenshot
    # ID was 285
    try:
        t285 = Topic.objects.get(id=285)
        # Manually force set to be 100% sure
        t285.title = "Temel İşlem Yeteneği"
        t285.save()
        print("Force fixed Topic 285.")
    except:
        pass

    print("--- FINAL FIX COMPLETE ---")

if __name__ == "__main__":
    run_fix()
