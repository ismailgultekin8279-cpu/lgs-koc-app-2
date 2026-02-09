
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Subject, Topic

def populate():
    # 1. Subject creation is now inside the loop
    print("Starting Curriculum Population...")

    # 2. Data from our prototype
    # Define Curriculum Data for All Subjects
    months_map = {
        9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık",
        1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan", 5: "Mayıs", 6: "Haziran"
    }

    curr_data = {
        "Matematik": [
            { "id": 9, "weeks": [ {"week": 1, "topics": ["Pozitif Tam Sayıların Çarpanları", "Asal Çarpanlara Ayırma"]}, {"week": 2, "topics": ["En Büyük Ortak Bölen (EBOB)", "En Küçük Ortak Kat (EKOK)"]}, {"week": 3, "topics": ["EBOB Problemleri", "EKOK Problemleri"]}, {"week": 4, "topics": ["Aralarında Asal Olma Kuralı"]} ]},
            { "id": 10, "weeks": [ {"week": 1, "topics": ["Tam Sayıların Tam Sayı Kuvvetleri"]}, {"week": 2, "topics": ["Üslü İfadelerle İlgili Temel Kurallar"]}, {"week": 3, "topics": ["Sayıların Ondalık Gösterimi", "Çözümleme"]}, {"week": 4, "topics": ["Bilimsel Gösterim"]} ]},
            { "id": 11, "weeks": [ {"week": 1, "topics": ["Kareköklü İfadeler"]}, {"week": 2, "topics": ["Tam Kare Sayılar"]}, {"week": 3, "topics": ["Kareköklü İfadelerde Çarpma/Bölme"]}, {"week": 4, "topics": ["Kareköklü İfadelerde Toplama/Çıkarma"]} ]},
            { "id": 12, "weeks": [ {"week": 1, "topics": ["Gerçek Sayılar"]}, {"week": 2, "topics": ["Veri Analizi (Çizgi ve Sütun Grafikleri)"]}, {"week": 3, "topics": ["Veri Analizi (Daire Grafiği)"]}, {"week": 4, "topics": ["Basit Olayların Olma Olasılığı"]} ]},
            { "id": 1, "weeks": [ {"week": 1, "topics": ["Cebirsel İfadeler"]}, {"week": 2, "topics": ["Cebirsel İfadeleri Çarpanlara Ayırma"]}, {"week": 3, "topics": ["Özdeşlikler"]}, {"week": 4, "topics": ["Doğrusal Denklemler (Koordinat Sistemi)"]} ]},
            { "id": 2, "weeks": [ {"week": 1, "topics": ["Doğrusal İlişkiler"]}, {"week": 2, "topics": ["Eğim"]}, {"week": 3, "topics": ["Eşitsizlikler"]}, {"week": 4, "topics": ["Üçgenler (Yardımcı Elemanlar)"]} ]},
            { "id": 3, "weeks": [ {"week": 1, "topics": ["Üçgen Eşitsizliği"]}, {"week": 2, "topics": ["Pisagor Bağıntısı"]}, {"week": 3, "topics": ["Eşlik ve Benzerlik"]}, {"week": 4, "topics": ["Dönüşüm Geometrisi (Öteleme, Yansıma)"]} ]},
            { "id": 4, "weeks": [ {"week": 1, "topics": ["Geometrik Cisimler (Prizmalar)"]}, {"week": 2, "topics": ["Dik Dairesel Silindir"]}, {"week": 3, "topics": ["Silindirin Hacmi"]}, {"week": 4, "topics": ["Dik Piramit ve Koni"]} ]},
            { "id": 5, "weeks": [ {"week": 1, "topics": ["Eşitsizlikler Genel Tekrar"]}, {"week": 2, "topics": ["Geometri Genel Tekrar"]}, {"week": 3, "topics": ["MEB Örnek Sorular Çözümü"]}, {"week": 4, "topics": ["Deneme Sınavı Analizi"]} ]}, 
            { "id": 6, "weeks": [ {"week": 1, "topics": ["LGS Genel Tekrar - 1"]}, {"week": 2, "topics": ["LGS Genel Tekrar - 2"]}, {"week": 3, "topics": ["Motivasyon ve Stres Yönetimi"]}, {"week": 4, "topics": ["Büyük Gün Hazırlığı"]} ]}
        ],
        "Fen Bilimleri": [
            { "id": 9, "weeks": [ {"week": 1, "topics": ["Mevsimlerin Oluşumu"]}, {"week": 2, "topics": ["İklim ve Hava Hareketleri"]}, {"week": 3, "topics": ["Küresel İklim Değişikliği"]}, {"week": 4, "topics": ["DNA ve Genetik Kod"]} ]},
            { "id": 10, "weeks": [ {"week": 1, "topics": ["Kalıtım (Mendel Genetiği)"]}, {"week": 2, "topics": ["Mutasyon ve Modifikasyon"]}, {"week": 3, "topics": ["Adaptasyon"]}, {"week": 4, "topics": ["Biyoteknoloji"]} ]},
            { "id": 11, "weeks": [ {"week": 1, "topics": ["Basınç (Katı Basıncı)"]}, {"week": 2, "topics": ["Sıvı Basıncı"]}, {"week": 3, "topics": ["Gaz Basıncı"]}, {"week": 4, "topics": ["Periyodik Sistem"]} ]},
            { "id": 12, "weeks": [ {"week": 1, "topics": ["Fiziksel ve Kimyasal Değişimler"]}, {"week": 2, "topics": ["Kimyasal Tepkimeler"]}, {"week": 3, "topics": ["Asitler ve Bazlar"]}, {"week": 4, "topics": ["Maddenin Isı ile Etkileşimi"]} ]},
            { "id": 1, "weeks": [ {"week": 1, "topics": ["Basit Makineler (Makaralar)"]}, {"week": 2, "topics": ["Kaldıraçlar"]}, {"week": 3, "topics": ["Eğik Düzlem ve Çıkrık"]}, {"week": 4, "topics": ["Basit Makineler (Dişli Çarklar, Kasnaklar)"]} ]},
            { "id": 2, "weeks": [ {"week": 1, "topics": ["Besin Zinciri ve Enerji Akışı"]}, {"week": 2, "topics": ["Enerji Dönüşümleri (Fotosentez)"]}, {"week": 3, "topics": ["Enerji Dönüşümleri (Solunum)"]}, {"week": 4, "topics": ["Madde Döngüleri"]} ]},
            { "id": 3, "weeks": [ {"week": 1, "topics": ["Elektrik Yükleri ve Elektriklenme"]}, {"week": 2, "topics": ["Elektrik Yüklü Cisimler"]}, {"week": 3, "topics": ["Elektrik Enerjisinin Dönüşümü"]}, {"week": 4, "topics": ["Sürdürülebilir Kalkınma"]} ]},
            { "id": 4, "weeks": [ {"week": 1, "topics": ["Elektrik Yükleri (Tekrar)"]}, {"week": 2, "topics": ["Çevre Bilimi ve İklim Değişikliği"]}, {"week": 3, "topics": ["DNA ve Genetik Kod (Tekrar)"]}, {"week": 4, "topics": ["Basınç (Tekrar)"]} ]},
            { "id": 5, "weeks": [ {"week": 1, "topics": ["Basit Makineler Genel Tekrar"]}, {"week": 2, "topics": ["Madde ve Endüstri Genel Tekrar"]}, {"week": 3, "topics": ["Fen Bilimleri Deneme 1"]}, {"week": 4, "topics": ["Fen Bilimleri Deneme 2"]} ]},
            { "id": 6, "weeks": [ {"week": 1, "topics": ["Son Genel Tekrar - Fizik"]}, {"week": 2, "topics": ["Son Genel Tekrar - Kimya/Biyoloji"]}, {"week": 3, "topics": ["Çıkmış Sorular Çözümü"]}, {"week": 4, "topics": ["Sınav Stratejileri"]} ]}
        ],
        "Türkçe": [
            { "id": 9, "weeks": [ {"week": 1, "topics": ["Fiilimsiler (İsim-Fiil)"]}, {"week": 2, "topics": ["Fiilimsiler (Sıfat-Fiil)"]}, {"week": 3, "topics": ["Fiilimsiler (Zarf-Fiil)"]}, {"week": 4, "topics": ["Sözcükte Anlam"]} ]},
            { "id": 10, "weeks": [ {"week": 1, "topics": ["Cümlenin Ögeleri (Temel Ögeler)"]}, {"week": 2, "topics": ["Cümlenin Ögeleri (Yardımcı Ögeler)"]}, {"week": 3, "topics": ["Cümle Vurgusu"]}, {"week": 4, "topics": ["Paragrafta Anlam"]} ]},
            { "id": 11, "weeks": [ {"week": 1, "topics": ["Fiilde Çatı (Özne-Yüklem)"]}, {"week": 2, "topics": ["Fiilde Çatı (Nesne-Yüklem)"]}, {"week": 3, "topics": ["Cümle Türleri (Anlamına Göre)"]}, {"week": 4, "topics": ["Cümle Türleri (Yapısına Göre)"]} ]},
            { "id": 12, "weeks": [ {"week": 1, "topics": ["Yazım Kuralları"]}, {"week": 2, "topics": ["Noktalama İşaretleri"]}, {"week": 3, "topics": ["Metin Türleri"]}, {"week": 4, "topics": ["Söz Sanatları"]} ]},
            { "id": 1, "weeks": [ {"week": 1, "topics": ["Anlatım Bozuklukları (Ögeler)"]}, {"week": 2, "topics": ["Anlatım Bozuklukları (Anlam)"]}, {"week": 3, "topics": ["Paragraf (Ana Düşünce)"]}, {"week": 4, "topics": ["Paragraf (Yardımcı Düşünce)"]} ]},
            { "id": 2, "weeks": [ {"week": 1, "topics": ["Sözel Mantık (Giriş)"]}, {"week": 2, "topics": ["Sözel Mantık (Tablo Okuma)"]}, {"week": 3, "topics": ["Grafik ve Görsel Yorumlama"]}, {"week": 4, "topics": ["Deyimler ve Atasözleri"]} ]},
            { "id": 3, "weeks": [ {"week": 1, "topics": ["Paragrafta Yapı"]}, {"week": 2, "topics": ["Sözel Mantık (İleri Seviye)"]}, {"week": 3, "topics": ["Yazım ve Noktalama Tekrar"]}, {"week": 4, "topics": ["Fiilimsiler Tekrar"]} ]},
            { "id": 4, "weeks": [ {"week": 1, "topics": ["Cümlenin Ögeleri Tekrar"]}, {"week": 2, "topics": ["Cümle Türleri Tekrar"]}, {"week": 3, "topics": ["Türkçe Genel Deneme"]}, {"week": 4, "topics": ["Paragraf Hızlandırma Taktikleri"]} ]},
            { "id": 5, "weeks": [ {"week": 1, "topics": ["Sözel Mantık Çıkmış Sorular"]}, {"week": 2, "topics": ["Dil Bilgisi Karma Tekrar"]}, {"week": 3, "topics": ["MEB Örnek Sorular"]}, {"week": 4, "topics": ["Deneme Analizi"]} ]},
            { "id": 6, "weeks": [ {"week": 1, "topics": ["Son Bakış: Yazım Kuralları"]}, {"week": 2, "topics": ["Son Bakış: Noktalama"]}, {"week": 3, "topics": ["Motivasyon"]}, {"week": 4, "topics": ["Sınav Hazırlığı"]} ]}
        ],
        "T.C. İnkılap Tarihi": [
            { "id": 9, "weeks": [ {"week": 1, "topics": ["Bir Kahraman Doğuyor"]}, {"week": 2, "topics": ["Milli Uyanış"]}, {"week": 3, "topics": ["Milli Mücadele Hazırlık"]}, {"week": 4, "topics": ["TBMM'nin Açılması"]} ]},
            { "id": 10, "weeks": [ {"week": 1, "topics": ["Doğu ve Güney Cepheleri"]}, {"week": 2, "topics": ["Batı Cephesi"]}, {"week": 3, "topics": ["Sakarya Meydan Savaşı"]}, {"week": 4, "topics": ["Büyük Taarruz"]} ]},
            { "id": 11, "weeks": [ {"week": 1, "topics": ["Atatürkçülük ve Türk İnkılabı"]}, {"week": 2, "topics": ["Siyasi Alanda İnkılaplar"]}, {"week": 3, "topics": ["Hukuk Alanında İnkılaplar"]}, {"week": 4, "topics": ["Eğitim Alanında İnkılaplar"]} ]},
            { "id": 12, "weeks": [ {"week": 1, "topics": ["Toplumsal Alanda İnkılaplar"]}, {"week": 2, "topics": ["Ekonomi Alanında İnkılaplar"]}, {"week": 3, "topics": ["Atatürk Dönemi Türk Dış Politikası"]}, {"week": 4, "topics": ["Atatürk'ün Ölümü ve Sonrası"]} ]},
            { "id": 1, "weeks": [ {"week": 1, "topics": ["Demokratikleşme Çabaları"]}, {"week": 2, "topics": ["Atatürk Dönemi Dış Politika (1923-1930)"]}, {"week": 3, "topics": ["Atatürk Dönemi Dış Politika (1930-1938)"]}, {"week": 4, "topics": ["Atatürk'ün Ölümü ve Yankıları"]} ]}, 
            { "id": 2, "weeks": [ {"week": 1, "topics": ["İkinci Dünya Savaşı ve Türkiye"]}, {"week": 2, "topics": ["Çok Partili Hayata Geçiş"]}, {"week": 3, "topics": ["Genel Tekrar: Ünite 1"]}, {"week": 4, "topics": ["Genel Tekrar: Ünite 2"]} ]},
            { "id": 3, "weeks": [ {"week": 1, "topics": ["Genel Tekrar: Milli Mücadele"]}, {"week": 2, "topics": ["Genel Tekrar: İnkılaplar"]}, {"week": 3, "topics": ["Harita Yorumlama"]}, {"week": 4, "topics": ["Kronoloji Çalışması"]} ]},
            { "id": 4, "weeks": [ {"week": 1, "topics": ["Kavram Bilgisi (Siyasi, Hukuki)"]}, {"week": 2, "topics": ["Kavram Bilgisi (Sosyal, Ekonomik)"]}, {"week": 3, "topics": ["Örnek Sorular Çözümü"]}, {"week": 4, "topics": ["Deneme Sınavı 1"]} ]},
            { "id": 5, "weeks": [ {"week": 1, "topics": ["T.C. İnkılap Tarihi Deneme 2"]}, {"week": 2, "topics": ["Çıkmış Sorular Analizi"]}, {"week": 3, "topics": ["Nokta Atışı Bilgiler"]}, {"week": 4, "topics": ["Son Eksik Tamamlama"]} ]},
            { "id": 6, "weeks": [ {"week": 1, "topics": ["Genel Tekrar"]}, {"week": 2, "topics": ["Motivasyon"]} ]}
        ],
        "Din Kültürü": [
            { "id": 9, "weeks": [ {"week": 1, "topics": ["Kader İnancı"]}, {"week": 2, "topics": ["Zekat ve Sadaka"]}, {"week": 3, "topics": ["Din ve Hayat"]}, {"week": 4, "topics": ["Hz. Muhammed'in Örnekliği"]} ]},
            { "id": 10, "weeks": [ {"week": 1, "topics": ["Kuran-ı Kerim ve Özellikleri"]}, {"week": 2, "topics": ["Ayetler ve Sureler"]}, {"week": 3, "topics": ["Hz. Yusuf Kıssası"]}, {"week": 4, "topics": ["Asr Suresi"]} ]},
            { "id": 11, "weeks": [ {"week": 1, "topics": ["İslam'ın Paylaşma ve Yardımlaşmaya Verdiği Önem"]}, {"week": 2, "topics": ["Zekat ve Sadaka İbadeti (Detay)"]}, {"week": 3, "topics": ["Maun Suresi"]}, {"week": 4, "topics": ["Din, Birey ve Toplum"]} ]},
            { "id": 12, "weeks": [ {"week": 1, "topics": ["Dinin Temel Gayesi"]}, {"week": 2, "topics": ["Hz. Şuayb (a.s.)"]}, {"week": 3, "topics": ["Hz. Muhammed'in Doğruluğu"]}, {"week": 4, "topics": ["Hz. Muhammed'in Merhameti"]} ]},
            { "id": 1, "weeks": [ {"week": 1, "topics": ["Hz. Muhammed'in Adaleti"]}, {"week": 2, "topics": ["Hz. Muhammed'in Cesareti"]}, {"week": 3, "topics": ["Hz. Muhammed'in İstişareye Önemi"]}, {"week": 4, "topics": ["Kureyş Suresi"]} ]},
            { "id": 2, "weeks": [ {"week": 1, "topics": ["Kuran-ı Kerim'in Ana Konuları"]}, {"week": 2, "topics": ["İslam Dininin Korunması"]}, {"week": 3, "topics": ["Canın ve Malın Korunması"]}, {"week": 4, "topics": ["Aklın ve Neslin Korunması"]} ]},
            { "id": 3, "weeks": [ {"week": 1, "topics": ["Hz. Nuh (a.s.)"]}, {"week": 2, "topics": ["Kadir Suresi"]}, {"week": 3, "topics": ["Ünite Tekrar: Kader"]}, {"week": 4, "topics": ["Ünite Tekrar: Zekat"]} ]},
            { "id": 4, "weeks": [ {"week": 1, "topics": ["Ünite Tekrar: Din ve Hayat"]}, {"week": 2, "topics": ["Ünite Tekrar: Hz. Muhammed"]}, {"week": 3, "topics": ["Deneme Çözümü 1"]}, {"week": 4, "topics": ["Deneme Çözümü 2"]} ]},
            { "id": 5, "weeks": [ {"week": 1, "topics": ["Kavram Çalışması"]}, {"week": 2, "topics": ["Ayet ve Hadis Yorumlama"]}, {"week": 3, "topics": ["Çıkmış Sorular"]}, {"week": 4, "topics": ["Son Tekrar"]} ]},
            { "id": 6, "weeks": [ {"week": 1, "topics": ["Final Tekrarı"]}, {"week": 2, "topics": ["Motivasyon"]} ]}
        ],
        "Yabancı Dil": [
            { "id": 9, "weeks": [ {"week": 1, "topics": ["Unit 1: Friendship"]}, {"week": 2, "topics": ["Accepting and Refusing"]}, {"week": 3, "topics": ["Unit 2: Teen Life"]}, {"week": 4, "topics": ["Regular Actions"]} ]},
            { "id": 10, "weeks": [ {"week": 1, "topics": ["Unit 3: In The Kitchen"]}, {"week": 2, "topics": ["Process and Recipes"]}, {"week": 3, "topics": ["Unit 4: On The Phone"]}, {"week": 4, "topics": ["Phone Conversations"]} ]},
            { "id": 11, "weeks": [ {"week": 1, "topics": ["Unit 5: The Internet"]}, {"week": 2, "topics": ["Internet Safety"]}, {"week": 3, "topics": ["Unit 6: Adventures"]}, {"week": 4, "topics": ["Extreme Sports"]} ]},
            { "id": 12, "weeks": [ {"week": 1, "topics": ["Comparisons"]}, {"week": 2, "topics": ["Preferences"]}, {"week": 3, "topics": ["Unit 7: Tourism"]}, {"week": 4, "topics": ["Experiences"]} ]},
            { "id": 1, "weeks": [ {"week": 1, "topics": ["Unit 8: Chores"]}, {"week": 2, "topics": ["Obligations"]}, {"week": 3, "topics": ["Unit 9: Science"]}, {"week": 4, "topics": ["Scientific Achievements"]} ]},
            { "id": 2, "weeks": [ {"week": 1, "topics": ["Unit 10: Natural Forces"]}, {"week": 2, "topics": ["Predictions"]}, {"week": 3, "topics": ["Future Tense"]}, {"week": 4, "topics": ["General Revision: Units 1-5"]} ]},
            { "id": 3, "weeks": [ {"week": 1, "topics": ["General Revision: Units 6-10"]}, {"week": 2, "topics": ["Vocabulary Quiz"]}, {"week": 3, "topics": ["Reading Comprehension"]}, {"week": 4, "topics": ["Dialogue Completion"]} ]},
            { "id": 4, "weeks": [ {"week": 1, "topics": ["LGS Practice Exam 1"]}, {"week": 2, "topics": ["LGS Practice Exam 2"]}, {"week": 3, "topics": ["Important Vocabulary List"]}, {"week": 4, "topics": ["Common Expressions"]} ]},
            { "id": 5, "weeks": [ {"week": 1, "topics": ["Last Look: Friendship & Teen Life"]}, {"week": 2, "topics": ["Last Look: Internet & Adventures"]}, {"week": 3, "topics": ["Last Look: Chores & Science"]}, {"week": 4, "topics": ["Mock Exam"]} ]},
            { "id": 6, "weeks": [ {"week": 1, "topics": ["Final Revision"]}, {"week": 2, "topics": ["Exam Strategies"]} ]}
        ]
    }

    # 3. Insert Topics
    total_count = 0
    
    for subject_name, months in curr_data.items():
        # Ensure subject exists
        subject_obj, _ = Subject.objects.get_or_create(name=subject_name)
        print(f"Processing Subject: {subject_obj.name}")
        
        for month in months:
            m_id = month["id"]
            for week_data in month["weeks"]:
                w_id = week_data["week"]
                for index, title in enumerate(week_data["topics"]):
                    topic, created = Topic.objects.get_or_create(
                        subject=subject_obj,
                        title=title,
                        month=m_id,
                        week=w_id,
                        defaults={"order": index}
                    )
                    if created:
                        total_count += 1
                        
    print(f"Successfully created {total_count} new topics across all subjects.")

if __name__ == '__main__':
    populate()
