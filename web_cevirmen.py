import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
from io import BytesIO

# Sayfa ayarları
st.set_page_config(page_title="Dil Asistanım", page_icon="📝")

# --- ARKA PLAN VE TASARIM AYARI (CSS) ---
# Resmin doğrudan bağlantısını buraya ekledim
arka_plan_resmi = "https://i.hizliresim.com/g83efef.jpg"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{arka_plan_resmi}");
        background-attachment: fixed;
        background-size: cover;
        background-position: center;
    }}
    
    /* Yazıların olduğu ana kutu tasarımı */
    .main .block-container {{
        background-color: rgba(255, 255, 255, 0.85); /* %85 beyazlık, yazıların okunması için */
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-top: 2rem;
    }}

    /* Başlık ve yazıları daha şık yapalım */
    h1, h2, h3, p {{
        color: #2c3e50 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
# ---------------------------------------

st.title("📝 Dil Asistanım")
st.write("Kelimelerini buraya yazabilir, çevirilerini görebilir ve listenin Excel çıktısını alabilirsin.")

# Hafızayı başlat
if 'kelimeler' not in st.session_state:
    st.session_state.kelimeler = []

# Giriş kutusunu sıfırlamak için kullanılan fonksiyon
def kelime_ekle():
    ingilizce_kelime = st.session_state.yeni_kelime.strip()
    
    if ingilizce_kelime:
        # Çeviri işlemi
        translator = GoogleTranslator(source='en', target='tr')
        try:
            turkce_kelime = translator.translate(ingilizce_kelime)
            
            # Listeye ekle (Eğer daha önce eklenmemişse)
            if not any(d['İngilizce'] == ingilizce_kelime for d in st.session_state.kelimeler):
                st.session_state.kelimeler.append({
                    "İngilizce": ingilizce_kelime, 
                    "Türkçe": turkce_kelime
                })
        except Exception as e:
            st.error("Çeviri sırasında bir hata oluştu.")
    
    # Giriş kutusunu temizle
    st.session_state.yeni_kelime = ""

# Giriş alanı
st.text_input("İngilizce kelime yazın ve Enter'a basın:", key="yeni_kelime", on_change=kelime_ekle)

# Eklenen kelimeleri tablo olarak göster
if st.session_state.kelimeler:
    st.write("### 📚 Kaydedilen Kelimeler")
    df = pd.DataFrame(st.session_state.kelimeler)
    st.table(df)

    # Excel dosyasına dönüştürme
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Kelimelerim')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="📥 Excel Dosyasını İndir",
            data=output.getvalue(),
            file_name="kelimelerim.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    with col2:
        if st.button("🗑️ Listeyi Temizle"):
            st.session_state.kelimeler = []
            st.rerun()
