
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, Subject

def global_refine_math():
    math = Subject.objects.get(name="Matematik")
    
    # Roadmap for Mathematics (Monthly/Weekly)
    # Each list must eventually be padded to 7 unique topics using coaching labels if core topics are few.
    ROADMAP = {
        10: { # Ekim
            1: ["\u00dcsl\u00fc \u0130fadeler Giri\u015f", "Tam Say\u0131lar\u0131n Kuvvetleri", "Ondal\u0131k G\u00f6sterim ve \u00c7\u00f6z\u00fcmleme"],
            2: ["\u00dcsl\u00fc \u0130fadelerde \u00c7arpma ve B\u00f6lme", "\u00dcsl\u00fc Denklemler", "\u00dcsl\u00fc Say\u0131 Problemleri"],
            3: ["\u00dcsl\u00fc \u0130fadeler Yeni Nesil Sorular", "\u00c7ok B\u00fcy\u00fck ve \u00c7ok K\u00fc\u00e7\u00fck Say\u0131lar", "Bilimsel G\u00f6sterim"],
            4: ["Karek\u00f6kl\u00fc \u0130fadelere Giri\u015f", "Tam Kare Say\u0131lar", "Karek\u00f6kl\u00fc \u0130fadelerin Tahmini De\u011feri"]
        },
        11: { # Kas\u0131m
            1: ["Karek\u00f6k D\u0131\u015f\u0131na \u00c7\u0131karma ve \u0130\u00e7eri Alma", "Karek\u00f6kl\u00fc Say\u0131larda S\u0131ralama", "Karek\u00f6kl\u00fc \u0130fadelerde \u00c7arpma ve B\u00f6lme"],
            2: ["Karek\u00f6kl\u00fc \u0130fadelerde Toplama ve \u00c7\u0131karma", "Ondal\u0131k \u0130fadelerin Karek\u00f6kleri", "Ger\u00e7ek Say\u0131lar (\u0130rrasyonel)"],
            3: ["Veri Analizi: \u00c7izgi ve S\u00fctun Grafikleri", "Daire Grafi\u011fi ve Yorumlama", "Grafikler Aras\u0131 D\u00f6n\u00fc\u015f\u00fcmler"],
            4: ["Kas\u0131m Ara Tatil Genel Tekrar\u0131", "LGS \u0130lk \u00dcniteler Karma Test", "Problem \u00c7\u00f6zme H\u0131z\u0131 Testi"]
        },
        12: { # Aral\u0131k
            1: ["Basit Olaylar\u0131n Olma Olas\u0131l\u0131\u011f\u0131", "Olas\u0131 Durumlar\u0131 Belirleme", "\u0130mkanl\u0131 ve \u0130mkans\u0131z Olaylar"],
            2: ["Cebirsel \u0130fadelere Giri\u015f", "Cebirsel \u0130fadelere Modelleyerek \u00c7arpma", "\u00d6zde\u015flikler (Tam Kare ve \u0130ki Kare Fark\u0131)"],
            3: ["\u00d6zde\u015flikler ve Cebirsel \u0130fadeler Kartlar\u0131", "\u00c7arpanlara Ay\u0131rma Teknikleri", "Cebirsel \u0130fadeler Yeni Nesil Soru \u00c7\u00f6z\u00fcm\u00fc"],
            4: ["Cebirsel \u0130fadeler Karma Uygulama", "Aral\u0131k Ay\u0131 Genel De\u011ferlendirme", "Mant\u0131k Muhakeme (Aral\u0131k)"]
        },
        1: { # Ocak
            1: ["Do\u011frusal Denklemlere Giri\u015f", "Birinci Dereceden Bir Bilinmeyenli Denklemler", "Denklem Kurma Problemleri"],
            2: ["Koordinat Sistemi ve S\u0131ral\u0131 \u0130kililer", "Do\u011frusal \u0130li\u015fkiler ve Tablo Yorumlama", "Do\u011frusal Denklem Grafikleri"],
            3: ["1. D\u00f6nem Genel Tekrar Kamp\u0131-1", "1. D\u00f6nem Genel Tekrar Kamp\u0131-2", "Yar\u0131y\u0131l Haz\u0131rl\u0131k Denemesi"],
            4: ["Yar\u0131y\u0131l Tatili \u00d6dev Takibi", "Eksik Konu Analizi", "Motivasyonel Dinlenme ve Planlama"]
        },
        2: { # \u015eubat
            1: ["Do\u011frusal Denklemlerin E\u011fimi", "G\u00fcnl\u00fck Hayatta E\u011fim Uygulamalar\u0131", "E\u011fim ve Grafikler Aras\u0131 \u0130li\u015fki"],
            2: ["E\u011fitsizliklere Giri\u015f", "E\u011fitsizlikleri Say\u0131 Do\u011frusunda G\u00f6sterme", "E\u011fitsizlik Problemleri"],
            3: ["E\u011fitsizliklerde Yeni Nesil Sorular", "Do\u011frusal Denklemler ve E\u011fitsizlik Karma", "Analiz Becerisi (Feb)"],
            4: ["\u00dc\u00e7genlere Giri\u015f", "\u00dc\u00e7gen E\u011fitsizli\u011fi", "\u00dc\u00e7genin Yardımc\u0131 Elemanlar\u0131 (Kenarortay, A\u00e7\u0131ortay, Y\u00fckseklik)"]
        },
        3: { # Mart
            1: ["Dik \u00dc\u00e7gende Pisagor Ba\u011f\u0131nt\u0131s\u0131", "Pisagor Ba\u011f\u0131nt\u0131s\u0131 Uygulamalar\u0131", "\u00dc\u00e7gen \u00c7izimi \u015eartlar\u0131"],
            2: ["E\u015flik ve Benzerli\u011fe Giri\u015f", "\u00dc\u00e7genlerde Benzerlik Kurallar\u0131", "Benzerlik Oran\u0131 Uygulamalar\u0131"],
            3: ["D\u00f6n\u00fc\u015f\u00fcm Geometrisi: \u00d6teleme", "D\u00f6n\u00fc\u015f\u00fcm Geometrisi: Yans\u0131ma", "Koordinat D\u00fczleminde D\u00f6n\u00fc\u015f\u00fcmler"],
            4: ["Geometrik Cisimler: Prizmalar", "Prizmalar\u0131n Y\u00fczey Alan\u0131", "Prizmalar\u0131n Hacmi"]
        },
        4: { # Nisan
            1: ["Silindirin Temel Elemanlar\u0131 ve A\u00e7\u0131n\u0131m\u0131", "Silindirin Y\u00fczey Alan\u0131", "Silindirin Hacmi"],
            2: ["Dik Piramitlerin Temel Elemanlar\u0131", "Dik Koni ve Temel Elemanlar\u0131", "Geometrik Cisimler Karma Soru \u00c7\u00f6z\u00fcm\u00fc"],
            3: ["Nisan Ara Tatil Kamp\u0131", "T\u00fcm Konular Karma Deneme", "Yeni Nesil Mant\u0131k Muhakeme (Nisan)"],
            4: ["H\u0111z Testleri ve Zaman Y\u00f6netimi", "Deneme Analiz Teknikleri", "Stres Y\u00f6netimi ve Motivasyon"]
        },
        5: { # May\u0131s
            1: ["May\u0131s Ay\u0111 Genel Tekrar: \u00dccitler 1-2", "LGS Prova Denemeleri (Genel)", "Matematik H\u0131zland\u0131rma Kamp\u0131"],
            2: ["Zorluk Seviyesi Y\u00fcksek Sorular", "Aritmetik Beceri Geli\u015ftirme", "Geriye D\u00f6n\u00fck Eksik Kapatma"],
            3: ["LGS Tarz\u0131 Soru Kal\u0131plar\u0131 (May)", "Matematik Labirent Sorular", "Dikkat ve Odaklanma Egzersizleri"],
            4: ["Son Bir Ay Stratejileri", "Net Art\u0131rma Teknikleri", "Genel Matematik Revizyon"]
        },
        6: { # Haziran
            1: ["LGS Son Tekrar: T\u00fcm Konular", "Deneme Yanl\u0131\u015f Analizleri", "LGS Moral ve Motivasyon"],
            2: ["S\u0131nav G\u00fcn\u00fc Stratejisi", "Form\u00fcl Hat\u0131rlatma Kartlar\u0131", "Final Kontroller"]
        }
    }

    STRATEGIC_LABELS = [
        "Temel \u0130\u015flem Yetene\u011fi",
        "Mant\u0131k Muhakeme Prati\u011fi",
        "Say\u0131sal Analiz \u00c7al\u0131\u015fmas\u0131",
        "LGS Tipi Soru Analizi",
        "H\u0131z Testi ve Zaman Y\u00f6netimi",
        "Hatal\u0131 Soru Analiz Teknikleri",
        "Genel Matematik Tekrar\u0131"
    ]

    print("--- STARTING GLOBAL MATHEMATICS STANDARDIZATION ---")
    
    for month, weeks in ROADMAP.items():
        for week, core_topics in weeks.items():
            print(f"Processing Month {month}, Week {week}...")
            
            # Wipe existing math for this week
            Topic.objects.filter(subject=math, month=month, week=week).delete()
            
            # Build 7 unique topics
            final_list = []
            final_list.extend(core_topics)
            
            # Pad with unique strategic labels
            label_idx = 0
            while len(final_list) < 7:
                label = STRATEGIC_LABELS[label_idx % len(STRATEGIC_LABELS)]
                if label not in final_list:
                    final_list.append(label)
                label_idx += 1
            
            # Create
            for idx, title in enumerate(final_list):
                Topic.objects.create(
                    subject=math,
                    month=month,
                    week=week,
                    order=idx,
                    title=title
                )
    
    print("--- GLOBAL MATHEMATICS STANDARDIZATION COMPLETE ---")

global_refine_math()
