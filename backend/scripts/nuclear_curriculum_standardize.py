
import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, Subject

def nuclear_standardization():
    print("--- STARTING NUCLEAR CURRICULUM STANDARDIZATION ---")
    
    # 1. Subjects Mapping
    SUBJECT_MAP = {
        "Matematik": [
            "Pozitif Tam Sayıların Çarpanları", "Asal Çarpanlara Ayırma", "EBOB-EKOK", "EBOB-EKOK Problemleri",
            "Üslü İfadeler Giriş", "Tam Sayıların Kuvvetleri", "Ondalık Gösterim ve Çözümleme", "Üslü Sayılarda İşlemler",
            "Kareköklü İfadeler Giriş", "Tam Kare Sayılar", "Karekök Tahmini Değer", "Karekök İşlemleri",
            "Veri Analizi: Grafikler", "Olasılık Temel Kavramlar", "Basit Olayların Olasılığı", 
            "Cebirsel İfadeler Giriş", "Özdeşlikler", "Çarpanlara Ayırma", "Doğrusal Denklemler", 
            "Eğim ve Grafikler", "Eşitsizlikler", "Üçgenler", "Pisagor Bağıntısı", "Eşlik ve Benzerlik",
            "Dönüşüm Geometrisi", "Geometrik Cisimler"
        ],
        "Fen Bilimleri": [
            "Mevsimlerin Oluşumu", "İklim ve Hava Hareketleri", "DNA ve Genetik Kod", "Kalıtım", "Mutasyon ve Modifikasyon",
            "Adaptasyon", "Biyoteknoloji", "Basınç: Katı Basıncı", "Basınç: Sıvı ve Gaz", "Periyodik Sistem",
            "Fiziksel ve Kimyasal Değişimler", "Kimyasal Tepkimeler", "Asitler ve Bazlar", "Maddenin Isı ile Etkileşimi",
            "Türkiye'de Kimya Endüstrisi", "Basit Makineler", "Besin Zinciri ve Enerji Akışı", "Fotosentez", 
            "Solunum", "Madde Döngüleri", "Sürdürülebilir Kalkınma", "Elektrik Yükleri ve Elektriklenme",
            "Elektrik Yüklü Cisimler", "Elektrik Enerjisinin Dönüşümü"
        ],
        "Türkçe": [
            "Fiilimsiler", "Sözcükte Anlam", "Cümlede Anlam", "Paragrafta Anlam", "Yazım Kuralları",
            "Noktalama İşaretleri", "Cümlenin Ögeleri", "Fiilde Çatı", "Cümle Türleri", "Anlatım Bozuklukları",
            "Söz Sanatları", "Metin Türleri", "Sözel Mantık ve Muhakeme", "Görsel Okuma ve Grafik Yorumlama"
        ],
        "T.C. İnkılap Tarihi": [
            "Bir Kahraman Doğuyor", "Milli Uyanış: Bağımsızlık Yolunda Atılan Adımlar", "Milli Bir Destan: Ya İstiklal Ya Ölüm",
            "Atatürkçülük ve Çağdaşlaşan Türkiye", "Demokratikleşme Çabaları", "Atatürk Dönemi Türk Dış Politikası",
            "Atatürk'ün Ölümü ve Sonrası"
        ],
        "Yabancı Dil": [
            "Friendship", "Teen Life", "In the Kitchen", "On the Phone", "The Internet",
            "Adventures", "Tourism", "Chores", "Science", "Natural Forces"
        ],
        "Din Kültürü": [
            "Kader İnancı", "Zekat ve Sadaka", "Din ve Hayat", "Hz. Muhammedin Örnekliği", "Kur'an-ı Kerim ve Özellikleri"
        ]
    }

    STRATEGIC_LABELS = [
        "Temel Beceri Gelişimi",
        "Yeni Nesil Soru Çözümü",
        "Mantık Muhakeme Pratiği",
        "Hız ve Zaman Yönetimi",
        "Hatalı Soru Analizi",
        "Kavram Haritası Çalışması",
        "Genel Tekrar ve Değerlendirme"
    ]

    MONTH_NAMES = {9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık", 1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan", 5: "Mayıs", 6: "Haziran"}

    # Clear existing topics
    print("Wiping existing topics...")
    Topic.objects.all().delete()

    for subj_name, main_topics in SUBJECT_MAP.items():
        subject, _ = Subject.objects.get_or_create(name=subj_name)
        print(f"Standardizing {subj_name}...")
        
        topic_idx = 0
        for month in [9, 10, 11, 12, 1, 2, 3, 4, 5, 6]:
            for week in [1, 2, 3, 4]:
                # Build 7 topics for this specific week
                week_list = []
                
                # Pick 2-3 main topics if available, cycling through
                for _ in range(2 if subj_name in ["Din Kültürü", "Yabancı Dil", "T.C. İnkılap Tarihi"] else 3):
                    cur_topic = main_topics[topic_idx % len(main_topics)]
                    week_list.append(cur_topic)
                    topic_idx += 1
                
                # Pad with Strategic Labels
                label_idx = 0
                while len(week_list) < 7:
                    label = STRATEGIC_LABELS[label_idx % len(STRATEGIC_LABELS)]
                    # GUARANTEE UNIQUENESS: Add Month/Week suffix to EVERYTHING
                    # (Even the main topics)
                    label_idx += 1
                
                # Create with unique suffix
                month_name = MONTH_NAMES[month]
                for order, base_title in enumerate(week_list):
                    unique_title = f"{base_title} ({month_name} {week}. Hafta)"
                    Topic.objects.create(
                        subject=subject,
                        month=month,
                        week=week,
                        order=order,
                        title=unique_title
                    )
                
                # Pad remaining with standard review labels if needed
                for order in range(len(week_list), 7):
                    label = STRATEGIC_LABELS[order % len(STRATEGIC_LABELS)]
                    unique_label = f"{label} ({month_name} {week}. Hafta)"
                    Topic.objects.create(
                        subject=subject,
                        month=month,
                        week=week,
                        order=order,
                        title=unique_label
                    )

    print("--- NUCLEAR STANDARDIZATION COMPLETE ---")

if __name__ == "__main__":
    nuclear_standardization()
