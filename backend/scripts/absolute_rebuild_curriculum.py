
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, Subject

def absolute_rebuild_curriculum():
    # POOLS for each subject (standardized, high quality, no parentheses)
    POOLS = {
        "Matematik": [
            "Pozitif Tam Say\u0131lar\u0131n \u00c7arpanlar\u0131",
            "Asal \u00c7arpanlara Ay\u0131rma",
            "Temel \u0130\u015flem Yetene\u011fi",
            "Mant\u0131k Muhakeme",
            "Say\u0131sal Analiz Becerisi",
            "Problem \u00c7\u00f6zme Stratejileri",
            "Matematik H\u0131z Testi"
        ],
        "Fen Bilimleri": [
            "Mevsimlerin Olu\u015fumu",
            "Bilimsel Muhakeme Becerisi",
            "Deney Analizi ve Yorumlama",
            "Fen Bilimleri Yeni Nesil Soru",
            "Kavram Haritas\u0131 \u00c7al\u0131\u015fmas\u0131",
            "Fen Bilimleri H\u0131z Testi",
            "Fen Bilimleri Genel Tekrar"
        ],
        "T\u00fcrk\u00e7e": [
            "Paragraf Yorumlama",
            "S\u00f6zel Mant\u0131k Becerisi",
            "Okuma Anlama",
            "S\u00f6zc\u00fckte Anlam",
            "Yaz\u0131m ve Noktalama",
            "C\u00fcmlede Anlam",
            "T\u00fcrk\u00e7e H\u0131z Testi"
        ],
        "T.C. \u0130nk\u0131lap Tarihi": [
            "Kronolojik Analiz Becerisi",
            "Harita ve G\u00f6rsel Yorumlama",
            "Bir Kahraman Do\u011fuyor",
            "Milli Uyan\u0131\u015f",
            "Milli Destan",
            "Atat\u00fcrk\u00e7\u00fcl\u00fck ve \u0130nk\u0131laplar",
            "\u0130nk\u0131lap Tarihi Genel Tekrar"
        ],
        "Yabanc\u0131 Dil": [
            "Vocabulary Builder",
            "Reading Comprehension",
            "Grammar Review",
            "English Practice",
            "Word Association",
            "Translation Exercises",
            "English Speed Test"
        ],
        "Din K\u00fclt\u00fcr\u00fc": [
            "Kader \u0130nanc\u0131",
            "Zekat ve Sadaka",
            "Din ve Hayat",
            "Hz Muhammedin \u00d6rneklik",
            "Kuran ve \u00d6zellikleri",
            "Ahlaki Tutumlar",
            "Din Bilgisi Genel Tekrar"
        ]
    }

    months = [9, 10, 11, 12, 1, 2, 3, 4, 5, 6]
    
    print("--- REBUILDING CURRICULUM FROM SCRATCH (NO DUPLICATES) ---")
    
    # WIPE ALL TOPICS FIRST to ensure absolute cleanliness
    Topic.objects.all().delete()
    print("Database cleared.")
    
    total_added = 0
    
    for subj_name, pool in POOLS.items():
        sub, _ = Subject.objects.get_or_create(name=subj_name)
        print(f"Processing {subj_name}...")
        
        for m in months:
            for w in range(1, 5):
                for idx, title in enumerate(pool):
                    Topic.objects.create(
                        subject=sub,
                        month=m,
                        week=w,
                        order=idx,
                        title=title
                    )
                    total_added += 1
    
    print(f"Re-aligned {total_added} topics.")
    print("--- REBUILD COMPLETE ---")

absolute_rebuild_curriculum()
