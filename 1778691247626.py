import sqlite3

# Burası gelen mesajı analiz edip karar veren 'Karar Destek' mekanizması
def asistan_cevap_ver(gelen_soru):
    soru = gelen_soru.lower()
    db = sqlite3.connect('kobi_pilot.db')
    cursor = db.cursor()

    # Senaryo A: Stok Sorgulama
    if "stok" in soru or "var mı" in soru:
        cursor.execute("SELECT urun_adi, stok_miktari FROM Envanter")
        urunler = cursor.fetchall()
        for ad, miktar in urunler:
            if ad.lower() in soru:
                return f"Kontrol ettim, elimizde {miktar} adet {ad} mevcut."
        return "İstediğiniz ürünü bulamadım, ismini tam yazar mısınız?"

    # Senaryo B: Kargo Takibi
    elif "kargo" in soru or "nerede" in soru:
        # Sayıları ayıklayıp sipariş no bulmaya çalışıyoruz
        numara = ''.join(filter(str.isdigit, soru))
        if numara:
            cursor.execute("SELECT kargo_durumu, takip_kodu FROM Siparisler WHERE siparis_no = ?", (numara,))
            sonuc = cursor.fetchone()
            if sonuc:
                return f"{numara} nolu siparişiniz: {sonuc[0]}. Takip No: {sonuc[1]}"
            return f"{numara} nolu bir sipariş bulamadım."
        return "Sipariş durumunu öğrenmek için lütfen sipariş numaranızı yazın."

    else:
        return "Merhaba! Ben KOBİ-Pilot. Size stok bilgisi veya kargo durumu hakkında yardımcı olabilirim."

# Test için:
# print(asistan_cevap_ver("101 nolu siparişim nerede?"))