
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, Subject

def refine():
    math = Subject.objects.get(name="Matematik")
    
    # 1. Definitve Math Plan for September (Weeks 1-4)
    # Each list has exactly 7 topics in Order 0-6.
    PLAN = {
        1: [
            "Pozitif Tam Say\u0131lar\u0131n \u00c7arpanlar\u0131",
            "Asal \u00c7arpanlara Ay\u0131rma",
            "Temel \u0130\u015flem Yetene\u011fi",
            "Mant\u0131k Muhakeme (Giri\u015f)",
            "Say\u0131sal Analiz Becerisi",
            "Problem \u00c7\u00f6zme Stratejileri",
            "\u0130\u015flem H\u0131z\u0131 Geli\u015ftirme"
        ],
        2: [
            "En B\u00fcy\u00fck Ortak B\u00f6len (EBOB)",
            "En K\u00fc\u00e7\u00fck Ortak Kat (EKOK)",
            "EBOB-EKOK Problemleri",
            "Mant\u0131k Muhakeme Prati\u011fi",
            "Say\u0131sal Analiz \u00c7al\u0131\u015fmas\u0131",
            "LGS Tipi Soru Analizi",
            "\u0130leri D\u00fczey \u0130\u015flem H\u0131z\u0131"
        ],
        3: [
            "EBOB-EKOK Genel Uygulama",
            "Problem \u00c7\u00f6zme Stratejileri (EBOB-EKOK)",
            "Yeni Nesil Soru Yakla\u015f\u0131mlar\u0131",
            "Veri Analizi ve Yorumlama",
            "S\u00f6zel Mant\u0131k Destekli Say\u0131lar",
            "Matematiksel Ak\u0131l Y\u00fcr\u00fctme",
            "3. Hafta Genel Tekrar"
        ],
        4: [
            "Aralar\u0131nda Asal Olma Kural\u0131",
            "Asall\u0131k ve B\u00f6l\u00fcnebilme \u0130li\u015fkisi",
            "1. \u00dcnite Karma Soru \u00c7\u00f6z\u00fcm\u00fc",
            "LGS \u00c7\u0131km\u0131\u015f Soru Analizi",
            "Zaman Y\u00f6netimi ve H\u0131z Testi",
            "Hatal\u0131 Soru Analiz Teknikleri",
            "Eyl\u00fcl Ay\u0131 De\u011ferlendirme"
        ]
    }

    print("--- REFINING MATHEMATICS CURRICULUM (SEPTEMBER) ---")
    
    for w, topics_list in PLAN.items():
        print(f"Processing Week {w}...")
        
        # 1. DELETE ALL existing Math topics for this week to avoid order conflicts/duplicates
        Topic.objects.filter(subject=math, month=9, week=w).delete()
        
        # 2. CREATE exactly 7 clean topics
        for idx, title in enumerate(topics_list):
            Topic.objects.create(
                subject=math,
                month=9,
                week=w,
                order=idx,
                title=title
            )
            print(f"  Created: {idx} - {title}")

    print("--- REFINEMENT COMPLETE ---")

refine()
