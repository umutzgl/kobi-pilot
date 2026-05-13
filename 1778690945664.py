import sqlite3

# Adım 1: Veritabanını ve tabloları hazırlıyoruz
def kurulum_yap():
    # Dosya ismini 'kobi_pilot' yaptım, projeye özel olsun
    baglanti = sqlite3.connect('kobi_pilot.db')
    murekkep = baglanti.cursor()

    # Envanter Tablosu: Mühendislik dokunuşu olarak 'kritik_esik' ekledim
    murekkep.execute('''
        CREATE TABLE IF NOT EXISTS Envanter (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            urun_adi TEXT,
            stok_miktari INTEGER,
            kritik_esik INTEGER, -- Bu değerin altına düşerse sistem alarm verecek
            fiyat REAL
        )
    ''')

    # Siparişler Tablosu: Kargo takibi için
    murekkep.execute('''
        CREATE TABLE IF NOT EXISTS Siparisler (
            siparis_no INTEGER PRIMARY KEY,
            musteri_ad TEXT,
            kargo_durumu TEXT,
            takip_kodu TEXT
        )
    ''')

    # Örnek veriler (Demo sırasında jüriye dolu gözüksün diye)
    urun_listesi = [
        ('Sızma Zeytinyağı 5L', 25, 10, 1100.0),
        ('Kurutulmuş Domates', 8, 15, 200.0), # Bak bu stokta az kalmış, sistem uyaracak
        ('Organik Çiçek Balı', 40, 5, 750.0)
    ]
    
    siparis_listesi = [
        (101, 'Ahmet Y.', 'Yolda', 'KP-TR-001'),
        (102, 'Ayşe K.', 'Hazırlanıyor', '-')
    ]

    murekkep.executemany('INSERT INTO Envanter (urun_adi, stok_miktari, kritik_esik, fiyat) VALUES (?,?,?,?)', urun_listesi)
    murekkep.executemany('INSERT INTO Siparisler VALUES (?,?,?,?)', siparis_listesi)

    baglanti.commit()
    baglanti.close()
    print("Veritabanı başarıyla kuruldu ve örnek veriler yüklendi.")

if __name__ == "__main__":
    kurulum_yap()