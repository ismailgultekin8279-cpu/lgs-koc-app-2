
import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, Subject

def nuclear_standardization():
    print("--- STARTING OPTIMIZED NUCLEAR CURRICULUM STANDARDIZATION ---")
    
    # 1. Subjects Mapping
    SUBJECT_MAP = {
        "Matematik": [
            "Pozitif Tam Sayıların Çarpanları", "Asal Çarpanlara Ayırma", "EBOB-EKOK", "EBOB-EKOK Problemleri",
            "Üslü İfadeler Giriş", "Tam Sayıların Kuvvetleri", "Ondalık Gösterim ve Çözümleme", "Üslü Sayılarda İşlemler",
            "Kareköklü İfadeler Giriş", "Tam Kare Sayılar", "Karekök Tahmini Değer", "Karekök İşlemleri"
        ],
        "Fen Bilimleri": [
            "Mevsimlerin Oluşumu", "İklim ve Hava Hareketleri", "DNA ve Genetik Kod", "Kalıtım", "Mutasyon ve Modifikasyon",
            "Adaptasyon", "Biyoteknoloji", "Basınç: Katı Basıncı", "Basınç: Sıvı ve Gaz", "Periyodik Sistem"
        ],
        "Türkçe": [
            "Fiilimsiler", "Sözcükte Anlam", "Cümlede Anlam", "Paragrafta Anlam", "Yazım Kuralları",
            "Noktalama İşaretleri", "Cümlenin Ögeleri", "Fiilde Çatı", "Cümle Türleri"
        ],
        "T.C. İnkılap Tarihi": [
            "Bir Kahraman Doğuyor", "Milli Uyanış: Bağımsızlık Yolunda Adımlar", "Milli Bir Destan",
            "Atatürkçülük ve Çağdaşlaşan Türkiye", "Demokratikleşme Çabaları"
        ],
        "Yabancı Dil": [
            "Friendship", "Teen Life", "In the Kitchen", "On the Phone", "The Internet",
            "Adventures", "Tourism"
        ],
        "Din Kültürü": [
            "Kader İnancı", "Zekat ve Sadaka", "Din ve Hayat", "Hz. Muhammedin Örnekliği"
        ]
    }

    STRATEGIC_LABELS = [
        "Temel Beceri Gelişimi", "Yeni Nesil Soru Çözümü", "Mantık Muhakeme Pratiği",
        "Hız ve Zaman Yönetimi", "Hatalı Soru Analizi", "Kavram Haritası Çalışması", "Genel Tekrar"
    ]

    MONTH_NAMES = {9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık", 1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan", 5: "Mayıs", 6: "Haziran"}

    print("Wiping existing topics...")
    Topic.objects.all().delete()

    all_topics_to_create = []

    for subj_name, main_topics in SUBJECT_MAP.items():
        subject, _ = Subject.objects.get_or_create(name=subj_name)
        print(f"Preparing {subj_name}...")
        
        topic_idx = 0
        for month in range(1, 13):
            if month not in MONTH_NAMES: continue
            for week in [1, 2, 3, 4]:
                week_list = []
                
                # Main topics
                for _ in range(2 if len(main_topics) < 10 else 3):
                    cur_topic = main_topics[topic_idx % len(main_topics)]
                    week_list.append(cur_topic)
                    topic_idx += 1
                
                month_name = MONTH_NAMES[month]
                # Pad to 7 items
                for order in range(7):
                    if order < len(week_list):
                        base_title = week_list[order]
                    else:
                        base_title = STRATEGIC_LABELS[order % len(STRATEGIC_LABELS)]
                    
                    unique_title = f"{base_title} ({month_name} {week}. Hafta)"
                    all_topics_to_create.append(Topic(
                        subject=subject,
                        month=month,
                        week=week,
                        order=order,
                        title=unique_title
                    ))

    print(f"Bulk creating {len(all_topics_to_create)} topics...")
    Topic.objects.bulk_create(all_topics_to_create)

    print("--- OPTIMIZED NUCLEAR STANDARDIZATION COMPLETE ---")

if __name__ == "__main__":
    nuclear_standardization()
