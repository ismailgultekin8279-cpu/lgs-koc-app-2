
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, Subject

def expand():
    subjects = {
        "Matematik": [
            "Temel İşlem Yeteneği",
            "Mantık Muhakeme Pratiği",
            "Sayısal Analiz Çalışması",
            "Problem Çözme Stratejileri",
            "İşlem Hızı Geliştirme",
            "LGS Tipi Soru Analizi",
            "Genel Matematik Tekrarı"
        ],
        "Türkçe": [
            "Paragraf Yorumlama",
            "Sözcükte Anlam Pratiği",
            "Okuma Anlama Çalışması"
        ],
        "Fen Bilimleri": [
            "Bilimsel Süreç Becerileri",
            "Deney Analizi ve Yorumlama",
            "Fen Bilimleri Soru Çözümü"
        ]
    }

    print("Scaling curriculum to 7 topics per week (Months 9-6)...")

    # Months: 9 (Sept) to 6 (June). 13 is used as a wrap if needed but usually 9-12 then 1-6
    months = [9, 10, 11, 12, 1, 2, 3, 4, 5, 6]
    
    for m in months:
        for w in range(1, 5): # Weeks 1-4
            print(f"Processing Month {m}, Week {w}...")
            
            for subj_name, extras in subjects.items():
                sub, _ = Subject.objects.get_or_create(name=subj_name)
                
                # Get existing topics for this week
                existing = Topic.objects.filter(subject=sub, month=m, week=w).count()
                
                if subj_name == "Matematik":
                    target = 7
                else:
                    target = 3 # Ensure at least 3 for core others
                
                needed = target - existing
                if needed > 0:
                    print(f"  Adding {needed} extras to {subj_name}")
                    for i in range(needed):
                        # Use order starting from 20 to not clobber main curriculum (usually 0, 1)
                        Topic.objects.get_or_create(
                            subject=sub,
                            month=m,
                            week=w,
                            title=extras[i % len(extras)],
                            defaults={"order": 20 + i}
                        )

    # 3. Final HARD REPAIR for Week 1 specifically since user is looking at it
    print("Performing targeted repair for Week 1 Math...")
    math_sub = Subject.objects.get(name="Matematik")
    week1_math = [
        (0, "Pozitif Tam Sayıların Çarpanları"),
        (1, "Asal Çarpanlara Ayırma"),
        (10, "Temel İşlem Yeteneği"),
        (11, "Mantık Muhakeme (Giriş)"),
        (12, "Sayısal Analiz Becerisi"),
        (13, "Problem Çözme Stratejileri"),
        (14, "İşlem Hızı Geliştirme")
    ]
    for order, title in week1_math:
        Topic.objects.filter(subject=math_sub, month=9, week=1, order=order).update(title=title)

    print("Expansion and Targeted Repair Complete.")

expand()
