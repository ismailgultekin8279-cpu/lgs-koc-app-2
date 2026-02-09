
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, Subject

def absolute_finalize():
    # POOLS for each subject (strictly unicode escaped)
    POOLS = {
        "Matematik": [
            "Temel \u0130\u015flem Yetene\u011fi",
            "Mant\u0131k Muhakeme Prati\u011fi",
            "Say\u0131sal Analiz \u00c7al\u0131\u015fmas\u0131",
            "LGS Tipi Soru Analizi",
            "H\u0131z Testi ve Zaman Y\u00f6netimi",
            "Hatal\u0131 Soru Analiz Teknikleri",
            "Genel Matematik Tekrar\u0131"
        ],
        "Fen Bilimleri": [
            "Bilimsel Muhakeme Becerisi",
            "Deney Analizi ve Yorumlama",
            "Yeni Nesil Soru \u00c7\u00f6z\u00fcm\u00fc",
            "Fen Bilimleri H\u0131z Testi",
            "Kavram Haritas\u0131 \u00c7al\u0131\u015fmas\u0131",
            "Laboratuvar Sorular\u0131 Analizi",
            "Fen Bilimleri Genel Tekrar"
        ],
        "T\u00fcrk\u00e7e": [
            "Paragraf H\u0131zland\u0131rma",
            "S\u00f6zel Mant\u0131k Becerisi",
            "Okuma Anlama ve Yorum",
            "S\u00f6zc\u00fckte Anlam Prati\u011fi",
            "Yaz\u0131m ve Noktalama Check",
            "Metin T\u00fcrleri Analizi",
            "T\u00fcrk\u00e7e Genel Tekrar"
        ],
        "T.C. \u0130nk\u0131lap Tarihi": [
            "Kronoloji Analiz Becerisi",
            "Harita ve G\u00f6rsel Yorumlama",
            "Kavram Bilgisi Tekrar\u0131",
            "Kaynak Analizi \u00c7al\u0131\u015fmas\u0131",
            "Tarihsel Muhakeme",
            "Olay-Olgu Ayr\u0131m\u0131",
            "\u0130nk\u0131lap Tarihi Genel Tekrar"
        ],
        "Yabanc\u0131 Dil": [
            "Vocabulary Builder (Focus)",
            "Reading Comprehension",
            "Grammar Review and Check",
            "Sentence Parsing Practice",
            "Word Association Games",
            "Translation Exercises",
            "English General Review"
        ],
        "Din K\u00fclt\u00fcr\u00fc": [
            "Metin Analizi ve Yorum",
            "Kavram Tekrar\u0131",
            "Ayet ve Hadis Yorumlama",
            "Ahlaki Tutum Analizi",
            "Dini Terimler S\u00f6zl\u00fc\u011f\u00fc",
            "Din K\u00fclt\u00fcr\u00fc Soru Prati\u011fi",
            "Din Bilgisi Genel Tekrar"
        ]
    }

    months = [9, 10, 11, 12, 1, 2, 3, 4, 5, 6]
    
    print("--- STARTING ABSOLUTE GLOBAL STANDARDIZATION ---")
    
    total_added = 0
    
    for subj_name, pool in POOLS.items():
        sub, _ = Subject.objects.get_or_create(name=subj_name)
        print(f"Processing Subject: {subj_name}...")
        
        for m in months:
            for w in range(1, 5):
                # Count current topics
                # We count all topics to see if we reached the magic 7
                existing_count = Topic.objects.filter(subject=sub, month=m, week=w).count()
                
                if existing_count < 7:
                    needed = 7 - existing_count
                    # Get existing titles to avoid exact duplicates in same week
                    existing_titles = set(Topic.objects.filter(subject=sub, month=m, week=w).values_list('title', flat=True))
                    
                    # Highest order
                    last_topic = Topic.objects.filter(subject=sub, month=m, week=w).order_by('-order').first()
                    start_order = (last_topic.order + 1) if last_topic else 0
                    
                    added_this_week = 0
                    pool_idx = 0
                    while added_this_week < needed and pool_idx < 20: # Safety break
                        title = pool[pool_idx % len(pool)]
                        if title not in existing_titles:
                            Topic.objects.create(
                                subject=sub,
                                month=m,
                                week=w,
                                order=start_order + added_this_week,
                                title=title
                            )
                            existing_titles.add(title)
                            added_this_week += 1
                            total_added += 1
                        pool_idx += 1
    
    print(f"Added {total_added} missing topics globally.")
    print("--- ABSOLUTE GLOBAL STANDARDIZATION COMPLETE ---")

absolute_finalize()
