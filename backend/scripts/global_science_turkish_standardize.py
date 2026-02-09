
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, Subject

def global_refine_science_and_turkish():
    science = Subject.objects.get(name="Fen Bilimleri")
    turkish = Subject.objects.get(name="T\u00fcrk\u00e7e")
    
    # Roadmap for Science
    SCIENCE_ROADMAP = {
        10: { # Ekim
            1: ["H\u00fccre ve B\u00f6l\u00fcnmeler: Mitoz", "Mitoz B\u00f6l\u00fcnme Evreleri", "H\u00fccre B\u00f6l\u00fcnmesi Deney G\u00f6zlemi"],
            2: ["Mayoz B\u00f6l\u00fcnme Temelleri", "Mitoz ve Mayoz Aras\u0131ndaki Farklar", "Genetik \u00c7e\u015fitlilik ve Mayoz"],
            3: ["Kuvvet ve Enerji: K\u00fctle ve A\u011f\u0131rl\u0131k \u0130li\u015fkisi", "Kuvvet, \u0130\u015f ve Enerji \u0130li\u015fkisi", "Potansiyel ve Kinetik Enerji D\u00f6n\u00fc\u015fc\u00fcm\u00fc"],
            4: ["Enerji D\u00f6n\u00fc\u015f\u00fcmleri ve S\u00fcrt\u00fcnme Kuvveti", "Fen Bilimleri Proje Haz\u0131rl\u0131k", "Ekim Ay\u0111 Deney Analizi"]
        },
        11: { # Kas\u0131m
            1: ["Maddenin Tanecikli Yap\u0131s\u0131", "Atomun Yap\u0131s\u0131 ve Tarih\u00e7esi", "Molek\u00fcl ve Saf Maddeler"],
            2: ["Kar\u0131\u015f\u0131mlar ve T\u00fcrleri", "Kar\u0131\u015f\u0131mlar\u0131 Ay\u0131rma Teknikleri", "Evsel At\u0131klar ve Geri D\u00f6n\u00fc\u015f\u00fcm"],
            3: ["I\u015f\u0131\u011f\u0131n So\u011furulmas\u0131 ve Renkler", "G\u00fcne\u015f Enerjisinin Kullan\u0131m Alanlar\u0131", "Radyometre ve I\u015f\u0131k Enerjisi"],
            4: ["Aynalar ve T\u00fcrleri: D\u00fcz, \u00c7ukur, T\u00fcmsek", "I\u015f\u011f\u0131n K\u0131r\u0131lmas\u0131 ve Mercekler", "Kas\u0131m Ara Tatil Fen Kamp\u0131"]
        }
    }

    # Roadmap for Turkish
    TURKISH_ROADMAP = {
        10: { # Ekim
            1: ["S\u00f6zc\u00fckte Anlam: Ger\u00e7ek, Yan, Mecaz", "Terim Anlam ve S\u00f6zc\u00fck \u0130li\u015fkileri", "Deyimler ve Atas\u00f6zleri Analizi"],
            2: ["C\u00fcmlede Anlam: \u00d6znel ve Nesnel Yarg\u0131", "Sebep-Sonu\u00e7, Ama\u00e7-Sonu\u00e7 C\u00fcmleleri", "\u00d6rt\u00fcl\u00fc Anlam ve C\u00fcmle Yorumu"],
            3: ["Paragraf: Ana D\u00fc\u015f\u00fcnce ve Yardımc\u0131 D\u00fc\u015f\u00fcnce", "Paragrafta Yap\u0131 ve Ak\u0131\u015f\u0131 Bozma", "S\u00f6zel Mant\u0131k ve Muhakeme-1"],
            4: ["Fiiller: Anlamlar\u0131na G\u00f6re Fiiller", "Fiillerde Kip ve Ki\u015fi", "Ekim Ay\u0111 Kitap Analizi"]
        },
        11: { # Kas\u0131m
            1: ["S\u00f6z Sanatlar\u0131 ve Metin T\u00fcrleri", "Hikaye unsurlar\u0131 ve Anlat\u0131c\u0131 Bak\u0131\u015f A\u00e7\u0131lar\u0131", "Bilgilendirici ve Hikaye Edici Metinler"],
            2: ["Yaz\u0131m Kurallar\u0131: B\u00fcy\u00fck Harfler ve Says\u0131lar", "Noktalama \u0130\u015faretleri: Nokta, Virg\u00fcl, \u0130ki Nokta", "Yaz\u0131m Yanl\u0131\u015flar\u0131 ve Noktalama Prati\u011fi"],
            3: ["C\u00fcmlede Anlam: Yakla\u015f\u0131mlar ve Kavramlar", "D\u00fc\u015f\u00fcnceyi Geli\u015ftirme Yollar\u0131", "S\u00f6zel Mant\u0131k ve Muhakeme-2"],
            4: ["Kas\u0131m Ara Tatil T\u00fcrk\u00e7e Kamp\u0131", "Paragraf H\u0131z Testi", "T\u00fcrk\u00e7e Karma Deneme Analizi"]
        }
    }

    # Standard Strategic Labels to Pad to 7 Topics
    STRATEGIC_LABELS = [
        "Bilimsel Muhakeme Becerisi",
        "Yeni Nesil Soru Analizi",
        "Zaman Y\u00f6netimi Uygulamas\u0131",
        "Okuma Anlama ve H\u0131zland\u0131rma",
        "S\u00f6zel/Say\u0131sal Mant\u0131k Destek",
        "Haftal\u0131k De\u011ferlendirme",
        "Genel Tekrar ve Peki\u015ftirme"
    ]

    print("--- STANDARDIZING SCIENCE AND TURKISH ---")
    
    # Process both subjects (Ekim and Kas\u0131m for now, scaling logic is same for all months)
    for month in [10, 11]:
        for week in range(1, 5):
            # Science
            print(f"  Science: Month {month}, Week {week}")
            Topic.objects.filter(subject=science, month=month, week=week).delete()
            scie_core = SCIENCE_ROADMAP.get(month, {}).get(week, [])
            scie_final = list(scie_core)
            l_idx = 0
            while len(scie_final) < 7:
                label = STRATEGIC_LABELS[l_idx % len(STRATEGIC_LABELS)]
                if label not in scie_final: scie_final.append(label)
                l_idx += 1
            for idx, title in enumerate(scie_final):
                Topic.objects.create(subject=science, month=month, week=week, order=idx, title=title)
            
            # Turkish
            print(f"  Turkish: Month {month}, Week {week}")
            Topic.objects.filter(subject=turkish, month=month, week=week).delete()
            tur_core = TURKISH_ROADMAP.get(month, {}).get(week, [])
            tur_final = list(tur_core)
            l_idx = 0
            while len(tur_final) < 7:
                label = STRATEGIC_LABELS[l_idx % len(STRATEGIC_LABELS)]
                if label not in tur_final: tur_final.append(label)
                l_idx += 1
            for idx, title in enumerate(tur_final):
                Topic.objects.create(subject=turkish, month=month, week=week, order=idx, title=title)

    print("--- SCIENCE AND TURKISH STANDARDIZATION COMPLETE ---")

global_refine_science_and_turkish()
