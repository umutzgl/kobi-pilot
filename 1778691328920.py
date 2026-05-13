import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="KOBİ-Pilot Paneli", layout="wide")

st.title("🚀 KOBİ-Pilot | Operasyonel Takip Paneli")
st.write("İşletme verimliliğini artırmak için hazırlanan otonom kontrol ekranı.")

def veri_cek(tablo):
    conn = sqlite3.connect('kobi_pilot.db')
    df = pd.read_sql_query(f"SELECT * FROM {tablo}", conn)
    conn.close()
    return df

# Üst Kısım: Kritik Stok Uyarıları (Endüstri Mühendisliği Dokunuşu)
st.subheader("🚨 Kritik Stok Alarmları")
df_stok = veri_cek("Envanter")
kritik_durum = df_stok[df_stok['stok_miktari'] < df_stok['kritik_esik']]

if not kritik_durum.empty:
    for _, satir in kritik_durum.iterrows():
        st.warning(f"DİKKAT: {satir['urun_adi']} stoğu {satir['stok_miktari']} birime düştü! (Emniyet Stoğu: {satir['kritik_esik']})")
else:
    st.success("Tüm stok seviyeleri planlanan aralıkta.")

st.divider()

# Alt Kısım: Tablolar
sol, sag = st.columns(2)

with sol:
    st.info("📦 Envanter Listesi")
    st.dataframe(df_stok, use_container_width=True)

with sag:
    st.info("🚚 Sipariş ve Kargo Takibi")
    df_siparis = veri_cek("Siparisler")
    st.write(df_siparis)

st.sidebar.title("KOBİ-Pilot Ayarlar")
st.sidebar.info("Beşiktaş Mağazası Aktif")
if st.sidebar.button("Stok Raporu Oluştur"):
    st.sidebar.success("Rapor yöneticiye iletildi.")