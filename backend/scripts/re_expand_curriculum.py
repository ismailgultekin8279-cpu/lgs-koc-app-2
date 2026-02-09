
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, Subject

def expand():
    # Multi-subject mapping with clean labels
    SUBJECT_MAP = {
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
            "Okuma Anlama \u00c7al\u0131\u015fmas\u0131",
            "S\u00f6zel Mant\u0131k Becerisi",
            "Yaz\u0131m Kurallar\u0131 Tekrar\u0131",
            "Noktalama \u0130\u015faretleri Prati\u011fi",
            "G\u00fcnl\u00fck Soru Analizi"
        ],
        "Fen Bilimleri": [
            "Bilimsel S\u00fcre\u00e7 Becerileri",
            "Deney Analizi ve Yorumlama",
            "Fen Bilimleri Soru \u00c7\u00f6z\u00fcm\u00fc",
            "Grafeik Okuma ve Yorumlama",
            "Hipotez Kurma Prati\u011fi",
            "Fen Bilimleri Genel Tekrar",
            "Beceri Temelli Sorular"
        ],
        "Din K\u00fclt\u00fcr\u00fc": [
            "Metin Analizi ve Yorum",
            "Kavram Tekrar\u0131",
            "Din K\u00fclt\u00fcr\u00fc Genel Tekrar"
        ],
        "T.C. \u0130nk\u0131lap Tarihi": [
            "Kronolojik Analiz Becerisi",
            "Harita Okuma ve Yorumlama",
            "\u0130nk\u0131lap Tarihi Soru Prati\u011fi"
        ],
        "Yabanc\u0131 Dil": [
            "Vocabulary Builder",
            "Reading Comprehension",
            "Grammar Review"
        ]
    }

    months = [9, 10, 11, 12, 1, 2, 3, 4, 5, 6]
    
    print("Expanding curriculum for ALL subjects...")
    
    for m in months:
        for w in range(1, 5):
            print(f"  Month {m}, Week {w}...")
            for subj_name, topics_list in SUBJECT_MAP.items():
                sub, _ = Subject.objects.get_or_create(name=subj_name)
                
                # Check current count
                current_count = Topic.objects.filter(subject=sub, month=m, week=w, order__lt=20).count()
                
                # Minimum target
                if subj_name == "Matematik": target = 7
                elif subj_name in ["T\u00fcrk\u00e7e", "Fen Bilimleri"]: target = 3
                else: target = 1 # At least one for social sciences
                
                added = 0
                if current_count < target:
                    needed = target - current_count
                    for i in range(needed):
                        title = topics_list[i % len(topics_list)]
                        Topic.objects.get_or_create(
                            subject=sub, month=m, week=w, order=20+i,
                            defaults={"title": title}
                        )
                        added += 1
                if added:
                    print(f"    Added {added} topics to {subj_name}")

    print("Curriculum expansion complete.")

expand()
