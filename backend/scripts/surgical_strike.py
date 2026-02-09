
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, Subject

def surgical_strike():
    print("--- STARTING SURGICAL STRIKE ---")

    # 1. Week 1 Cleanup
    # Delete the impostor LGS topic at Order 0 (ID 294 based on audit, but let's be safe by query)
    impostors = Topic.objects.filter(month=9, week=1, order=0).exclude(title__startswith="Pozitif")
    for imp in impostors:
        print(f"Deleting Week 1 Impostor: {imp.title} (Order 0)")
        imp.delete()
        
    # Ensure Pozitif is correct
    try:
        pozitif = Topic.objects.get(month=9, week=1, order=0)
        if "Pozitif" not in pozitif.title:
             print(f"WARNING: Order 0 is '{pozitif.title}', renaming to Pozitif...")
             pozitif.title = "Pozitif Tam Say\u0131lar\u0131n \u00c7arpanlar\u0131"
             pozitif.save()
        else:
            print("Week 1 Order 0 is verified: Pozitif.")
    except Topic.DoesNotExist:
        # Re-create if missing
        print("CRITICAL: Pozitif missing. Re-creating.")
        sub = Subject.objects.get(name="Matematik")
        Topic.objects.create(
            subject=sub, month=9, week=1, order=0, 
            title="Pozitif Tam Say\u0131lar\u0131n \u00c7arpanlar\u0131"
        )

    # 2. Week 2-30 Cleanup
    # Delete ALL Topics with Order >= 20 in these months. 
    # This wipes the corrupted "Extras" so we can re-generate them cleanly.
    print("Wiping corrupted extras in future weeks...")
    corrupted_extras = Topic.objects.filter(order__gte=20).exclude(month=9, week=1)
    count = corrupted_extras.count()
    corrupted_extras.delete()
    print(f"Deleted {count} corrupted extra topics.")
    
    # 3. Re-Expand with Clean Strings
    # Re-run the logic but locally here with \u escapes
    print("Re-expanding future weeks with clean strings...")
    
    # Safe Extras Map
    EXTRAS = {
        "Matematik": [
            "Temel \u0130\u015flem Yetene\u011fi",
            "Mant\u0131k Muhakeme Prati\u011fi",
            "Say\u0131sal Analiz \u00c7al\u0131\u015fmas\u0131",
            "Problem \u00c7\u00f6zme Stratejileri",
            "\u0130\u015flem H\u0131z\u0131 Geli\u015ftirme",
            "LGS Tipi Soru Analizi",
            "Genel Matematik Tekrar\u0131"
        ],
        "T\u00fcrk\u00e7e": [
            "Paragraf Yorumlama",
            "S\u00f6zc\u00fckte Anlam Prati\u011fi",
            "Okuma Anlama \u00c7al\u0131\u015fmas\u0131"
        ],
        "Fen Bilimleri": [
            "Bilimsel S\u00fcre\u00e7 Becerileri",
            "Deney Analizi ve Yorumlama",
            "Fen Bilimleri Soru \u00c7\u00f6z\u00fcm\u00fc"
        ]
    }
    
    months = [9, 10, 11, 12, 1, 2, 3, 4, 5, 6]
    for m in months:
        for w in range(1, 5):
            # Skip 9.1 because check 1 handled it
            if m == 9 and w == 1: continue
            
            for subj_name, extras_list in EXTRAS.items():
                # Get subject safely
                try:
                    sub = Subject.objects.get(name=subj_name)
                except Subject.DoesNotExist:
                    # Try to match by startswith if encoded poorly
                    # But better to just create or skip
                    # Assuming nuking fixed subjects too? No nuking only topics.
                    # Try creating proper one
                    sub, _ = Subject.objects.get_or_create(name=subj_name)

                # Get existing Core topics (order < 20)
                core_count = Topic.objects.filter(subject=sub, month=m, week=w, order__lt=20).count()
                
                if "Matematik" in subj_name:
                    target = 7
                else:
                    target = 3
                
                needed = target - core_count
                if needed > 0:
                    for i in range(needed):
                        title = extras_list[i % len(extras_list)]
                        Topic.objects.get_or_create(
                            subject=sub, month=m, week=w, order=20+i,
                            defaults={"title": title}
                        )
                        
    print("--- SURGICAL STRIKE COMPLETE ---")

surgical_strike()
